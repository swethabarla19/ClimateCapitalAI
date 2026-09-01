from __future__ import annotations

import hashlib
import os
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.data import fetch_sources


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPOSITORY_ROOT / "data" / "metadata" / "source_registry.csv"


class SourceRegistryTests(unittest.TestCase):
    def test_canonical_registry_is_valid_and_contains_registered_sources(self) -> None:
        rows = fetch_sources.load_registry(REGISTRY_PATH)

        self.assertEqual(
            [row["source_id"] for row in rows],
            [
                "austin_wpd_2026_bond_projects_2025_11_21",
                "austin_2026_bond_initial_draft_2026_01_21",
                "austin_rna_projects_layer_8_live",
            ],
        )
        self.assertEqual(rows[0]["analytical_role"], "analytical")
        self.assertEqual(rows[1]["analytical_role"], "benchmark")
        self.assertEqual(rows[2]["historical_fit"], "uncertain")
        self.assertEqual(rows[2]["analytical_role"], "research-only")
        self.assertEqual(rows[2]["published_date"], "")
        self.assertEqual(rows[2]["crs"], "ESRI:102739 (EPSG:2277)")
        self.assertTrue(
            all(
                row["retrieved_at"] == ""
                or fetch_sources.UTC_TIMESTAMP_PATTERN.fullmatch(row["retrieved_at"])
                for row in rows
            )
        )
        self.assertTrue(
            all(
                row["checksum"] == ""
                or fetch_sources.CHECKSUM_PATTERN.fullmatch(row["checksum"])
                for row in rows
            )
        )

    def test_registry_allows_unknown_published_date_but_rejects_bad_nonempty_date(self) -> None:
        rows = fetch_sources.load_registry(REGISTRY_PATH)
        self.assertEqual(rows[2]["published_date"], "")

        candidate = deepcopy(rows)
        candidate[2]["published_date"] = "2026/09/01"
        with self.assertRaises(fetch_sources.RegistryValidationError):
            fetch_sources.validate_registry_rows(
                list(fetch_sources.EXPECTED_COLUMNS), candidate
            )

    def test_registry_rejects_invalid_contract_values(self) -> None:
        rows = fetch_sources.load_registry(REGISTRY_PATH)
        invalid_cases = {
            "duplicate source_id": ("source_id", rows[0]["source_id"]),
            "published date": ("published_date", "2025/11/21"),
            "historical fit": ("historical_fit", "maybe"),
            "analytical role": ("analytical_role", "input"),
            "checksum": ("checksum", "sha256:ABC"),
            "retrieval timestamp": ("retrieved_at", "2026-08-31T12:00:00"),
            "source URL": ("source_url", "http://example.com/source.pdf"),
        }

        for label, (field, value) in invalid_cases.items():
            with self.subTest(label=label):
                candidate = deepcopy(rows)
                candidate[1][field] = value
                with self.assertRaises(fetch_sources.RegistryValidationError):
                    fetch_sources.validate_registry_rows(
                        list(fetch_sources.EXPECTED_COLUMNS), candidate
                    )

    def test_registry_rejects_wrong_column_order(self) -> None:
        rows = fetch_sources.load_registry(REGISTRY_PATH)
        columns = list(fetch_sources.EXPECTED_COLUMNS)
        columns[0], columns[1] = columns[1], columns[0]

        with self.assertRaises(fetch_sources.RegistryValidationError):
            fetch_sources.validate_registry_rows(columns, rows)


class SnapshotTests(unittest.TestCase):
    def test_downloaded_bytes_are_written_unchanged_and_checksum_matches(self) -> None:
        downloaded = b"%PDF-1.7\nexact raw bytes\x00\xff\n%%EOF\n"
        expected_checksum = "sha256:" + hashlib.sha256(downloaded).hexdigest()

        with tempfile.TemporaryDirectory() as temporary_directory:
            destination = Path(temporary_directory) / "nested" / "source.pdf"
            status = fetch_sources.write_snapshot(destination, downloaded)

            self.assertEqual(status, "created")
            self.assertEqual(destination.read_bytes(), downloaded)
            self.assertEqual(fetch_sources.sha256_checksum(downloaded), expected_checksum)

    def test_existing_different_snapshot_is_never_overwritten(self) -> None:
        original = b"%PDF-1.4\noriginal\n%%EOF\n"
        replacement = b"%PDF-1.4\nreplacement\n%%EOF\n"

        with tempfile.TemporaryDirectory() as temporary_directory:
            destination = Path(temporary_directory) / "source.pdf"
            destination.write_bytes(original)

            with self.assertRaises(fetch_sources.SnapshotConflictError):
                fetch_sources.write_snapshot(destination, replacement)

            self.assertEqual(destination.read_bytes(), original)

    def test_existing_identical_snapshot_is_reported_without_rewrite(self) -> None:
        downloaded = b"%PDF-1.4\nidentical\n%%EOF\n"

        with tempfile.TemporaryDirectory() as temporary_directory:
            destination = Path(temporary_directory) / "source.pdf"
            destination.write_bytes(downloaded)
            original_mtime = 1_700_000_000
            destination.touch()
            destination.chmod(0o600)
            os.utime(destination, (original_mtime, original_mtime))

            status = fetch_sources.write_snapshot(destination, downloaded)

            self.assertEqual(status, "identical")
            self.assertEqual(destination.read_bytes(), downloaded)
            self.assertEqual(int(destination.stat().st_mtime), original_mtime)


class FetchWorkflowTests(unittest.TestCase):
    def test_fetch_updates_only_metadata_after_exact_snapshot_is_persisted(self) -> None:
        downloaded = b"%PDF-1.7\nworkflow bytes\n%%EOF\n"
        retrieved_at = "2026-08-31T18:30:00Z"

        def fake_downloader(url: str, timeout: float) -> fetch_sources.DownloadResponse:
            self.assertTrue(url.startswith("https://"))
            self.assertGreater(timeout, 0)
            return fetch_sources.DownloadResponse(
                body=downloaded,
                http_status=200,
                final_url=url,
            )

        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            registry = temporary_root / "source_registry.csv"
            registry.write_bytes(REGISTRY_PATH.read_bytes())
            staging_root = temporary_root / "staging"
            original_rows = {
                row["source_id"]: row for row in fetch_sources.load_registry(registry)
            }
            untouched_checksum = original_rows[
                "austin_2026_bond_initial_draft_2026_01_21"
            ]["checksum"]

            result = fetch_sources.fetch_registered_source(
                source_id="austin_wpd_2026_bond_projects_2025_11_21",
                registry_path=registry,
                staging_root=staging_root,
                downloader=fake_downloader,
                clock=lambda: retrieved_at,
            )

            expected_path = staging_root / Path(
                "raw/city_austin/watershed_bond_projects/2025-11-21/source.pdf"
            )
            self.assertEqual(result.local_path, expected_path)
            self.assertEqual(result.byte_size, len(downloaded))
            self.assertEqual(result.snapshot_status, "created")
            self.assertEqual(expected_path.read_bytes(), downloaded)

            updated = {
                row["source_id"]: row for row in fetch_sources.load_registry(registry)
            }
            source = updated["austin_wpd_2026_bond_projects_2025_11_21"]
            self.assertEqual(source["retrieved_at"], retrieved_at)
            self.assertEqual(source["checksum"], result.checksum)
            self.assertEqual(
                updated["austin_2026_bond_initial_draft_2026_01_21"]["checksum"],
                untouched_checksum,
            )

            repeated = fetch_sources.fetch_registered_source(
                source_id="austin_wpd_2026_bond_projects_2025_11_21",
                registry_path=registry,
                staging_root=staging_root,
                downloader=fake_downloader,
                clock=lambda: retrieved_at,
            )
            self.assertEqual(repeated.snapshot_status, "identical")

    def test_unsuccessful_http_status_does_not_create_a_snapshot(self) -> None:
        def failed_downloader(
            url: str, timeout: float
        ) -> fetch_sources.DownloadResponse:
            return fetch_sources.DownloadResponse(
                body=b"%PDF-1.7\nshould not be written\n%%EOF\n",
                http_status=503,
                final_url=url,
            )

        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            registry = temporary_root / "source_registry.csv"
            registry.write_bytes(REGISTRY_PATH.read_bytes())
            staging_root = temporary_root / "staging"

            with self.assertRaises(fetch_sources.SourceFetchError):
                fetch_sources.fetch_registered_source(
                    source_id="austin_wpd_2026_bond_projects_2025_11_21",
                    registry_path=registry,
                    staging_root=staging_root,
                    downloader=failed_downloader,
                )

            self.assertFalse(staging_root.exists())

    def test_http_downloader_rejects_non_https_url_before_network_access(self) -> None:
        with self.assertRaises(fetch_sources.SourceFetchError):
            fetch_sources.download_https("http://example.com/source.pdf", timeout=1)


if __name__ == "__main__":
    unittest.main()
