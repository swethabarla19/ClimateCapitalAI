"""Narrow technical objects for contract tests and the development fixture."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from climatecapital.contracts.artifacts import (
    BenchmarkArtifact,
    CatalogArtifact,
    MapContextArtifact,
    ReleaseManifest,
)
from climatecapital.contracts.common import EvidenceType, ReleaseTier
from climatecapital.contracts.versions import (
    ACTIVE_FAMILY_PROJECT_IDS,
    BENCHMARK_CONTRACT_VERSION,
    BROWSER_SESSION_CONTRACT_VERSION,
    CATALOG_CONTRACT_VERSION,
    FUNDING_PLAN_CONTRACT_VERSION,
    GEMINI_EXPLAIN_CONTRACT_VERSION,
    MAP_CONTEXT_CONTRACT_VERSION,
    METHODOLOGY_VERSION,
    RELEASE_MANIFEST_CONTRACT_VERSION,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
GOVERNED_CSV = (
    REPOSITORY_ROOT
    / "data/reconnaissance/city_austin/watershed_bond_projects/2025-11-21/projects.csv"
)

MEMO_SOURCE_ID = "austin_wpd_2026_bond_projects_2025_11_21"
RNA_SOURCE_ID = "austin_rna_projects_layer_8_live"
FEMA_SOURCE_ID = "austin_floodpro_fema_layer_8_live"
EAZ_SOURCE_ID = "austin_equity_analysis_zones_2021"
PROBLEM_SCORE_SOURCE_ID = "austin_wpd_problem_score_documentary_context"
BENCHMARK_SOURCE_ID = "austin_2026_bond_initial_draft_2026_01_21"
DATA_VERSION = "m2b-development-fixture-1"


# Exact derived-purpose facts from the locked all-37 methodology audit. These are
# governed fixture facts, not City taxonomy or eligibility labels.
PURPOSE_AUDIT = {
    "4015.001": ("Water/wastewater infrastructure", "Name", "HIGH", "No current RNA match"),
    "5282.043": (
        "Local flood/local drainage, mixed stormwater treatment",
        "Name + RNA description",
        "MEDIUM",
        "RNA describes hydrology, water quality, and flood benefit; not a pure drainage-only purpose",
    ),
    "5282.133": (
        "Stormwater treatment/water quality",
        "Name + RNA",
        "HIGH",
        "Green-infrastructure retrofit, not common local-flood severity",
    ),
    "5282.134": (
        "Stormwater treatment/water quality",
        "Name + RNA",
        "HIGH",
        "Treatment retrofit, not common local-flood severity",
    ),
    "5282.150": ("Stormwater treatment/water quality", "Name", "HIGH", "No current RNA match"),
    "5282.162": (
        "Stormwater treatment/water quality",
        "Name",
        "HIGH",
        "CAPEX program/control wording, no current RNA match",
    ),
    "5754.089": (
        "Low-water crossing/roadway flood safety",
        "Name + RNA",
        "HIGH",
        "Different safety/benefit mechanism from local drainage",
    ),
    "5754.139": (
        "Creek flood-risk reduction",
        "Name",
        "HIGH",
        "No current RNA match; not a local storm-drain project",
    ),
    "5754.145": (
        "Low-water crossing/roadway flood safety",
        "Name",
        "HIGH",
        "No current RNA match",
    ),
    "5754.147": (
        "Mixed flood-control channel/ecosystem restoration",
        "Name",
        "HIGH",
        "Mixed flood-control and ecological purpose",
    ),
    "5754.149": (
        "Low-water crossing/roadway flood safety",
        "Name",
        "HIGH",
        "No current RNA match",
    ),
    "5789.075": (
        "Local flood/local drainage",
        "Name + RNA description",
        "HIGH",
        "None material for purpose",
    ),
    "5789.107": (
        "Local flood/local drainage",
        "Name + RNA description",
        "HIGH",
        "Includes homes, streets, and low-water-crossing work within one local project",
    ),
    "5789.121": (
        "Local flood/local drainage",
        "Name + RNA description",
        "HIGH",
        "None material for purpose",
    ),
    "5789.126": (
        "Local flood/local drainage",
        "Name + RNA description",
        "HIGH",
        "None material for purpose",
    ),
    "5789.127": (
        "Water/wastewater infrastructure; identity/purpose unresolved",
        "Name + conflicting RNA name/description",
        "LOW",
        "Governed name says water/wastewater renewal; exact-ID RNA record says storm-drain improvements",
    ),
    "5789.136": ("Local flood/local drainage", "Name", "HIGH", "No current RNA match"),
    "5789.139": ("Local flood/local drainage", "Name", "HIGH", "No current RNA match"),
    "5789.141": ("Local flood/local drainage", "Name", "HIGH", "No current RNA match"),
    "5789.150": (
        "Local-drainage renewal program",
        "Name",
        "HIGH",
        "Citywide program is not a discrete project-level geography",
    ),
    "5789.145": ("Local flood/local drainage", "Name", "HIGH", "No current RNA match"),
    "5789.146": ("Local flood/local drainage", "Name", "HIGH", "No current RNA match"),
    "5848.053": (
        "Erosion/stream rehabilitation",
        "Name + RNA",
        "HIGH",
        "Different benefit mechanism from local drainage",
    ),
    "5848.070": ("Erosion/channel stabilization", "Name", "HIGH", "No current RNA match"),
    "5848.071": (
        "Erosion/stream restoration",
        "Name + RNA",
        "HIGH",
        "Different benefit mechanism from local drainage",
    ),
    "5848.087": ("Erosion protection", "Name", "HIGH", "No current RNA match"),
    "5848.091": ("Erosion/stream stabilization", "Name", "HIGH", "No current RNA match"),
    "5848.092": ("Erosion/stream stabilization", "Name", "HIGH", "No current RNA match"),
    "6039.109": (
        "Mixed/integrated drainage",
        "Name + RNA",
        "MEDIUM",
        "Integrated project may combine local, creek, and other drainage purposes",
    ),
    "7492.011": (
        "Dam/flood-control infrastructure",
        "Name + RNA",
        "HIGH",
        "Dam modernization is not comparable to local drainage",
    ),
    "7492.032": (
        "Dam/flood-control infrastructure",
        "Name + RNA",
        "HIGH",
        "Minor source-name variation: rehabilitation versus maintenance",
    ),
    "7492.045": ("Dam/flood-control infrastructure", "Name", "HIGH", "No current RNA match"),
    "8598.014": ("Local flood/local drainage", "Name", "HIGH", "No current RNA match"),
    "9999.235": (
        "Low-water crossing/roadway flood safety",
        "Name",
        "HIGH",
        "No current RNA match",
    ),
    "9999.236": (
        "Low-water crossing/roadway flood safety",
        "Name",
        "HIGH",
        "No current RNA match",
    ),
    "10878.010": (
        "Flood-control/tunnel infrastructure",
        "Name",
        "HIGH",
        "No current RNA match; not a local drainage project",
    ),
    "11889.004": (
        "Transportation/corridor infrastructure",
        "Name + RNA type/department",
        "MEDIUM",
        "Exact-ID RNA name differs materially from the governed corridor extent",
    ),
}


def canonical_bytes(value: Any) -> bytes:
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


def _source_references() -> dict[str, dict[str, Any]]:
    return {
        MEMO_SOURCE_ID: {
            "source_id": MEMO_SOURCE_ID,
            "publisher": "City of Austin - Watershed Protection Department",
            "title": "Austin Watershed Protection Potential 2026 Bond Projects",
            "source_url": "https://services.austintexas.gov/edims/document.cfm?id=463345",
            "source_vintage": "2025-11-21 planning snapshot",
            "published_date": "2025-11-21",
            "retrieval_timestamp": "2026-08-31T19:57:53Z",
            "sha256": "d1c2731cc12ecb3938569d29ec0c92d0966d7706af919e0a519b48329493d88e",
            "byte_size": 1_151_348,
            "gcs_object": {
                "uri": "gs://climatecapital-ai-raw-swetha/raw/city_austin/watershed_bond_projects/2025-11-21/source.pdf",
                "generation": "1788210198102506",
                "sha256": "d1c2731cc12ecb3938569d29ec0c92d0966d7706af919e0a519b48329493d88e",
                "byte_size": 1_151_348,
            },
            "historical_fit": "HISTORICALLY_VALID",
            "license_reuse_status": "UNVERIFIED",
            "attribution_text": "City of Austin source memorandum.",
            "known_limitations": ["Source presence does not establish analytical family membership."],
        },
        RNA_SOURCE_ID: {
            "source_id": RNA_SOURCE_ID,
            "publisher": "City of Austin",
            "title": "Austin RNA Projects - RNA Projects Layer 8",
            "source_url": "https://maps.austintexas.gov/arcgis/rest/services/LongRangeCIP/RNAProjects/MapServer/8",
            "source_vintage": "Live/current service; content vintage unknown",
            "published_date": None,
            "retrieval_timestamp": "2026-09-01T18:33:23Z",
            "sha256": "471dd527d9811ccd85cbfb9db71e6323b9ac28fa3746ad51bdcc97fbcb48bfd9",
            "byte_size": 32_774_832,
            "gcs_object": {
                "uri": "gs://climatecapital-ai-raw-swetha/raw/city_austin/rna_projects/layer_8/20260901T183323Z/features.arcgis.json",
                "generation": "1788287767379062",
                "sha256": "471dd527d9811ccd85cbfb9db71e6323b9ac28fa3746ad51bdcc97fbcb48bfd9",
                "byte_size": 32_774_832,
            },
            "historical_fit": "HISTORICAL_FIT_UNCERTAIN",
            "license_reuse_status": "UNVERIFIED",
            "attribution_text": "City of Austin current RNA Projects layer.",
            "known_limitations": ["Current display geometry does not establish January 2026 state."],
        },
        FEMA_SOURCE_ID: {
"source_id": FEMA_SOURCE_ID,
"publisher": "City of Austin",
"title": "FloodPro - FEMA Floodplain Layer 8",
"source_url": "https://maps.austintexas.gov/gis/rest/FloodPro/FloodPro/MapServer/8",
"source_vintage": "Live/current service; content vintage unknown",
"published_date": None,
"retrieval_timestamp": "2026-09-03T00:18:16Z",
"sha256": "e8d5760838454c74dd9752c3a6dd77663e3e61649a28bbf0e2c69471bcef090f",
"byte_size": 4_823,
"gcs_object": None,
"historical_fit": "HISTORICAL_FIT_UNCERTAIN",
"license_reuse_status": "UNVERIFIED",
"attribution_text": "City of Austin FloodPro FEMA Floodplain Layer 8.",
"known_limitations": [
"Identity is the immutable local snapshot manifest for the multipart acquisition.",
"Current FEMA context does not establish January 2026 state, project severity, benefit, eligibility, or priority.",
],
},
EAZ_SOURCE_ID: {
"source_id": EAZ_SOURCE_ID,
"publisher": "City of Austin",
"title": "Equity Analysis Zones 2021",
"source_url": "https://services.arcgis.com/0L95CJ0VTaxqcmED/arcgis/rest/services/Equity_Analysis_Zones_2021/FeatureServer/0",
"source_vintage": "2021 snapshot using 2019 ACS five-year inputs",
"published_date": None,
"retrieval_timestamp": "2026-09-03T00:36:45Z",
"sha256": "58e4dada99490044bb3fd782868429db06d6821eeb8aa0f626059992c3ab06be",
"byte_size": 764_207,
"gcs_object": None,
"historical_fit": "HISTORICALLY_VALID",
"license_reuse_status": "UNVERIFIED",
"attribution_text": "City of Austin Equity Analysis Zones 2021.",
"known_limitations": [
"Historically valid only as the dated 2021 contextual snapshot.",
"Project-level equity context requires defensible geography and is not a beneficiary or priority measure.",
],
},
PROBLEM_SCORE_SOURCE_ID: {
"source_id": PROBLEM_SCORE_SOURCE_ID,
"publisher": "City of Austin - Watershed Protection Department",
"title": "Watershed Problem Score Documentary Context",
"source_url": "https://services.austintexas.gov/edims/document.cfm?id=261630",
"source_vintage": "City documentary context from preserved methodology budget-response and related documents",
"published_date": None,
"retrieval_timestamp": "2026-09-03T00:40:43Z",
"sha256": "c2bd25d7a63f7fb4149b12e0aeb18706a1257f3346e96cc228f2d5ef0c821655",
"byte_size": 2_577,
"gcs_object": None,
"historical_fit": "HISTORICALLY_VALID",
"license_reuse_status": "UNVERIFIED",
"attribution_text": "City of Austin Watershed Problem Score documentary context.",
"known_limitations": [
"Identity is the immutable local snapshot manifest enumerating the three preserved documents.",
"Historically valid as documentary provenance only; association strength is not numeric Local Flood severity.",
],
},
BENCHMARK_SOURCE_ID: {
            "source_id": BENCHMARK_SOURCE_ID,
            "publisher": "City of Austin - Capital Delivery Services",
            "title": "2026 Bond Initial Draft Project Recommendation",
            "source_url": "https://services.austintexas.gov/edims/document.cfm?id=466344",
            "source_vintage": "2026-01-21 initial draft recommendation",
            "published_date": "2026-01-21",
            "retrieval_timestamp": "2026-08-31T19:57:54Z",
            "sha256": "da85a00273a32afb63f057e0e7f5065078f5e226d2e8c73a3efba69ee4bd0359",
            "byte_size": 412_820,
            "gcs_object": {
                "uri": "gs://climatecapital-ai-raw-swetha/raw/city_austin/initial_draft_recommendation/2026-01-21/source.pdf",
                "generation": "1788210202820922",
                "sha256": "da85a00273a32afb63f057e0e7f5065078f5e226d2e8c73a3efba69ee4bd0359",
                "byte_size": 412_820,
            },
            "historical_fit": "HISTORICALLY_VALID",
            "license_reuse_status": "UNVERIFIED",
            "attribution_text": "City of Austin historical recommendation source.",
            "known_limitations": ["Descriptive historical benchmark only."],
        },
    }


def _evidence_item(
    project_id: str,
    evidence_type: str,
    role: str,
    availability: str,
    *,
    value: Any = None,
    fact_kind: str | None = None,
    source_id: str = MEMO_SOURCE_ID,
    confidence: str | None = None,
    transformation_version: str | None = "development-fixture/1",
) -> dict[str, Any]:
    available = availability == "AVAILABLE"
    source = _source_references()[source_id]
    fixture_state = availability == "NOT_EVALUATED_FIXTURE"
    return {
        "evidence_id": f"{project_id}:{evidence_type.lower()}",
        "evidence_type": evidence_type,
        "evidence_role": role,
        "fact_kind": fact_kind,
        "availability": availability,
        "reason_code": (
            None
            if available
            else (
                f"fixture:{evidence_type.lower()}:not_evaluated"
                if fixture_state
                else f"{evidence_type.lower()}:not_available"
            )
        ),
        "explanation": (
            "Development-fixture curation has not evaluated this evidence item."
            if fixture_state
            else "Development fixture using governed or locked methodology state."
        ),
        "value": value if available else None,
        "unit": None,
        "category": None,
        "source_ids": [source_id],
        "source_vintage": source["source_vintage"],
        "historical_fit": source["historical_fit"],
        "association_method": None,
        "transformation_version": transformation_version,
        "coverage_scope": "Governed project record",
        "limitations": ["Development fixture; not a reviewed release artifact."],
        "confidence": confidence,
        "confidence_meaning": "Purpose classification strength only" if confidence else None,
        "public_label": evidence_type.replace("_", " ").title(),
        "public_disclaimer": "Use only within the locked analytical role.",
    }


def _project_evidence(
    project_id: str,
    request_dollars: int,
    family: bool,
    geography_status: str,
    purpose_label: str,
    purpose_confidence: str,
    release_tier: str,
) -> list[dict[str, Any]]:
    if geography_status == "DISPLAY_GEOMETRY_AVAILABLE":
        rna_availability, rna_value = "AVAILABLE", True
    elif geography_status == "DISPLAY_GEOMETRY_MISSING":
        rna_availability = (
            "NOT_EVALUATED_FIXTURE" if release_tier == "FIXTURE" else "MISSING"
        )
        rna_value = None
    else:
        rna_availability, rna_value = "NOT_APPLICABLE", None
    return [
        _evidence_item(
            project_id,
            "GOVERNED_PROJECT_IDENTITY",
            "FACT",
            "AVAILABLE",
            value=project_id,
            fact_kind="SOURCE_GOVERNED",
        ),
        _evidence_item(
            project_id,
            "GOVERNED_REQUEST",
            "FACT",
            "AVAILABLE",
            value=request_dollars,
            fact_kind="SOURCE_GOVERNED",
        ),
        _evidence_item(
            project_id,
            "DERIVED_PURPOSE",
            "FACT",
            "AVAILABLE",
            value=purpose_label,
            fact_kind="CLIMATE_CAPITAL_DERIVED",
            confidence=purpose_confidence,
            transformation_version="p0-purpose-classification/2026-09-01",
        ),
        _evidence_item(
            project_id,
            "P0_FAMILY",
            "FACT",
            "AVAILABLE",
            value=family,
            fact_kind="CLIMATE_CAPITAL_DERIVED",
            transformation_version="p0-purpose-classification/2026-09-01",
        ),
        _evidence_item(
            project_id,
            "PROBLEM_SCORE_ASSOCIATION",
            "CONTEXTUAL_EVIDENCE",
            "NOT_EVALUATED_FIXTURE",
            source_id=PROBLEM_SCORE_SOURCE_ID,
        ),
        _evidence_item(
            project_id,
            "RNA_DISPLAY_GEOMETRY_AVAILABILITY",
            "RESEARCH_ONLY_EVIDENCE",
            rna_availability,
            value=rna_value,
            source_id=RNA_SOURCE_ID,
        ),
        _evidence_item(
            project_id,
            "FEMA_CURRENT_HAZARD_CONTEXT",
            "CONTEXTUAL_EVIDENCE",
            "NOT_EVALUATED_FIXTURE",
            source_id=FEMA_SOURCE_ID,
        ),
        _evidence_item(
            project_id,
            "EAZ_2021_CONTEXT",
            "CONTEXTUAL_EVIDENCE",
            "NOT_EVALUATED_FIXTURE",
            source_id=EAZ_SOURCE_ID,
        ),
        _evidence_item(
            project_id,
            "EXPECTED_FLOOD_REDUCTION_BENEFIT",
            "UNAVAILABLE_UNSUPPORTED",
            "UNSUPPORTED",
            transformation_version=None,
        ),
        _evidence_item(
            project_id,
            "BENEFICIARY_ESTIMATES",
            "UNAVAILABLE_UNSUPPORTED",
            "UNSUPPORTED",
            transformation_version=None,
        ),
    ]


def build_catalog(
    *,
    release_tier: str = "FIXTURE",
    available_geometry_ids: set[str] | None = None,
) -> dict[str, Any]:
    if available_geometry_ids is None:
        available_geometry_ids = {"5282.043", "5754.089"}
    with GOVERNED_CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    projects: list[dict[str, Any]] = []
    family_ids = set(ACTIVE_FAMILY_PROJECT_IDS)
    for row in rows:
        project_id = row["subproject_id"]
        purpose_label, purpose_evidence, purpose_confidence, purpose_ambiguity = (
            PURPOSE_AUDIT[project_id]
        )
        family = project_id in family_ids
        if project_id == "5789.150":
            geography_status = "NON_PROJECT_GEOGRAPHY"
            program_scope = "CITYWIDE_PROGRAM"
        elif project_id in available_geometry_ids:
            geography_status = "DISPLAY_GEOMETRY_AVAILABLE"
            program_scope = "DISCRETE_PROJECT"
        else:
            geography_status = "DISPLAY_GEOMETRY_MISSING"
            program_scope = "DISCRETE_PROJECT"
        request = int(row["current_funding_request_estimate_dollars"])
        projects.append(
            {
                "project_id": project_id,
                "governed_name": row["project_name"],
                "governed_request_dollars": request,
                "governed_request_source_text": row["current_funding_request_estimate_source"],
                "source_row": {
                    "source_id": row["source_id"],
                    "source_pdf_page": int(row["source_pdf_page"]),
                    "source_table_row_order": int(row["source_table_row_order"]),
                    "map_label": row["map_label"],
                    "council_districts_source": row["council_districts_source"],
                },
                "purpose": {
                    "label": purpose_label,
                    "evidence_role": "FACT",
                    "fact_kind": "CLIMATE_CAPITAL_DERIVED",
                    "confidence": purpose_confidence,
                    "confidence_meaning": "Purpose classification strength only",
                    "evidence_summary": purpose_evidence,
                    "ambiguity_or_conflict": purpose_ambiguity,
                    "transformation_version": "p0-purpose-classification/2026-09-01",
                },
                "p0_family": {
                    "member": family,
                    "rationale": "Exact locked family membership from the Methodology Lock.",
                    "evidence_role": "FACT",
                    "fact_kind": "CLIMATE_CAPITAL_DERIVED",
                    "not_city_taxonomy_or_eligibility": True,
                    "geometry_is_not_membership_authority": True,
                },
                "geography_status": geography_status,
                "program_scope": program_scope,
                "evidence": _project_evidence(
                    project_id,
                    request,
                    family,
                    geography_status,
                    purpose_label,
                    purpose_confidence,
                    release_tier,
                ),
                "provenance_refs": [MEMO_SOURCE_ID],
            }
        )
    sources = _source_references()
    return {
        "contract_version": CATALOG_CONTRACT_VERSION,
        "data_version": DATA_VERSION,
        "release_tier": release_tier,
        "decision_context": {
            "historical_decision_snapshot_date": "2026-01-21",
            "historical_decision_snapshot_label": "Historical Decision Snapshot",
            "historical_envelope_dollars": 125_000_000,
            "historical_envelope_label": "Historical Envelope",
            "historical_watershed_allocation_dollars": 160_000_000,
            "historical_simulation": True,
            "not_official_funding_decision": True,
        },
        "governed_universe_summary": {
            "project_count": 37,
            "governed_request_total_dollars": 327_970_000,
        },
        "active_family_summary": {
            "project_ids": list(ACTIVE_FAMILY_PROJECT_IDS),
            "project_count": 12,
            "governed_request_total_dollars": 143_005_000,
            "provisional_climatecapital_derivation": True,
            "not_city_taxonomy_or_eligibility": True,
        },
        "source_references": {
            key: sources[key]
            for key in (
                MEMO_SOURCE_ID,
                RNA_SOURCE_ID,
                FEMA_SOURCE_ID,
                EAZ_SOURCE_ID,
                PROBLEM_SCORE_SOURCE_ID,
            )
        },
        "unsupported_metric_definitions": [
            {
                "metric_id": metric,
                "evidence_role": "UNAVAILABLE_UNSUPPORTED",
                "availability": "UNSUPPORTED",
                "reason_code": "locked_methodology:unsupported",
                "public_explanation": "The locked P0 methodology does not support this metric.",
            }
            for metric in (
                "EXPECTED_FLOOD_REDUCTION_BENEFIT",
                "PEOPLE_POTENTIALLY_BENEFITING",
                "STRUCTURES_BENEFITED",
            )
        ],
        "projects": projects,
        "methodology_version": METHODOLOGY_VERSION,
    }


def build_map(
    available_geometry_ids: set[str], *, release_tier: str = "FIXTURE"
) -> dict[str, Any]:
    features = []
    for index, project_id in enumerate(sorted(available_geometry_ids)):
        longitude = -97.8 + index * 0.01
        latitude = 30.2 + index * 0.01
        ring = [
            [longitude, latitude],
            [longitude + 0.001, latitude],
            [longitude + 0.001, latitude + 0.001],
            [longitude, latitude],
        ]
        feature_id = f"rna:{project_id}"
        features.append(
            {
                "type": "Feature",
                "id": feature_id,
                "properties": {
                    "feature_id": feature_id,
                    "source_feature_id": f"rna-source:{project_id}",
                    "layer_id": "rna_current_project_display",
                    "evidence_role": "RESEARCH_ONLY_EVIDENCE",
                    "availability": "AVAILABLE",
                    "source_id": RNA_SOURCE_ID,
                    "source_vintage": "Live/current service; content vintage unknown",
                    "historical_fit": "HISTORICAL_FIT_UNCERTAIN",
                    "transformation_version": "development-fixture-geometry/1",
                    "limitations": ["Technical geometry for contract validation only."],
                    "project_id": project_id,
                },
                "geometry": {"type": "Polygon", "coordinates": [ring]},
            }
        )
    return {
        "type": "FeatureCollection",
        "contract_version": MAP_CONTEXT_CONTRACT_VERSION,
        "data_version": DATA_VERSION,
        "release_tier": release_tier,
        "crs_contract": {
            "standard": "RFC_7946",
            "coordinate_reference_system": "EPSG:4326",
            "axis_order": "longitude_latitude",
        },
        "source_crs_and_transformations": [
            {
                "layer_id": layer_id,
                "source_crs": "Source-specific governed CRS",
                "transformation_tool": "Development-fixture serializer",
                "transformation_version": "development-fixture-geometry/1",
                "validation": "Finite RFC 7946 coordinates validated.",
                "limitations": ["Development fixture; not reviewed display geometry."],
            }
            for layer_id in (
                "rna_current_project_display",
                "fema_current_hazard_context",
                "eaz_2021_context",
            )
        ],
        "layer_definitions": [
            {
                "layer_id": "rna_current_project_display",
                "evidence_role": "RESEARCH_ONLY_EVIDENCE",
                "default_visible": True,
                "public_label": "Current RNA project display",
                "caveat": "Current research-only display geometry.",
            },
            {
                "layer_id": "fema_current_hazard_context",
                "evidence_role": "CONTEXTUAL_EVIDENCE",
                "default_visible": False,
                "public_label": "Current FEMA hazard context",
                "caveat": "Context only; not benefit evidence.",
            },
            {
                "layer_id": "eaz_2021_context",
                "evidence_role": "CONTEXTUAL_EVIDENCE",
                "default_visible": False,
                "public_label": "EAZ 2021 context",
                "caveat": "Dated location context only.",
            },
        ],
        "features": features,
    }


def build_benchmark(*, release_tier: str = "FIXTURE") -> dict[str, Any]:
    source = _source_references()[BENCHMARK_SOURCE_ID]
    return {
        "contract_version": BENCHMARK_CONTRACT_VERSION,
        "data_version": DATA_VERSION,
        "release_tier": release_tier,
        "benchmark_identity": {
            "source_id": BENCHMARK_SOURCE_ID,
            "published_title": "2026 Bond Initial Draft Project Recommendation",
            "published_date": "2026-01-21",
            "source_snapshot_sha256": source["sha256"],
            "extraction_version": "development-fixture-benchmark/1",
        },
        "source_references": {BENCHMARK_SOURCE_ID: source},
        "published_portfolio_summary": {
            "published_allocation": {
                "availability": "NOT_EVALUATED_FIXTURE",
                "unit": "USD",
                "reason_code": "benchmark:not_evaluated_fixture",
                "explanation": "Published allocation is not evaluated in this development fixture.",
            },
            "city_included_count": {
                "availability": "NOT_EVALUATED_FIXTURE",
                "reason_code": "benchmark:not_evaluated_fixture",
                "explanation": "Published included count is not evaluated in this development fixture.",
            },
            "explanation": "Benchmark extraction is not part of this development fixture.",
        },
        "published_project_treatments": [],
        "transformation_version": "development-fixture-benchmark/1",
        "limitations": ["Development fixture only; no benchmark treatment asserted."],
        "reconciliation": {
            "entry_count": 0,
            "available_amount_total_dollars": 0,
            "publication_reconciliation_passed": True,
            "explanation": "Zero technical entries reconcile; reviewed extraction is deferred.",
        },
    }


def _coverage(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for scope, projects in (
        ("GOVERNED_UNIVERSE", catalog["projects"]),
        ("ACTIVE_FAMILY", [p for p in catalog["projects"] if p["p0_family"]["member"]]),
    ):
        for evidence_type in EvidenceType:
            items = [
                next(item for item in project["evidence"] if item["evidence_type"] == evidence_type.value)
                for project in projects
            ]
            roles = {item["evidence_role"] for item in items}
            assert len(roles) == 1
            counts = Counter(item["availability"] for item in items)
            entries.append(
                {
                    "evidence_type": evidence_type.value,
                    "evidence_role": next(iter(roles)),
                    "scope": scope,
                    "denominator": len(projects),
                    "available_count": counts["AVAILABLE"],
                    "missing_count": counts["MISSING"],
                    "unsupported_count": counts["UNSUPPORTED"],
                    "not_applicable_count": counts["NOT_APPLICABLE"],
                    "fixture_state_count": counts["NOT_EVALUATED_FIXTURE"],
                }
            )
    return entries


def _write(path: Path, value: dict[str, Any]) -> bytes:
    payload = canonical_bytes(value)
    path.write_bytes(payload)
    return payload


def build_bundle(
    directory: Path,
    *,
    release_tier: str = "FIXTURE",
    available_geometry_ids: set[str] | None = None,
) -> tuple[dict[str, Any], str]:
    if available_geometry_ids is None:
        available_geometry_ids = {"5282.043", "5754.089"}
    catalog = build_catalog(
        release_tier=release_tier, available_geometry_ids=available_geometry_ids
    )
    map_context = build_map(available_geometry_ids, release_tier=release_tier)
    benchmark = build_benchmark(release_tier=release_tier)
    CatalogArtifact.model_validate_json(canonical_bytes(catalog), strict=True)
    MapContextArtifact.model_validate_json(canonical_bytes(map_context), strict=True)
    BenchmarkArtifact.model_validate_json(canonical_bytes(benchmark), strict=True)

    directory.mkdir(parents=True, exist_ok=True)
    payloads = {
        "catalog.json": _write(directory / "catalog.json", catalog),
        "map-context.geojson": _write(directory / "map-context.geojson", map_context),
        "benchmark.json": _write(directory / "benchmark.json", benchmark),
    }
    sources = _source_references()
    approved_source_ids = sorted(sources)
    manifest = {
        "contract_version": RELEASE_MANIFEST_CONTRACT_VERSION,
        "data_version": DATA_VERSION,
        "release_tier": release_tier,
        "contract_versions": {
            "catalog": CATALOG_CONTRACT_VERSION,
            "map_context": MAP_CONTEXT_CONTRACT_VERSION,
            "benchmark": BENCHMARK_CONTRACT_VERSION,
            "funding_plan": FUNDING_PLAN_CONTRACT_VERSION,
            "browser_session": BROWSER_SESSION_CONTRACT_VERSION,
            "gemini_explain": GEMINI_EXPLAIN_CONTRACT_VERSION,
        },
        "approved_source_ids": approved_source_ids,
        "sources": [sources[source_id] for source_id in approved_source_ids],
        "transformation_versions": {
            "extractor": "development-fixture/1",
            "join": "development-fixture/1",
            "geometry": "development-fixture-geometry/1",
            "classification": "p0-purpose-classification/2026-09-01",
            "serializer": "canonical-json/1",
        },
        "artifacts": {
            name: {"sha256": hashlib.sha256(payload).hexdigest(), "byte_size": len(payload)}
            for name, payload in payloads.items()
        },
        "governed_reconciliations": {
            "governed_project_count": 37,
            "governed_unique_project_id_count": 37,
            "governed_request_total_dollars": 327_970_000,
            "governed_source_semantic_sha256": "c9091117734b2f793ed5f396dba3b8897169ad168659df0fe4f97cd92aeb072a",
            "active_family_project_ids": list(ACTIVE_FAMILY_PROJECT_IDS),
            "active_family_project_count": 12,
            "active_family_request_total_dollars": 143_005_000,
            "whole_dollar_requests": True,
            "active_family_ids_in_governed_universe": True,
            "citywide_non_project_geography_without_feature": True,
            "catalog_map_project_id_coverage_agrees": True,
            "catalog_and_map_contain_no_benchmark_fields": True,
        },
        "evidence_coverage_missingness": _coverage(catalog),
        "benchmark_identity": {
            "source_id": BENCHMARK_SOURCE_ID,
            "published_title": benchmark["benchmark_identity"]["published_title"],
            "published_date": benchmark["benchmark_identity"]["published_date"],
            "extraction_version": benchmark["benchmark_identity"]["extraction_version"],
            "benchmark_contract_version": BENCHMARK_CONTRACT_VERSION,
            "artifact_sha256": hashlib.sha256(payloads["benchmark.json"]).hexdigest(),
        },
    }
    ReleaseManifest.model_validate_json(canonical_bytes(manifest), strict=True)
    manifest_payload = _write(directory / "manifest.json", manifest)
    return manifest, hashlib.sha256(manifest_payload).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def rewrite_artifacts_and_manifest(
    directory: Path,
    *,
    catalog: dict[str, Any] | None = None,
    map_context: dict[str, Any] | None = None,
    benchmark: dict[str, Any] | None = None,
    manifest: dict[str, Any] | None = None,
) -> str:
    values = {
        "catalog.json": catalog or load_json(directory / "catalog.json"),
        "map-context.geojson": map_context or load_json(directory / "map-context.geojson"),
        "benchmark.json": benchmark or load_json(directory / "benchmark.json"),
    }
    payloads = {name: _write(directory / name, value) for name, value in values.items()}
    manifest_value = manifest or load_json(directory / "manifest.json")
    for name, payload in payloads.items():
        manifest_value["artifacts"][name] = {
            "sha256": hashlib.sha256(payload).hexdigest(),
            "byte_size": len(payload),
        }
    manifest_value["benchmark_identity"]["artifact_sha256"] = hashlib.sha256(
        payloads["benchmark.json"]
    ).hexdigest()
    manifest_payload = _write(directory / "manifest.json", manifest_value)
    return hashlib.sha256(manifest_payload).hexdigest()
