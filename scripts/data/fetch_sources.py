#!/usr/bin/env python3
"""Fetch registered source documents as immutable local raw snapshots."""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY_PATH = REPOSITORY_ROOT / "data" / "metadata" / "source_registry.csv"
DEFAULT_STAGING_ROOT = REPOSITORY_ROOT / "data" / "staging"

EXPECTED_COLUMNS = (
    "source_id",
    "dataset_name",
    "publisher",
    "source_url",
    "source_vintage",
    "published_date",
    "retrieved_at",
    "format",
    "crs",
    "historical_fit",
    "analytical_role",
    "license_notes",
    "checksum",
    "known_caveats",
    "notes",
)
ALLOWED_HISTORICAL_FIT = frozenset(
    {
        "valid",
        "uncertain",
        "invalid",
        "valid_as_dated_2021_snapshot",
        "valid_as_documentary_context_only",
    }
)
ALLOWED_ANALYTICAL_ROLES = frozenset(
    {"analytical", "contextual", "benchmark", "research-only"}
)
CHECKSUM_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
UTC_TIMESTAMP_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$"
)

# These paths are both deterministic local suffixes and intended object paths in
# the existing raw-data bucket. No bucket name or credential belongs here.
SOURCE_OBJECT_PATHS = {
    "austin_wpd_2026_bond_projects_2025_11_21": Path(
        "raw/city_austin/watershed_bond_projects/2025-11-21/source.pdf"
    ),
    "austin_2026_bond_initial_draft_2026_01_21": Path(
        "raw/city_austin/initial_draft_recommendation/2026-01-21/source.pdf"
    ),
}


class RegistryValidationError(ValueError):
    """Raised when the canonical source registry violates its contract."""


class SourceFetchError(RuntimeError):
    """Raised when a source cannot be fetched or safely persisted."""


class SnapshotConflictError(SourceFetchError):
    """Raised when a historical snapshot exists with different bytes."""


@dataclass(frozen=True)
class DownloadResponse:
    body: bytes
    http_status: int
    final_url: str


@dataclass(frozen=True)
class FetchResult:
    source_id: str
    http_status: int
    local_path: Path
    byte_size: int
    checksum: str
    retrieved_at: str
    snapshot_status: str


def sha256_checksum(content: bytes) -> str:
    """Return a registry-formatted SHA-256 checksum for exact bytes."""

    return "sha256:" + hashlib.sha256(content).hexdigest()


def utc_retrieval_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp with second precision."""

    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )


def _validate_published_date(value: str, row_number: int) -> None:
    # Live services may not publish an effective/publication date. An empty value
    # preserves that unknown rather than substituting the retrieval date.
    if not value:
        return
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise RegistryValidationError(
            f"Row {row_number}: published_date must be a valid ISO date; got {value!r}."
        ) from error
    if parsed.isoformat() != value:
        raise RegistryValidationError(
            f"Row {row_number}: published_date must use YYYY-MM-DD; got {value!r}."
        )


def _validate_utc_timestamp(value: str, context: str) -> None:
    if not UTC_TIMESTAMP_PATTERN.fullmatch(value):
        raise RegistryValidationError(
            f"{context}: retrieved_at must be an ISO-8601 UTC timestamp ending in Z; "
            f"got {value!r}."
        )
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as error:
        raise RegistryValidationError(
            f"{context}: retrieved_at is not a valid timestamp; got {value!r}."
        ) from error
    if parsed.utcoffset() != timedelta(0):
        raise RegistryValidationError(
            f"{context}: retrieved_at must be UTC; got {value!r}."
        )


def validate_registry_rows(
    columns: list[str], rows: list[dict[str, str]]
) -> None:
    """Validate registry headers and governed field values."""

    if tuple(columns) != EXPECTED_COLUMNS:
        raise RegistryValidationError(
            "source_registry.csv columns must exactly match this order: "
            + ", ".join(EXPECTED_COLUMNS)
        )

    source_ids: set[str] = set()
    for row_number, row in enumerate(rows, start=2):
        if None in row or set(row) != set(EXPECTED_COLUMNS):
            raise RegistryValidationError(
                f"Row {row_number}: row shape does not match the required columns."
            )

        source_id = row["source_id"].strip()
        if not source_id:
            raise RegistryValidationError(f"Row {row_number}: source_id is required.")
        if source_id in source_ids:
            raise RegistryValidationError(
                f"Row {row_number}: duplicate source_id {source_id!r}."
            )
        source_ids.add(source_id)

        _validate_published_date(row["published_date"], row_number)

        historical_fit = row["historical_fit"]
        if historical_fit not in ALLOWED_HISTORICAL_FIT:
            raise RegistryValidationError(
                f"Row {row_number}: historical_fit {historical_fit!r} is not allowed."
            )

        analytical_role = row["analytical_role"]
        if analytical_role not in ALLOWED_ANALYTICAL_ROLES:
            raise RegistryValidationError(
                f"Row {row_number}: analytical_role {analytical_role!r} is not allowed."
            )

        checksum = row["checksum"]
        if checksum and not CHECKSUM_PATTERN.fullmatch(checksum):
            raise RegistryValidationError(
                f"Row {row_number}: checksum must be empty or sha256:<64 lowercase hex>."
            )

        retrieved_at = row["retrieved_at"]
        if retrieved_at:
            _validate_utc_timestamp(retrieved_at, f"Row {row_number}")

        parsed_url = urlsplit(row["source_url"])
        if parsed_url.scheme.lower() != "https" or not parsed_url.netloc:
            raise RegistryValidationError(
                f"Row {row_number}: source_url must be an absolute HTTPS URL."
            )


def load_registry(registry_path: Path) -> list[dict[str, str]]:
    """Read and validate the canonical source registry."""

    try:
        with registry_path.open("r", encoding="utf-8", newline="") as registry_file:
            reader = csv.DictReader(registry_file)
            columns = list(reader.fieldnames or [])
            rows = list(reader)
    except OSError as error:
        raise RegistryValidationError(
            f"Unable to read source registry {registry_path}: {error}"
        ) from error

    validate_registry_rows(columns, rows)
    return rows


def download_https(url: str, timeout: float = 60.0) -> DownloadResponse:
    """Download exact response bytes from an HTTPS source."""

    parsed_url = urlsplit(url)
    if parsed_url.scheme.lower() != "https" or not parsed_url.netloc:
        raise SourceFetchError(f"Refusing non-HTTPS source URL: {url!r}")

    request = Request(
        url,
        headers={"User-Agent": "ClimateCapitalAI-data-reconnaissance/1.0"},
        method="GET",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            status = response.getcode()
            final_url = response.geturl()
            if status is None or not 200 <= status < 300:
                raise SourceFetchError(
                    f"HTTP download failed for {url}: unexpected status {status}."
                )
            if urlsplit(final_url).scheme.lower() != "https":
                raise SourceFetchError(
                    f"Refusing HTTPS downgrade while fetching {url}: {final_url}"
                )
            body = response.read()
    except HTTPError as error:
        raise SourceFetchError(
            f"HTTP download failed for {url}: status {error.code} {error.reason}."
        ) from error
    except URLError as error:
        raise SourceFetchError(f"HTTPS download failed for {url}: {error.reason}.") from error
    except TimeoutError as error:
        raise SourceFetchError(f"HTTPS download timed out for {url}.") from error
    except OSError as error:
        raise SourceFetchError(f"HTTPS download failed for {url}: {error}.") from error

    if not body:
        raise SourceFetchError(f"HTTPS download returned no bytes for {url}.")
    if not body.startswith(b"%PDF-"):
        raise SourceFetchError(
            f"HTTPS response for {url} is not a PDF byte stream (missing %PDF- header)."
        )

    return DownloadResponse(body=body, http_status=status, final_url=final_url)


def _compare_existing_snapshot(destination: Path, content: bytes) -> str:
    existing = destination.read_bytes()
    if existing == content:
        return "identical"
    raise SnapshotConflictError(
        f"Historical snapshot already exists with different bytes: {destination}. "
        f"Existing {sha256_checksum(existing)}; downloaded {sha256_checksum(content)}. "
        "The existing snapshot was not overwritten."
    )


def write_snapshot(destination: Path, content: bytes) -> str:
    """Persist exact bytes once, or report an identical existing snapshot."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        return _compare_existing_snapshot(destination, content)

    temporary_path = destination.with_name(destination.name + ".part")
    try:
        with temporary_path.open("xb") as temporary_file:
            temporary_file.write(content)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
    except FileExistsError as error:
        raise SourceFetchError(
            f"Temporary download path already exists: {temporary_path}. "
            "Inspect or remove the stale partial file before retrying."
        ) from error
    except OSError as error:
        if temporary_path.exists():
            temporary_path.unlink()
        raise SourceFetchError(
            f"Unable to write temporary snapshot {temporary_path}: {error}"
        ) from error

    try:
        os.link(temporary_path, destination)
    except FileExistsError:
        return _compare_existing_snapshot(destination, content)
    except OSError as error:
        raise SourceFetchError(
            f"Unable to finalize immutable snapshot {destination}: {error}"
        ) from error
    finally:
        if temporary_path.exists():
            temporary_path.unlink()

    return "created"


def update_registry(
    registry_path: Path, source_id: str, retrieved_at: str, checksum: str
) -> None:
    """Atomically update retrieval metadata for exactly one registered source."""

    rows = load_registry(registry_path)
    matching_rows = [row for row in rows if row["source_id"] == source_id]
    if len(matching_rows) != 1:
        raise RegistryValidationError(
            f"Expected exactly one registry row for {source_id!r}; found {len(matching_rows)}."
        )

    matching_rows[0]["retrieved_at"] = retrieved_at
    matching_rows[0]["checksum"] = checksum
    validate_registry_rows(list(EXPECTED_COLUMNS), rows)

    temporary_path = registry_path.with_name(registry_path.name + ".tmp")
    try:
        with temporary_path.open("x", encoding="utf-8", newline="") as temporary_file:
            writer = csv.DictWriter(
                temporary_file,
                fieldnames=list(EXPECTED_COLUMNS),
                lineterminator="\n",
            )
            writer.writeheader()
            writer.writerows(rows)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_path, registry_path)
    except FileExistsError as error:
        raise RegistryValidationError(
            f"Temporary registry path already exists: {temporary_path}. "
            "Inspect or remove the stale file before retrying."
        ) from error
    except OSError as error:
        raise RegistryValidationError(
            f"Unable to update source registry {registry_path}: {error}"
        ) from error
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


Downloader = Callable[[str, float], DownloadResponse]
Clock = Callable[[], str]


def fetch_registered_source(
    source_id: str,
    registry_path: Path = DEFAULT_REGISTRY_PATH,
    staging_root: Path = DEFAULT_STAGING_ROOT,
    timeout: float = 60.0,
    downloader: Downloader = download_https,
    clock: Clock = utc_retrieval_timestamp,
) -> FetchResult:
    """Fetch one registered source and update its retrieval metadata."""

    rows = load_registry(registry_path)
    matching_rows = [row for row in rows if row["source_id"] == source_id]
    if len(matching_rows) != 1:
        raise SourceFetchError(
            f"Expected exactly one registry row for {source_id!r}; found {len(matching_rows)}."
        )
    if source_id not in SOURCE_OBJECT_PATHS:
        raise SourceFetchError(
            f"No deterministic staging path is configured for source_id {source_id!r}."
        )

    source = matching_rows[0]
    response = downloader(source["source_url"], timeout)
    if not 200 <= response.http_status < 300:
        raise SourceFetchError(
            f"HTTP download failed for {source['source_url']}: "
            f"status {response.http_status}."
        )
    if urlsplit(response.final_url).scheme.lower() != "https":
        raise SourceFetchError(
            f"Refusing non-HTTPS final URL for {source_id}: {response.final_url}"
        )
    if not response.body.startswith(b"%PDF-"):
        raise SourceFetchError(
            f"Downloaded bytes for {source_id} are not a PDF byte stream."
        )

    retrieved_at = clock()
    try:
        _validate_utc_timestamp(retrieved_at, source_id)
    except RegistryValidationError as error:
        raise SourceFetchError(str(error)) from error

    checksum = sha256_checksum(response.body)
    local_path = staging_root / SOURCE_OBJECT_PATHS[source_id]
    snapshot_status = write_snapshot(local_path, response.body)
    update_registry(registry_path, source_id, retrieved_at, checksum)

    return FetchResult(
        source_id=source_id,
        http_status=response.http_status,
        local_path=local_path,
        byte_size=len(response.body),
        checksum=checksum,
        retrieved_at=retrieved_at,
        snapshot_status=snapshot_status,
    )


def _display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPOSITORY_ROOT))
    except ValueError:
        return str(path)


def _build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Download registered authoritative PDFs to immutable local staging "
            "paths and update source_registry.csv retrieval metadata."
        )
    )
    parser.add_argument(
        "--source-id",
        action="append",
        dest="source_ids",
        help="Fetch one source_id; repeat to fetch multiple. Defaults to both sources.",
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=DEFAULT_REGISTRY_PATH,
        help="Path to source_registry.csv.",
    )
    parser.add_argument(
        "--staging-root",
        type=Path,
        default=DEFAULT_STAGING_ROOT,
        help="Ignored local staging root for immutable source snapshots.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=60.0,
        help="HTTPS request timeout in seconds (default: 60).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_argument_parser().parse_args(argv)
    source_ids = args.source_ids or list(SOURCE_OBJECT_PATHS)
    failures = 0

    for source_id in source_ids:
        try:
            result = fetch_registered_source(
                source_id=source_id,
                registry_path=args.registry,
                staging_root=args.staging_root,
                timeout=args.timeout,
            )
        except (RegistryValidationError, SourceFetchError) as error:
            failures += 1
            print(f"FAILURE: {source_id}", file=sys.stderr)
            print(f"  {error}", file=sys.stderr)
            continue

        print(f"SUCCESS: {result.source_id}")
        print(f"  HTTP status: {result.http_status}")
        print(f"  Local staging path: {_display_path(result.local_path)}")
        print(f"  Snapshot status: {result.snapshot_status}")
        print(f"  Byte size: {result.byte_size}")
        print(f"  Checksum: {result.checksum}")
        print(f"  Retrieved at: {result.retrieved_at}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
