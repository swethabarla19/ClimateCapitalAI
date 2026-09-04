"""Single source of truth for the initial P0 contract identifiers."""

from types import MappingProxyType

RELEASE_MANIFEST_CONTRACT_VERSION = "p0-release-manifest/1.0.0"
CATALOG_CONTRACT_VERSION = "p0-catalog/1.0.0"
MAP_CONTEXT_CONTRACT_VERSION = "p0-map-context/1.0.0"
BENCHMARK_CONTRACT_VERSION = "p0-benchmark/1.0.0"
FUNDING_PLAN_CONTRACT_VERSION = "p0-funding-plan/1.0.0"
BROWSER_SESSION_CONTRACT_VERSION = "p0-browser-session/1.0.0"
GEMINI_EXPLAIN_CONTRACT_VERSION = "p0-gemini-explain/1.0.0"
CROSS_CATEGORY_UNIVERSE_CONTRACT_VERSION = "p0-cross-category-universe/1.0.0"

CROSS_CATEGORY_SOURCE_ROW_COUNT = 136
CROSS_CATEGORY_ANALYTICAL_PROJECT_COUNT = 106
CROSS_CATEGORY_PROGRAM_BUCKET_COUNT = 23
CROSS_CATEGORY_PROGRAM_ALLOCATION_COUNT = 4
CROSS_CATEGORY_NOT_SCORED_COUNT = 3
API_NAMESPACE = "/api/v1"

METHODOLOGY_VERSION = "p0-evidence-methodology/2026-09-01"

CONTRACT_VERSIONS = MappingProxyType(
    {
        "release_manifest": RELEASE_MANIFEST_CONTRACT_VERSION,
        "catalog": CATALOG_CONTRACT_VERSION,
        "map_context": MAP_CONTEXT_CONTRACT_VERSION,
        "benchmark": BENCHMARK_CONTRACT_VERSION,
        "funding_plan": FUNDING_PLAN_CONTRACT_VERSION,
        "browser_session": BROWSER_SESSION_CONTRACT_VERSION,
        "gemini_explain": GEMINI_EXPLAIN_CONTRACT_VERSION,
        "api_namespace": API_NAMESPACE,
    }
)

RELEASE_ARTIFACT_FILENAMES = frozenset(
    {"catalog.json", "map-context.geojson", "benchmark.json", "manifest.json"}
)

GOVERNED_PROJECT_COUNT = 37
GOVERNED_REQUEST_TOTAL_DOLLARS = 327_970_000
GOVERNED_SOURCE_SEMANTIC_SHA256 = (
    "c9091117734b2f793ed5f396dba3b8897169ad168659df0fe4f97cd92aeb072a"
)
GOVERNED_PROJECT_IDS = (
    "4015.001",
    "5282.043",
    "5282.133",
    "5282.134",
    "5282.150",
    "5282.162",
    "5754.089",
    "5754.139",
    "5754.145",
    "5754.147",
    "5754.149",
    "5789.075",
    "5789.107",
    "5789.121",
    "5789.126",
    "5789.127",
    "5789.136",
    "5789.139",
    "5789.141",
    "5789.150",
    "5789.145",
    "5789.146",
    "5848.053",
    "5848.070",
    "5848.071",
    "5848.087",
    "5848.091",
    "5848.092",
    "6039.109",
    "7492.011",
    "7492.032",
    "7492.045",
    "8598.014",
    "9999.235",
    "9999.236",
    "10878.010",
    "11889.004",
)
GOVERNED_PROJECT_ID_SET = frozenset(GOVERNED_PROJECT_IDS)
ACTIVE_FAMILY_PROJECT_IDS = (
    "5282.043",
    "5789.075",
    "5789.107",
    "5789.121",
    "5789.126",
    "5789.136",
    "5789.139",
    "5789.141",
    "5789.145",
    "5789.146",
    "5789.150",
    "8598.014",
)
ACTIVE_FAMILY_PROJECT_ID_SET = frozenset(ACTIVE_FAMILY_PROJECT_IDS)
ACTIVE_FAMILY_REQUEST_DOLLARS = MappingProxyType(
    {
        "5282.043": 8_500_000,
        "5789.075": 35_000_000,
        "5789.107": 16_750_000,
        "5789.121": 6_255_000,
        "5789.126": 21_250_000,
        "5789.136": 7_700_000,
        "5789.139": 11_250_000,
        "5789.141": 7_350_000,
        "5789.145": 20_000_000,
        "5789.146": 4_450_000,
        "5789.150": 3_000_000,
        "8598.014": 1_500_000,
    }
)
ACTIVE_FAMILY_PROJECT_COUNT = 12
ACTIVE_FAMILY_REQUEST_TOTAL_DOLLARS = 143_005_000
CITYWIDE_PROJECT_ID = "5789.150"
HISTORICAL_ENVELOPE_DOLLARS = 125_000_000
HISTORICAL_WATERSHED_ALLOCATION_DOLLARS = 160_000_000
HISTORICAL_BENCHMARK_SOURCE_ID = "austin_2026_bond_initial_draft_2026_01_21"
GOVERNED_SOURCE_ID = "austin_wpd_2026_bond_projects_2025_11_21"
RNA_SOURCE_ID = "austin_rna_projects_layer_8_live"
MAX_SCENARIO_BUDGET_DOLLARS = 1_000_000_000

APPROVED_MAP_LAYER_DEFAULTS = MappingProxyType(
    {
        "rna_current_project_display": True,
        "fema_current_hazard_context": False,
        "eaz_2021_context": False,
    }
)
