/**
 * Frontend transport contracts for the activated cross-category runtime.
 *
 * The backend Pydantic models and generated JSON Schemas remain authoritative.
 * These types intentionally mirror only governed runtime fields consumed by the SPA.
 */

export const API_NAMESPACE = '/api/v1' as const
export const CATALOG_CONTRACT_VERSION =
  'p0-cross-category-catalog/2.0.0' as const
export const MAP_CONTEXT_CONTRACT_VERSION =
  'p0-cross-category-map-context/3.0.0' as const
export const FUNDING_PLAN_CONTRACT_VERSION =
  'p0-cross-category-funding-plan/2.0.0' as const
export const BENCHMARK_CONTRACT_VERSION =
  'p0-cross-category-benchmark/2.0.0' as const

export type PresentationCategory =
  | 'Transportation'
  | 'Parks & Open Space'
  | 'Watershed'
  | 'Community Facilities'

export interface ResponseIdentity {
  request_id: string
  api_namespace: typeof API_NAMESPACE
  contract_version: string | null
  data_version: string
  release_id: string
}

export interface ApiErrorDetail {
  error_code: string
  message: string
  field_path: Array<string | number>
  retryable: boolean
}

export interface ApiErrorEnvelope {
  status: 'ERROR'
  identity: ResponseIdentity
  error: ApiErrorDetail
}

export interface OfficialPrbComponents {
  strategic_alignment: number
  critical_asset: number
  community_consideration: number
  efficiency: number
  timeliness_readiness: number
  climate_resilience: number
}

export type CouncilDistrictAssignmentType =
  | 'SINGLE_DISTRICT'
  | 'MULTI_DISTRICT'
  | 'CITYWIDE'
  | 'UNSPECIFIED'

export interface CouncilDistrictContext {
  assignment_type: CouncilDistrictAssignmentType
  districts: number[]
  source_value: string | null
  analyst_review_only: true
  hard_portfolio_constraint: false
}

export interface OmImpactContext {
  value: 'YES' | 'NO'
  analyst_review_only: true
  hard_portfolio_constraint: false
  additional_score_preference_authorized: false
}

export interface RuntimeProject {
  decision_unit_id: string
  canonical_project_id: string | null
  governed_name: string
  presentation_category: PresentationCategory
  source_department: string
  source_domain: string
  model_request_dollars: number
  model_request_authority: string
  model_request_authority_source_id: string
  request_version_conflict: boolean
  funding_priority_score: number
  funding_priority_rank: number
  is_tied: boolean
  tie_group_size: number
  display_order_within_tie: number
  display_tiebreak_has_analytical_meaning: false
  prb_components: OfficialPrbComponents
  council_district: CouncilDistrictContext
  om_impact: OmImpactContext
  provenance_refs: string[]
}

export interface RuntimeCategoryCounts {
  transportation: number
  parks_open_space: number
  watershed: number
  community_facilities: number
}

export interface RuntimeCatalog {
  contract_version: typeof CATALOG_CONTRACT_VERSION
  data_version: string
  historical_decision_snapshot_date: '2026-01-21'
  model_scope: 'CROSS_CATEGORY_PRB_PROJECT_MODEL'
  methodology_name:
    'PRIORITY_CONSTRAINED_ANALYST_GOVERNED_PORTFOLIO_CONSTRUCTION'
  cross_category_ranking_authorized: true
  portfolio_selection_authorized: true
  runtime_integration_authorized: boolean
  project_count: number
  governed_request_total_dollars: number
  category_counts: RuntimeCategoryCounts
  unique_funding_priority_score_count: number
  tied_score_group_count: number
  projects_in_tied_score_groups: number
  projects: RuntimeProject[]
}

export type RuntimeMapDisplayRole =
  | 'PROJECT_DISPLAY_POINT'
  | 'PROJECT_SITE'
  | 'PROJECT_PARCEL'
  | 'PARK_SITE_CONTEXT'
  | 'FACILITY_SITE_CONTEXT'

export interface RuntimeMapFeatureProperties {
  decision_unit_id: string
  governed_name: string
  presentation_category: PresentationCategory
  display_role: RuntimeMapDisplayRole
  geometry_type: 'point' | 'polygon'
  geometry_origin: 'SOURCE_NATIVE_FEATURE'
  confidence: 'HIGH'
  governance_decision_id: 'D-116'
  caveats: string[]
  historical_fit_class: string
  historical_fit_judgment: string
  source_agency: string
  source_title: string
  source_feature_id: string
  source_url: string
  [key: string]: unknown
}

export type RuntimeMapGeometry =
  | {
      type: 'Point'
      coordinates: [number, number]
    }
  | {
      type: 'Polygon'
      coordinates: number[][][]
    }
  | {
      type: 'MultiPolygon'
      coordinates: number[][][][]
    }

export interface RuntimeMapFeature {
  type: 'Feature'
  id: string
  geometry: RuntimeMapGeometry
  properties: RuntimeMapFeatureProperties
}

export interface RuntimeMapContext {
  type: 'FeatureCollection'
  contract_version: typeof MAP_CONTEXT_CONTRACT_VERSION
  data_version: string
  historical_decision_snapshot_date: '2026-01-21'
  project_identity_key: 'decision_unit_id'
  geometry_authority: 'GOVERNED_RUNTIME_GEOMETRY_ONLY'
  mapping_status: 'PARTIAL_GOVERNED_RUNTIME_GEOMETRY_AVAILABLE'
  analytical_project_count: number
  mapped_project_count: number
  unmapped_project_count: number
  geometry_required_for_model_eligibility: false
  geometry_required_for_portfolio_selection: false
  fabricated_geometry: false
  derived_geocoded_geometry: false
  inferred_or_centroid_geometry: false
  crs_contract: 'RFC_7946_EPSG_4326'
  governance_decision_id: 'D-116'
  governance_reconciliation_sha256: string
  candidate_geometry_snapshot_sha256: string
  limitations: string[]
  features: RuntimeMapFeature[]
}

export interface PublicConfiguration {
  environment_label: string
  osm_tile_url: string
  osm_attribution: string
  fixture_mode: boolean
}

export interface BootstrapSuccessEnvelope {
  endpoint: '/api/v1/bootstrap'
  status: 'SUCCESS'
  identity: ResponseIdentity
  data: {
    catalog: RuntimeCatalog
    map_context: RuntimeMapContext
    public_configuration: PublicConfiguration
  }
}

export interface BoundaryResolutionInput {
  funding_priority_score: number
  funding_priority_rank: number
  selected_decision_unit_ids: string[]
  advance_with_feasible_same_tier_project_acknowledged: boolean
}

export interface FundingPlanInput {
  contract_version: typeof FUNDING_PLAN_CONTRACT_VERSION
  data_version: string
  available_budget_dollars: number
  boundary_resolutions: BoundaryResolutionInput[]
  expected_fingerprint: string | null
}

export type PortfolioEvaluationStatus =
  | 'COMPLETE'
  | 'ANALYST_RESOLUTION_REQUIRED'

export type SelectionSource =
  | 'AUTO_COMPLETE_TIER'
  | 'AUTO_UNIQUE_BUDGET_FEASIBLE'
  | 'ANALYST_BOUNDARY_RESOLUTION'

export interface SelectedProjectResult {
  decision_unit_id: string
  model_request_dollars: number
  funding_priority_score: number
  funding_priority_rank: number
  selection_source: SelectionSource
}

export interface BoundaryCandidateResult {
  decision_unit_id: string
  model_request_dollars: number
  funding_priority_score: number
  funding_priority_rank: number
  individually_budget_feasible: boolean
}

export interface BoundaryTierResult {
  funding_priority_score: number
  funding_priority_rank: number
  remaining_budget_before_tier_dollars: number
  full_tier_request_dollars: number
  candidates: BoundaryCandidateResult[]
}

export interface PortfolioWarning {
  warning_code: 'HIGHER_PRIORITY_FEASIBLE_PROJECT_REMAINS'
  message: string
  decision_unit_ids: string[]
}

export interface AppliedAnalystOverride {
  funding_priority_score: number
  funding_priority_rank: number
  acknowledged: true
  decision_unit_ids_left_feasible: string[]
}

export interface FundingPlanResult {
  contract_version: typeof FUNDING_PLAN_CONTRACT_VERSION
  data_version: string
  status: PortfolioEvaluationStatus
  available_budget_dollars: number
  selected_projects: SelectedProjectResult[]
  included_total_dollars: number
  remainder_dollars: number
  unresolved_boundary: BoundaryTierResult | null
  warnings: PortfolioWarning[]
  applied_analyst_overrides: AppliedAnalystOverride[]
  plan_fingerprint: string
}

export interface FundingPlanSuccessEnvelope {
  endpoint: '/api/v1/plans/evaluate'
  status: 'SUCCESS'
  identity: ResponseIdentity
  data: FundingPlanResult
}

export interface BenchmarkCategorySummary {
  presentation_category: PresentationCategory
  analytical_project_count: number
  historically_recommended_project_count: number
  recommendation_total_dollars: number
}

export interface BenchmarkProjectOutcome {
  decision_unit_id: string
  canonical_project_id: string | null
  governed_name: string
  presentation_category: PresentationCategory
  historically_recommended: boolean
  january_recommendation_dollars: number | null
  source_conflict_flag: boolean
  request_version_conflict: boolean
  outcome_role: 'BENCHMARK_OUTCOME_ONLY'
}

export interface HistoricalBenchmark {
  contract_version: typeof BENCHMARK_CONTRACT_VERSION
  data_version: string
  historical_decision_snapshot_date: '2026-01-21'
  source_id: string
  source_snapshot_sha256: string
  outcome_role: 'BENCHMARK_OUTCOME_ONLY'
  analytical_project_count: number
  full_initial_recommendation_dollars: number
  matched_analytical_cohort_dollars: number
  outside_analytical_cohort_dollars: number
  historically_recommended_project_count: number
  ranking_input: false
  portfolio_selection_input: false
  category_summaries: BenchmarkCategorySummary[]
  project_outcomes: BenchmarkProjectOutcome[]
  limitations: string[]
}

export interface HistoricalBenchmarkSuccessEnvelope {
  endpoint: '/api/v1/benchmark'
  status: 'SUCCESS'
  identity: ResponseIdentity
  data: {
    benchmark: HistoricalBenchmark
  }
}
