"""Deterministic JSON Schema export for the versioned Python contracts."""

from __future__ import annotations

import json
from pathlib import Path
from pydantic import BaseModel

from .api import (
    ApiErrorEnvelope,
    ApiSuccessEnvelope,
    BenchmarkComparisonSuccessEnvelope,
    BenchmarkSuccessEnvelope,
    BootstrapSuccessEnvelope,
    GeminiExplainSuccessEnvelope,
    HealthSuccessEnvelope,
    PlanEvaluationSuccessEnvelope,
)
from .artifacts import BenchmarkArtifact, CatalogArtifact, MapContextArtifact, ReleaseManifest
from .cross_category import CrossCategoryUniverseArtifact
from .common import (
    EVIDENCE_TYPE_AVAILABILITY,
    EVIDENCE_TYPE_FACT_KINDS,
    EVIDENCE_TYPE_ROLES,
    EvidenceType,
)
from .gemini import GeminiExplainRequest, GeminiExplainResponse, GeminiGroundingPackage
from .plans import (
    EvaluatedPlan,
    BenchmarkComparisonRequest,
    BenchmarkComparisonResponseData,
    PlanEvaluationRequest,
    PlanEvaluationResponseData,
    PlanInput,
)
from .session import BrowserSessionState
from .versions import (
    ACTIVE_FAMILY_PROJECT_COUNT,
    ACTIVE_FAMILY_PROJECT_ID_SET,
    ACTIVE_FAMILY_PROJECT_IDS,
    ACTIVE_FAMILY_REQUEST_DOLLARS,
    GOVERNED_PROJECT_IDS,
    GOVERNED_PROJECT_COUNT,
)

SCHEMA_EXPORTS: tuple[tuple[str, type[BaseModel]], ...] = (
    ("cross-category-universe-1.0.0.schema.json", CrossCategoryUniverseArtifact),
    ("release-manifest-1.0.0.schema.json", ReleaseManifest),
    ("catalog-1.0.0.schema.json", CatalogArtifact),
    ("map-context-1.0.0.schema.json", MapContextArtifact),
    ("benchmark-1.0.0.schema.json", BenchmarkArtifact),
    ("funding-plan-input-1.0.0.schema.json", PlanInput),
    ("funding-plan-evaluation-request-1.0.0.schema.json", PlanEvaluationRequest),
    ("funding-plan-evaluated-result-1.0.0.schema.json", EvaluatedPlan),
    ("funding-plan-evaluation-response-1.0.0.schema.json", PlanEvaluationResponseData),
    ("benchmark-comparison-request-1.0.0.schema.json", BenchmarkComparisonRequest),
    ("benchmark-comparison-response-1.0.0.schema.json", BenchmarkComparisonResponseData),
    ("browser-session-1.0.0.schema.json", BrowserSessionState),
    ("api-success-envelope-v1.schema.json", ApiSuccessEnvelope),
    ("api-health-success-v1.schema.json", HealthSuccessEnvelope),
    ("api-bootstrap-success-v1.schema.json", BootstrapSuccessEnvelope),
    ("api-benchmark-success-v1.schema.json", BenchmarkSuccessEnvelope),
    ("api-plan-evaluation-success-v1.schema.json", PlanEvaluationSuccessEnvelope),
    ("api-benchmark-comparison-success-v1.schema.json", BenchmarkComparisonSuccessEnvelope),
    ("api-gemini-explain-success-v1.schema.json", GeminiExplainSuccessEnvelope),
    ("api-error-envelope-v1.schema.json", ApiErrorEnvelope),
    ("gemini-explain-request-1.0.0.schema.json", GeminiExplainRequest),
    ("gemini-explain-response-1.0.0.schema.json", GeminiExplainResponse),
    ("gemini-grounding-1.0.0.schema.json", GeminiGroundingPackage),
)


def _close_patterned_objects(value: object) -> None:
    """Make Pydantic key constraints fail closed in other JSON Schema consumers."""

    if isinstance(value, dict):
        if "patternProperties" in value:
            value.setdefault("additionalProperties", False)
        for child in value.values():
            _close_patterned_objects(child)
    elif isinstance(value, list):
        for child in value:
            _close_patterned_objects(child)


def _named_contracts(schema: dict, title: str) -> list[dict]:
    contracts = []
    if schema.get("title") == title:
        contracts.append(schema)
    definition = schema.get("$defs", {}).get(title)
    if definition is not None:
        contracts.append(definition)
    return contracts


def _exact_array(items: tuple[str, ...]) -> dict:
    return {
        "items": False,
        "maxItems": len(items),
        "minItems": len(items),
        "prefixItems": [{"const": item} for item in items],
        "uniqueItems": True,
    }


def _one_item_with(property_name: str, value: str) -> dict:
    return {
        "contains": {
            "properties": {property_name: {"const": value}},
            "required": [property_name],
            "type": "object",
        },
        "maxContains": 1,
        "minContains": 1,
    }


def _apply_m1_schema_constraints(schema: dict) -> None:
    """Add standard JSON Schema forms of M1 model-validator invariants."""

    unique_array_properties = {
        "PlanInput": ("project_ids",),
        "EvaluatedPlan": (
            "included_project_ids",
            "not_included_active_family_project_ids",
            "included_governed_requests",
        ),
        "MembershipDollarDelta": ("project_ids",),
        "BenchmarkOverlap": ("project_ids",),
        "PlanComparison": ("unchanged_project_ids",),
        "ReleaseManifest": ("approved_source_ids",),
        "CatalogArtifact": ("projects",),
    }
    for title, property_names in unique_array_properties.items():
        for contract in _named_contracts(schema, title):
            for property_name in property_names:
                contract["properties"][property_name]["uniqueItems"] = True

    for title, property_name in (
        ("ActiveFamilySummary", "project_ids"),
        ("GovernedReconciliations", "active_family_project_ids"),
    ):
        for contract in _named_contracts(schema, title):
            contract["properties"][property_name].update(
                _exact_array(ACTIVE_FAMILY_PROJECT_IDS)
            )

    for contract in _named_contracts(schema, "ProjectRecord"):
        contract["properties"]["project_id"] = {
            "enum": list(GOVERNED_PROJECT_IDS),
            "type": "string",
        }
        evidence = contract["properties"]["evidence"]
        evidence["allOf"] = [
            _one_item_with("evidence_type", evidence_type.value)
            for evidence_type in EvidenceType
        ]

    for contract in _named_contracts(schema, "CatalogArtifact"):
        projects = contract["properties"]["projects"]
        projects["allOf"] = []
        for project_id in GOVERNED_PROJECT_IDS:
            required_project = {
                "project_id": {"const": project_id},
                "p0_family": {
                    "properties": {
                        "member": {
                            "const": project_id in ACTIVE_FAMILY_PROJECT_ID_SET
                        }
                    },
                    "required": ["member"],
                    "type": "object",
                },
            }
            if project_id in ACTIVE_FAMILY_REQUEST_DOLLARS:
                required_project["governed_request_dollars"] = {
                    "const": ACTIVE_FAMILY_REQUEST_DOLLARS[project_id]
                }
            projects["allOf"].append(
                {
                    "contains": {
                        "properties": required_project,
                        "required": list(required_project),
                        "type": "object",
                    },
                    "maxContains": 1,
                    "minContains": 1,
                }
            )

    for contract in _named_contracts(schema, "IncludedGovernedRequest"):
        contract["properties"]["project_id"] = {
            "enum": list(ACTIVE_FAMILY_PROJECT_IDS),
            "type": "string",
        }
        contract["allOf"] = [
            {
                "if": {
                    "properties": {"project_id": {"const": project_id}},
                    "required": ["project_id"],
                },
                "then": {
                    "properties": {
                        "governed_request_dollars": {"const": request_dollars}
                    }
                },
            }
            for project_id, request_dollars in ACTIVE_FAMILY_REQUEST_DOLLARS.items()
        ]

    for title in ("EvaluatedPlan", "MembershipDollarDelta", "BenchmarkOverlap"):
        for contract in _named_contracts(schema, title):
            for property_name in (
                "included_project_ids",
                "not_included_active_family_project_ids",
                "project_ids",
            ):
                property_schema = contract.get("properties", {}).get(property_name)
                if property_schema is not None:
                    property_schema["items"] = {
                        "enum": list(ACTIVE_FAMILY_PROJECT_IDS),
                        "type": "string",
                    }
    for contract in _named_contracts(schema, "PlanComparison"):
        contract["properties"]["unchanged_project_ids"]["items"] = {
            "enum": list(ACTIVE_FAMILY_PROJECT_IDS),
            "type": "string",
        }

    evidence_branches = []
    for evidence_type in EvidenceType:
        expected_fact_kind = EVIDENCE_TYPE_FACT_KINDS.get(evidence_type)
        then_properties = {
            "availability": {
                "enum": sorted(
                    state.value for state in EVIDENCE_TYPE_AVAILABILITY[evidence_type]
                )
            },
            "evidence_role": {"const": EVIDENCE_TYPE_ROLES[evidence_type].value},
            "fact_kind": (
                {"const": expected_fact_kind.value}
                if expected_fact_kind is not None
                else {"type": "null"}
            ),
        }
        then = {"properties": then_properties}
        if expected_fact_kind is not None:
            then["required"] = ["fact_kind"]
        evidence_branches.append(
            {
                "if": {
                    "properties": {"evidence_type": {"const": evidence_type.value}},
                    "required": ["evidence_type"],
                },
                "then": then,
            }
        )
    evidence_branches.extend(
        (
            {
                "if": {
                    "properties": {"availability": {"const": "AVAILABLE"}},
                    "required": ["availability"],
                },
                "then": {
                    "properties": {
                        "reason_code": {"type": "null"},
                        "value": {"not": {"type": "null"}},
                    },
                    "required": ["value"],
                },
            },
            {
                "if": {
                    "properties": {
                        "availability": {
                            "enum": [
                                "MISSING",
                                "NOT_APPLICABLE",
                                "NOT_EVALUATED_FIXTURE",
                                "UNSUPPORTED",
                            ]
                        }
                    },
                    "required": ["availability"],
                },
                "then": {
                    "properties": {
                        "category": {"type": "null"},
                        "reason_code": {
                            "pattern": "^[A-Za-z0-9][A-Za-z0-9._:/-]{0,199}$",
                            "type": "string",
                        },
                        "unit": {"type": "null"},
                        "value": {"type": "null"},
                    },
                    "required": ["reason_code"],
                },
            },
        )
    )
    for contract in _named_contracts(schema, "EvidenceItem"):
        contract["allOf"] = evidence_branches

    coverage_branches = []
    for evidence_type in EvidenceType:
        coverage_branches.append(
            {
                "if": {
                    "properties": {"evidence_type": {"const": evidence_type.value}},
                    "required": ["evidence_type"],
                },
                "then": {
                    "properties": {
                        "evidence_role": {
                            "const": EVIDENCE_TYPE_ROLES[evidence_type].value
                        }
                    }
                },
            }
        )
    coverage_branches.extend(
        (
            {
                "if": {
                    "properties": {"scope": {"const": "GOVERNED_UNIVERSE"}},
                    "required": ["scope"],
                },
                "then": {
                    "properties": {
                        "denominator": {"const": GOVERNED_PROJECT_COUNT}
                    }
                },
            },
            {
                "if": {
                    "properties": {"scope": {"const": "ACTIVE_FAMILY"}},
                    "required": ["scope"],
                },
                "then": {
                    "properties": {
                        "denominator": {"const": ACTIVE_FAMILY_PROJECT_COUNT}
                    }
                },
            },
        )
    )
    for contract in _named_contracts(schema, "EvidenceCoverageMissingness"):
        contract["allOf"] = coverage_branches
    for contract in _named_contracts(schema, "ReleaseManifest"):
        coverage = contract["properties"]["evidence_coverage_missingness"]
        coverage["allOf"] = [
            {
                "contains": {
                    "properties": {
                        "evidence_type": {"const": evidence_type.value},
                        "scope": {"const": scope},
                    },
                    "required": ["evidence_type", "scope"],
                    "type": "object",
                },
                "maxContains": 1,
                "minContains": 1,
            }
            for evidence_type in EvidenceType
            for scope in ("GOVERNED_UNIVERSE", "ACTIVE_FAMILY")
        ]


def render_schema(filename: str, model: type[BaseModel]) -> bytes:
    schema = model.model_json_schema(mode="validation", by_alias=True)
    _close_patterned_objects(schema)
    _apply_m1_schema_constraints(schema)
    if "oneOf" in schema and "additionalProperties" not in schema:
        schema["unevaluatedProperties"] = False
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    schema["$id"] = f"https://climatecapital.ai/contracts/schemas/{filename}"
    return (
        json.dumps(schema, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def export_schemas(output_dir: Path, *, check: bool = False) -> list[Path]:
    expected_names = {filename for filename, _ in SCHEMA_EXPORTS}
    existing_names = (
        {path.name for path in output_dir.glob("*.schema.json")}
        if output_dir.exists()
        else set()
    )
    if check and existing_names != expected_names:
        missing = sorted(expected_names - existing_names)
        extra = sorted(existing_names - expected_names)
        raise ValueError(f"schema file set mismatch; missing={missing}, extra={extra}")

    if not check:
        output_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for filename, model in SCHEMA_EXPORTS:
        path = output_dir / filename
        expected = render_schema(filename, model)
        if check:
            if not path.is_file() or path.read_bytes() != expected:
                raise ValueError(f"generated schema is stale: {path}")
        else:
            if path.exists() and path.read_bytes() != expected:
                path.write_bytes(expected)
            elif not path.exists():
                path.write_bytes(expected)
            written.append(path)
    return written
