"""Fail-closed validation for the fixed four-file release-data bundle."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, TypeVar

from pydantic import BaseModel, ValidationError

from climatecapital.contracts.artifacts import (
    BenchmarkArtifact,
    CatalogArtifact,
    MapContextArtifact,
    ReleaseManifest,
)
from climatecapital.contracts.authority import REGISTERED_SOURCE_IDENTITIES
from climatecapital.contracts.common import Availability, EvidenceType, ReleaseTier
from climatecapital.contracts.versions import (
    ACTIVE_FAMILY_PROJECT_IDS,
    CITYWIDE_PROJECT_ID,
    GOVERNED_SOURCE_ID,
    RNA_SOURCE_ID,
    RELEASE_ARTIFACT_FILENAMES,
)

MAX_ARTIFACT_BYTES = 50 * 1024 * 1024


@dataclass(frozen=True, slots=True)
class ValidationViolation:
    code: str
    path: str
    message: str


class BundleValidationError(ValueError):
    """Safe, structured bundle rejection without artifact content."""

    def __init__(self, violations: list[ValidationViolation]):
        self.violations = tuple(violations)
        summary = "; ".join(
            f"{item.code} at {item.path}: {item.message}" for item in violations
        )
        super().__init__(summary)


@dataclass(frozen=True, slots=True)
class ValidatedBundle:
    manifest: ReleaseManifest
    catalog: CatalogArtifact
    map_context: MapContextArtifact
    benchmark: BenchmarkArtifact
    manifest_sha256: str


ModelT = TypeVar("ModelT", bound=BaseModel)


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number {value!r} is forbidden")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def _canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def _read_artifact(
    path: Path, model_type: type[ModelT]
) -> tuple[bytes, Any, ModelT]:
    if path.is_symlink() or not path.is_file():
        raise ValueError("artifact must be a regular non-symlink file")
    size = path.stat().st_size
    if size <= 0 or size > MAX_ARTIFACT_BYTES:
        raise ValueError(f"artifact byte size must be within 1..{MAX_ARTIFACT_BYTES}")
    payload = path.read_bytes()
    if payload.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM is forbidden")
    if b"\r" in payload or not payload.endswith(b"\n"):
        raise ValueError("artifacts require Unix newlines and one final newline")
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("artifact is not valid UTF-8") from error
    try:
        raw = json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except (json.JSONDecodeError, ValueError) as error:
        raise ValueError(f"invalid strict JSON: {error}") from error
    if payload != _canonical_bytes(raw):
        raise ValueError("artifact bytes are not in deterministic canonical JSON form")
    try:
        model = model_type.model_validate_json(payload, strict=True)
    except ValidationError as error:
        first = error.errors(include_url=False)[0]
        location = ".".join(str(part) for part in first["loc"])
        raise ValueError(f"schema violation at {location or '<root>'}: {first['msg']}") from error
    return payload, raw, model


def _normalize_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def _walk_keys(value: Any, path: str = "$") -> Iterator[tuple[str, str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            yield child_path, key
            yield from _walk_keys(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_keys(child, f"{path}[{index}]")


def _walk_strings(value: Any, path: str = "$") -> Iterator[tuple[str, str]]:
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for key, child in value.items():
            yield from _walk_strings(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_strings(child, f"{path}[{index}]")


ANALYTICAL_FORBIDDEN_KEY_FRAGMENTS = (
    "fundingpriority",
    "priorityscore",
    "projectrank",
    "climateriskscore",
    "communityvulnerabilityscore",
    "communityequityscore",
    "importancesweight",
    "importanceweight",
    "objectiveweight",
    "optimizermembership",
    "optimizedmembership",
    "objectivevalue",
    "tiebreak",
    "preferredcombination",
    "expectedfloodreductionbenefit",
    "benefitestimate",
    "imputedevidence",
    "missingnesspenalty",
    "confidenceasneed",
    "editablerequest",
    "partialrequest",
)

CATALOG_MAP_BENCHMARK_KEY_FRAGMENTS = (
    "historicalcityrecommendation",
    "benchmarktreatment",
    "benchmarkmembership",
    "cityincluded",
    "citytreatment",
)

BENCHMARK_CORE_KEY_FRAGMENTS = (
    "p0family",
    "governedrequest",
    "planmembership",
    "projectevidence",
)

MANIFEST_CIRCULAR_KEY_FRAGMENTS = (
    "manifestsha256",
    "codegitsha",
    "containinggitsha",
    "containerimagedigest",
    "releaseid",
    "runtimestate",
    "sessionstate",
)


def _scan_forbidden_keys(
    raw: Any,
    fragments: tuple[str, ...],
    artifact_name: str,
) -> list[ValidationViolation]:
    violations: list[ValidationViolation] = []
    for path, key in _walk_keys(raw):
        normalized = _normalize_key(key)
        matched = next((fragment for fragment in fragments if fragment in normalized), None)
        if matched:
            violations.append(
                ValidationViolation(
                    "FORBIDDEN_FIELD",
                    f"{artifact_name}:{path}",
                    f"field name violates locked contract ({matched})",
                )
            )
    return violations


def _model_json(model: BaseModel) -> dict[str, Any]:
    return model.model_dump(mode="json", by_alias=True, exclude_none=False)


def _source_ids_from_catalog(catalog: CatalogArtifact) -> set[str]:
    ids = set(catalog.source_references)
    for project in catalog.projects:
        ids.add(project.source_row.source_id)
        ids.update(project.provenance_refs)
        for item in project.evidence:
            ids.update(item.source_ids)
    return ids


def _source_ids_from_map(map_context: MapContextArtifact) -> set[str]:
    return {feature.properties.source_id for feature in map_context.features}


def _source_ids_from_benchmark(benchmark: BenchmarkArtifact) -> set[str]:
    ids = set(benchmark.source_references)
    ids.add(benchmark.benchmark_identity.source_id)
    for entry in benchmark.published_project_treatments:
        ids.update(entry.source_ids)
    return ids


def _validate_registered_sources(manifest: ReleaseManifest) -> list[ValidationViolation]:
    violations: list[ValidationViolation] = []
    for source in manifest.sources:
        expected = REGISTERED_SOURCE_IDENTITIES.get(source.source_id)
        path = f"manifest.json:sources.{source.source_id}"
        if expected is None:
            violations.append(
                ValidationViolation(
                    "UNREGISTERED_SOURCE",
                    path,
                    "source_id is not present in the approved repository source authority",
                )
            )
            continue
        actual_identity = (
            source.publisher,
            source.title,
            source.source_url,
            source.source_vintage,
            source.published_date,
            source.retrieval_timestamp,
            source.sha256,
            source.byte_size,
            source.historical_fit,
            source.license_reuse_status,
        )
        expected_identity = (
            expected.publisher,
            expected.title,
            expected.source_url,
            expected.source_vintage,
            expected.published_date,
            expected.retrieval_timestamp,
            expected.sha256,
            expected.byte_size,
            expected.historical_fit,
            expected.license_reuse_status,
        )
        if actual_identity != expected_identity:
            violations.append(
                ValidationViolation(
                    "SOURCE_REGISTRATION_MISMATCH",
                    path,
                    "bundle source identity differs from approved repository authority",
                )
            )
        gcs = source.gcs_object
        if gcs is None or (
            gcs.uri,
            gcs.generation,
            gcs.sha256,
            gcs.byte_size,
        ) != (
            expected.gcs_uri,
            expected.gcs_generation,
            expected.sha256,
            expected.byte_size,
        ):
            violations.append(
                ValidationViolation(
                    "REQUIRED_GCS_PIN_MISMATCH",
                    f"{path}.gcs_object",
                    "known preserved source requires its exact approved GCS object identity",
                )
            )
    return violations


def _validate_cross_file_semantics(
    manifest: ReleaseManifest,
    catalog: CatalogArtifact,
    map_context: MapContextArtifact,
    benchmark: BenchmarkArtifact,
) -> list[ValidationViolation]:
    violations: list[ValidationViolation] = []
    artifacts = (catalog, map_context, benchmark)
    for name, artifact in zip(
        ("catalog.json", "map-context.geojson", "benchmark.json"), artifacts, strict=True
    ):
        if artifact.data_version != manifest.data_version:
            violations.append(
                ValidationViolation("DATA_VERSION_MISMATCH", name, "data_version differs from manifest")
            )
        if artifact.release_tier != manifest.release_tier:
            violations.append(
                ValidationViolation("RELEASE_TIER_MISMATCH", name, "release_tier differs from manifest")
            )

    expected_contracts = {
        "catalog.json": manifest.contract_versions.catalog,
        "map-context.geojson": manifest.contract_versions.map_context,
        "benchmark.json": manifest.contract_versions.benchmark,
    }
    for name, artifact in zip(
        ("catalog.json", "map-context.geojson", "benchmark.json"), artifacts, strict=True
    ):
        if artifact.contract_version != expected_contracts[name]:
            violations.append(
                ValidationViolation(
                    "CONTRACT_VERSION_MISMATCH",
                    name,
                    "artifact contract_version differs from manifest contract set",
                )
            )

    approved_ids = set(manifest.approved_source_ids)
    referenced_by_artifact = {
        "catalog.json": _source_ids_from_catalog(catalog),
        "map-context.geojson": _source_ids_from_map(map_context),
        "benchmark.json": _source_ids_from_benchmark(benchmark),
    }
    for name, source_ids in referenced_by_artifact.items():
        unknown = sorted(source_ids - approved_ids)
        if unknown:
            violations.append(
                ValidationViolation(
                    "UNAPPROVED_SOURCE_REFERENCE",
                    name,
                    f"source references are not approved: {unknown}",
                )
            )

    manifest_sources = {source.source_id: _model_json(source) for source in manifest.sources}
    manifest_source_models = {source.source_id: source for source in manifest.sources}
    for source_id, source in catalog.source_references.items():
        if source_id in manifest_sources and _model_json(source) != manifest_sources[source_id]:
            violations.append(
                ValidationViolation(
                    "SOURCE_IDENTITY_MISMATCH",
                    f"catalog.json:source_references.{source_id}",
                    "catalog and manifest source identity differ",
                )
            )
    for source_id, source in benchmark.source_references.items():
        if source_id in manifest_sources and _model_json(source) != manifest_sources[source_id]:
            violations.append(
                ValidationViolation(
                    "SOURCE_IDENTITY_MISMATCH",
                    f"benchmark.json:source_references.{source_id}",
                    "benchmark and manifest source identity differ",
                )
            )

    transform_by_evidence_type = {
        EvidenceType.GOVERNED_PROJECT_IDENTITY: manifest.transformation_versions.extractor,
        EvidenceType.GOVERNED_REQUEST: manifest.transformation_versions.extractor,
        EvidenceType.DERIVED_PURPOSE: manifest.transformation_versions.classification,
        EvidenceType.P0_FAMILY: manifest.transformation_versions.classification,
        EvidenceType.PROBLEM_SCORE_ASSOCIATION: manifest.transformation_versions.join,
        EvidenceType.RNA_DISPLAY_GEOMETRY_AVAILABILITY: manifest.transformation_versions.join,
        EvidenceType.FEMA_CURRENT_HAZARD_CONTEXT: manifest.transformation_versions.join,
        EvidenceType.EAZ_2021_CONTEXT: manifest.transformation_versions.join,
        EvidenceType.EXPECTED_FLOOD_REDUCTION_BENEFIT: None,
        EvidenceType.BENEFICIARY_ESTIMATES: None,
    }
    for project in catalog.projects:
        if project.purpose.transformation_version != manifest.transformation_versions.classification:
            violations.append(
                ValidationViolation(
                    "TRANSFORMATION_VERSION_MISMATCH",
                    f"catalog.json:projects.{project.project_id}.purpose",
                    "purpose transformation differs from the manifest classification version",
                )
            )
        for item in project.evidence:
            item_path = (
                f"catalog.json:projects.{project.project_id}.evidence.{item.evidence_type}"
            )
            referenced_sources = [
                manifest_source_models[source_id]
                for source_id in item.source_ids
                if source_id in manifest_source_models
            ]
            if referenced_sources and any(
                source.historical_fit != item.historical_fit
                or source.source_vintage != item.source_vintage
                for source in referenced_sources
            ):
                violations.append(
                    ValidationViolation(
                        "EVIDENCE_PROVENANCE_MISMATCH",
                        item_path,
                        "evidence vintage/historical fit differs from its referenced source",
                    )
                )
            expected_transformation = transform_by_evidence_type[item.evidence_type]
            if item.transformation_version != expected_transformation:
                violations.append(
                    ValidationViolation(
                        "TRANSFORMATION_VERSION_MISMATCH",
                        item_path,
                        "evidence transformation differs from its locked manifest stage",
                    )
                )
        identity_sources = next(
            item.source_ids
            for item in project.evidence
            if item.evidence_type == EvidenceType.GOVERNED_PROJECT_IDENTITY
        )
        request_sources = next(
            item.source_ids
            for item in project.evidence
            if item.evidence_type == EvidenceType.GOVERNED_REQUEST
        )
        if (
            project.source_row.source_id != GOVERNED_SOURCE_ID
            or identity_sources != [GOVERNED_SOURCE_ID]
            or request_sources != [GOVERNED_SOURCE_ID]
        ):
            violations.append(
                ValidationViolation(
                    "GOVERNED_SOURCE_MISMATCH",
                    f"catalog.json:projects.{project.project_id}",
                    "governed identity/request facts must resolve only to the governed memorandum",
                )
            )

    transformations = {
        item.layer_id: item for item in map_context.source_crs_and_transformations
    }
    for feature in map_context.features:
        props = feature.properties
        source = manifest_source_models.get(props.source_id)
        path = f"map-context.geojson:features.{feature.id}"
        if source is not None and (
            props.historical_fit != source.historical_fit
            or props.source_vintage != source.source_vintage
        ):
            violations.append(
                ValidationViolation(
                    "MAP_PROVENANCE_MISMATCH",
                    path,
                    "map feature vintage/historical fit differs from its referenced source",
                )
            )
        layer_transform = transformations[props.layer_id]
        if (
            props.transformation_version != layer_transform.transformation_version
            or props.transformation_version != manifest.transformation_versions.geometry
        ):
            violations.append(
                ValidationViolation(
                    "TRANSFORMATION_VERSION_MISMATCH",
                    path,
                    "map feature transformation must match layer and manifest geometry versions",
                )
            )
        if props.layer_id == "rna_current_project_display" and props.source_id != RNA_SOURCE_ID:
            violations.append(
                ValidationViolation(
                    "MAP_SOURCE_MISMATCH",
                    path,
                    "RNA display geometry must resolve to the approved RNA layer-8 snapshot",
                )
            )

    benchmark_identity = benchmark.benchmark_identity
    manifest_benchmark = manifest.benchmark_identity
    if (
        benchmark_identity.source_id != manifest_benchmark.source_id
        or benchmark_identity.published_title != manifest_benchmark.published_title
        or benchmark_identity.published_date != manifest_benchmark.published_date
        or benchmark_identity.extraction_version != manifest_benchmark.extraction_version
    ):
        violations.append(
            ValidationViolation(
                "BENCHMARK_IDENTITY_MISMATCH",
                "benchmark.json:benchmark_identity",
                "benchmark identity differs from manifest",
            )
        )
    benchmark_source = benchmark.source_references.get(benchmark_identity.source_id)
    if benchmark_source and benchmark_identity.source_snapshot_sha256 != benchmark_source.sha256:
        violations.append(
            ValidationViolation(
                "BENCHMARK_SOURCE_MISMATCH",
                "benchmark.json:benchmark_identity.source_snapshot_sha256",
                "benchmark snapshot checksum differs from its registered source",
            )
        )

    benchmark_source_id = benchmark_identity.source_id
    if benchmark_source_id in _source_ids_from_catalog(catalog):
        violations.append(
            ValidationViolation(
                "BENCHMARK_LEAKAGE",
                "catalog.json",
                "benchmark source identity cannot enter the core catalog path",
            )
        )
    if benchmark_source_id in _source_ids_from_map(map_context):
        violations.append(
            ValidationViolation(
                "BENCHMARK_LEAKAGE",
                "map-context.geojson",
                "benchmark source identity cannot enter the map path",
            )
        )

    catalog_projects = {project.project_id: project for project in catalog.projects}
    available_geometry_ids = {
        project.project_id
        for project in catalog.projects
        if project.geography_status == "DISPLAY_GEOMETRY_AVAILABLE"
    }
    rna_feature_ids = {
        feature.properties.project_id
        for feature in map_context.features
        if feature.properties.layer_id == "rna_current_project_display"
    }
    if rna_feature_ids != available_geometry_ids:
        violations.append(
            ValidationViolation(
                "CATALOG_MAP_COVERAGE_MISMATCH",
                "catalog.json|map-context.geojson",
                "RNA project features must exactly match catalog AVAILABLE geometry states",
            )
        )
    map_project_ids = {
        feature.properties.project_id
        for feature in map_context.features
        if feature.properties.project_id is not None
    }
    unknown_map_ids = sorted(map_project_ids - set(catalog_projects))
    if unknown_map_ids:
        violations.append(
            ValidationViolation(
                "UNKNOWN_MAP_PROJECT",
                "map-context.geojson:features",
                f"map refers to projects outside the governed catalog: {unknown_map_ids}",
            )
        )
    if CITYWIDE_PROJECT_ID in map_project_ids:
        violations.append(
            ValidationViolation(
                "CITYWIDE_GEOMETRY_FORBIDDEN",
                "map-context.geojson:features",
                "5789.150 cannot have a map feature",
            )
        )

    unknown_benchmark_project_ids = sorted(
        {
            entry.governed_project_id
            for entry in benchmark.published_project_treatments
            if entry.governed_project_id is not None
        }
        - set(catalog_projects)
    )
    if unknown_benchmark_project_ids:
        violations.append(
            ValidationViolation(
                "BENCHMARK_GOVERNED_ID_UNKNOWN",
                "benchmark.json:published_project_treatments",
                "benchmark governed-overlap IDs must exist in the authoritative catalog",
            )
        )
    family_from_catalog = sorted(
        project.project_id for project in catalog.projects if project.p0_family.member
    )
    if family_from_catalog != list(ACTIVE_FAMILY_PROJECT_IDS):
        violations.append(
            ValidationViolation(
                "FAMILY_RECONCILIATION_FAILED",
                "catalog.json:projects",
                "family membership differs from the locked geometry-independent family",
            )
        )

    declared_coverage = {
        (entry.evidence_type, entry.evidence_role, entry.scope): entry
        for entry in manifest.evidence_coverage_missingness
    }
    for scope, projects in (
        ("GOVERNED_UNIVERSE", catalog.projects),
        (
            "ACTIVE_FAMILY",
            [project for project in catalog.projects if project.p0_family.member],
        ),
    ):
        for evidence_type in EvidenceType:
            items = [
                next(item for item in project.evidence if item.evidence_type == evidence_type)
                for project in projects
            ]
            roles = {item.evidence_role for item in items}
            if len(roles) != 1:
                violations.append(
                    ValidationViolation(
                        "EVIDENCE_ROLE_MISMATCH",
                        f"catalog.json:projects.{evidence_type.value}",
                        "one evidence type must retain one analytical role within a scope",
                    )
                )
                continue
            role = next(iter(roles))
            declaration = declared_coverage.get((evidence_type.value, role, scope))
            if declaration is None:
                violations.append(
                    ValidationViolation(
                        "EVIDENCE_COVERAGE_MISSING",
                        "manifest.json:evidence_coverage_missingness",
                        f"missing declaration for {evidence_type.value}/{role}/{scope}",
                    )
                )
                continue
            counts = Counter(item.availability for item in items)
            observed = {
                "available_count": counts[Availability.AVAILABLE],
                "missing_count": counts[Availability.MISSING],
                "unsupported_count": counts[Availability.UNSUPPORTED],
                "not_applicable_count": counts[Availability.NOT_APPLICABLE],
                "fixture_state_count": counts[Availability.NOT_EVALUATED_FIXTURE],
            }
            declared = {
                key: getattr(declaration, key)
                for key in observed
            }
            if observed != declared:
                violations.append(
                    ValidationViolation(
                        "EVIDENCE_COVERAGE_MISMATCH",
                        "manifest.json:evidence_coverage_missingness",
                        f"declared counts differ for {evidence_type.value}/{role}/{scope}",
                    )
                )
    return violations


def validate_bundle(
    bundle_directory: Path,
    *,
    manifest_sha256: str,
    expected_release_tier: ReleaseTier = ReleaseTier.REVIEWED_RELEASE,
) -> ValidatedBundle:
    """Validate exact bytes, schemas, identity, and locked cross-file semantics."""

    violations: list[ValidationViolation] = []
    if not re.fullmatch(r"[0-9a-f]{64}", manifest_sha256):
        raise BundleValidationError(
            [
                ValidationViolation(
                    "INVALID_EXTERNAL_MANIFEST_SHA256",
                    "manifest_sha256",
                    "external manifest checksum must be lowercase SHA-256",
                )
            ]
        )
    if bundle_directory.is_symlink() or not bundle_directory.is_dir():
        raise BundleValidationError(
            [ValidationViolation("INVALID_BUNDLE_DIRECTORY", str(bundle_directory), "not a directory")]
        )
    actual_names = {path.name for path in bundle_directory.iterdir()}
    if actual_names != RELEASE_ARTIFACT_FILENAMES:
        missing = sorted(RELEASE_ARTIFACT_FILENAMES - actual_names)
        extra = sorted(actual_names - RELEASE_ARTIFACT_FILENAMES)
        raise BundleValidationError(
            [
                ValidationViolation(
                    "INVALID_BUNDLE_FILE_SET",
                    str(bundle_directory),
                    f"fixed four-file set required; missing={missing}, extra={extra}",
                )
            ]
        )

    parsed: dict[str, tuple[bytes, Any, BaseModel]] = {}
    model_by_name: dict[str, type[BaseModel]] = {
        "manifest.json": ReleaseManifest,
        "catalog.json": CatalogArtifact,
        "map-context.geojson": MapContextArtifact,
        "benchmark.json": BenchmarkArtifact,
    }
    for name, model_type in model_by_name.items():
        try:
            parsed[name] = _read_artifact(bundle_directory / name, model_type)
        except (OSError, ValueError) as error:
            violations.append(ValidationViolation("ARTIFACT_INVALID", name, str(error)))
    if violations:
        raise BundleValidationError(violations)

    manifest_bytes, manifest_raw, manifest_model = parsed["manifest.json"]
    catalog_bytes, catalog_raw, catalog_model = parsed["catalog.json"]
    map_bytes, map_raw, map_model = parsed["map-context.geojson"]
    benchmark_bytes, benchmark_raw, benchmark_model = parsed["benchmark.json"]
    manifest = manifest_model
    catalog = catalog_model
    map_context = map_model
    benchmark = benchmark_model
    assert isinstance(manifest, ReleaseManifest)
    assert isinstance(catalog, CatalogArtifact)
    assert isinstance(map_context, MapContextArtifact)
    assert isinstance(benchmark, BenchmarkArtifact)

    actual_manifest_sha256 = hashlib.sha256(manifest_bytes).hexdigest()
    if actual_manifest_sha256 != manifest_sha256:
        violations.append(
            ValidationViolation(
                "MANIFEST_CHECKSUM_MISMATCH",
                "manifest.json",
                "exact manifest bytes do not match the external checksum",
            )
        )
    if manifest.release_tier != expected_release_tier:
        violations.append(
            ValidationViolation(
                "RELEASE_TIER_REJECTED",
                "manifest.json:release_tier",
                f"expected {expected_release_tier.value}, found {manifest.release_tier}",
            )
        )

    exact_artifacts = {
        "catalog.json": (catalog_bytes, manifest.artifacts.catalog_json),
        "map-context.geojson": (map_bytes, manifest.artifacts.map_context_geojson),
        "benchmark.json": (benchmark_bytes, manifest.artifacts.benchmark_json),
    }
    for name, (payload, expected) in exact_artifacts.items():
        if len(payload) != expected.byte_size:
            violations.append(
                ValidationViolation(
                    "ARTIFACT_SIZE_MISMATCH", name, "byte size differs from manifest"
                )
            )
        if hashlib.sha256(payload).hexdigest() != expected.sha256:
            violations.append(
                ValidationViolation(
                    "ARTIFACT_CHECKSUM_MISMATCH", name, "SHA-256 differs from manifest"
                )
            )

    violations.extend(
        _scan_forbidden_keys(
            manifest_raw,
            ANALYTICAL_FORBIDDEN_KEY_FRAGMENTS + MANIFEST_CIRCULAR_KEY_FRAGMENTS,
            "manifest.json",
        )
    )
    violations.extend(
        _scan_forbidden_keys(
            catalog_raw,
            ANALYTICAL_FORBIDDEN_KEY_FRAGMENTS + CATALOG_MAP_BENCHMARK_KEY_FRAGMENTS,
            "catalog.json",
        )
    )
    violations.extend(
        _scan_forbidden_keys(
            map_raw,
            ANALYTICAL_FORBIDDEN_KEY_FRAGMENTS
            + CATALOG_MAP_BENCHMARK_KEY_FRAGMENTS
            + ("p0family", "familymembership", "planmembership", "eligibility"),
            "map-context.geojson",
        )
    )
    violations.extend(
        _scan_forbidden_keys(
            benchmark_raw,
            ANALYTICAL_FORBIDDEN_KEY_FRAGMENTS + BENCHMARK_CORE_KEY_FRAGMENTS,
            "benchmark.json",
        )
    )

    if expected_release_tier == ReleaseTier.REVIEWED_RELEASE:
        for source in manifest.sources:
            if source.license_reuse_status == "UNVERIFIED":
                violations.append(
                    ValidationViolation(
                        "UNVERIFIED_SOURCE_REUSE",
                        f"manifest.json:sources.{source.source_id}",
                        "reviewed releases require completed source reuse/license review",
                    )
                )
        for name, raw in (
            ("manifest.json", manifest_raw),
            ("catalog.json", catalog_raw),
            ("map-context.geojson", map_raw),
            ("benchmark.json", benchmark_raw),
        ):
            for path, value in _walk_strings(raw):
                if "FIXTURE" in value.upper():
                    violations.append(
                        ValidationViolation(
                            "FIXTURE_MARKER_FORBIDDEN",
                            f"{name}:{path}",
                            "fixture state is forbidden in a reviewed release",
                        )
                    )

    violations.extend(_validate_registered_sources(manifest))
    violations.extend(
        _validate_cross_file_semantics(manifest, catalog, map_context, benchmark)
    )
    if violations:
        raise BundleValidationError(violations)
    return ValidatedBundle(
        manifest=manifest,
        catalog=catalog,
        map_context=map_context,
        benchmark=benchmark,
        manifest_sha256=actual_manifest_sha256,
    )
