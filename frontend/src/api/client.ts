import {
  API_NAMESPACE,
  BENCHMARK_CONTRACT_VERSION,
  CATALOG_CONTRACT_VERSION,
  FUNDING_PLAN_CONTRACT_VERSION,
  MAP_CONTEXT_CONTRACT_VERSION,
  type ApiErrorEnvelope,
  type BootstrapSuccessEnvelope,
  type FundingPlanInput,
  type FundingPlanSuccessEnvelope,
  type HistoricalBenchmarkSuccessEnvelope,
  type OfficialPrbComponents,
  type ResponseIdentity,
  type RuntimeMapFeature,
} from './contracts'

export type ApiClientErrorKind =
  | 'API_ERROR'
  | 'NETWORK_ERROR'
  | 'UNEXPECTED_PAYLOAD'
  | 'REQUEST_ABORTED'

interface ApiClientErrorOptions {
  kind: ApiClientErrorKind
  status?: number | null
  errorCode?: string | null
  fieldPath?: Array<string | number>
  retryable?: boolean
  identity?: ResponseIdentity | null
  cause?: unknown
}

export class ApiClientError extends Error {
  readonly kind: ApiClientErrorKind
  readonly status: number | null
  readonly errorCode: string | null
  readonly fieldPath: Array<string | number>
  readonly retryable: boolean
  readonly identity: ResponseIdentity | null

  constructor(message: string, options: ApiClientErrorOptions) {
    super(message, { cause: options.cause })
    this.name = 'ApiClientError'
    this.kind = options.kind
    this.status = options.status ?? null
    this.errorCode = options.errorCode ?? null
    this.fieldPath = [...(options.fieldPath ?? [])]
    this.retryable = options.retryable ?? false
    this.identity = options.identity ?? null
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function isStringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((entry) => typeof entry === 'string')
}

function isPath(value: unknown): value is Array<string | number> {
  return (
    Array.isArray(value) &&
    value.every(
      (entry) => typeof entry === 'string' || typeof entry === 'number',
    )
  )
}

function isFiniteNumber(value: unknown): value is number {
  return typeof value === 'number' && Number.isFinite(value)
}

function isSha256(value: unknown): value is string {
  return typeof value === 'string' && /^[0-9a-f]{64}$/.test(value)
}

function isGeoJsonPosition(value: unknown): value is [number, number] {
  return (
    Array.isArray(value) &&
    value.length === 2 &&
    isFiniteNumber(value[0]) &&
    isFiniteNumber(value[1]) &&
    value[0] >= -180 &&
    value[0] <= 180 &&
    value[1] >= -90 &&
    value[1] <= 90
  )
}

function isGeoJsonLinearRing(value: unknown): boolean {
  if (
    !Array.isArray(value) ||
    value.length < 4 ||
    !value.every(isGeoJsonPosition)
  ) {
    return false
  }

  const first = value[0]
  const last = value[value.length - 1]

  return first[0] === last[0] && first[1] === last[1]
}

function isGeoJsonPolygonCoordinates(value: unknown): boolean {
  return (
    Array.isArray(value) &&
    value.length > 0 &&
    value.every(isGeoJsonLinearRing)
  )
}

function validateRuntimeMapFeature(value: unknown): value is RuntimeMapFeature {
  if (
    !isRecord(value) ||
    value.type !== 'Feature' ||
    typeof value.id !== 'string' ||
    !isRecord(value.geometry) ||
    !isRecord(value.properties)
  ) {
    return false
  }

  const geometry = value.geometry
  const properties = value.properties

  const validGeometry =
    (geometry.type === 'Point' &&
      isGeoJsonPosition(geometry.coordinates)) ||
    (geometry.type === 'Polygon' &&
      isGeoJsonPolygonCoordinates(geometry.coordinates)) ||
    (geometry.type === 'MultiPolygon' &&
      Array.isArray(geometry.coordinates) &&
      geometry.coordinates.length > 0 &&
      geometry.coordinates.every(isGeoJsonPolygonCoordinates))

  const validDisplayRole =
    properties.display_role === 'PROJECT_DISPLAY_POINT' ||
    properties.display_role === 'PROJECT_SITE' ||
    properties.display_role === 'PROJECT_PARCEL' ||
    properties.display_role === 'PARK_SITE_CONTEXT' ||
    properties.display_role === 'FACILITY_SITE_CONTEXT'

  const validPresentationCategory =
    properties.presentation_category === 'Transportation' ||
    properties.presentation_category === 'Parks & Open Space' ||
    properties.presentation_category === 'Watershed' ||
    properties.presentation_category === 'Community Facilities'

  const expectedGeometryType =
    geometry.type === 'Point' ? 'point' : 'polygon'

  return (
    validGeometry &&
    validDisplayRole &&
    validPresentationCategory &&
    value.id.length > 0 &&
    typeof properties.decision_unit_id === 'string' &&
    properties.decision_unit_id.length > 0 &&
    properties.decision_unit_id === value.id &&
    typeof properties.governed_name === 'string' &&
    properties.governed_name.length > 0 &&
    properties.geometry_type === expectedGeometryType &&
    properties.geometry_origin === 'SOURCE_NATIVE_FEATURE' &&
    properties.confidence === 'HIGH' &&
    properties.governance_decision_id === 'D-116' &&
    Array.isArray(properties.caveats) &&
    properties.caveats.length > 0 &&
    properties.caveats.every(
      (entry) => typeof entry === 'string' && entry.length > 0,
    ) &&
    typeof properties.historical_fit_class === 'string' &&
    properties.historical_fit_class.length > 0 &&
    typeof properties.historical_fit_judgment === 'string' &&
    properties.historical_fit_judgment.length > 0 &&
    typeof properties.source_agency === 'string' &&
    properties.source_agency.length > 0 &&
    typeof properties.source_title === 'string' &&
    properties.source_title.length > 0 &&
    typeof properties.source_feature_id === 'string' &&
    properties.source_feature_id.length > 0 &&
    typeof properties.source_url === 'string' &&
    properties.source_url.length > 0
  )
}
function isWholeNumber(value: unknown): value is number {
  return isFiniteNumber(value) && Number.isInteger(value)
}

function isNonNegativeWholeNumber(value: unknown): value is number {
  return isWholeNumber(value) && value >= 0
}

function isPositiveWholeNumber(value: unknown): value is number {
  return isWholeNumber(value) && value > 0
}

function isHalfPoint(value: unknown, minimum: number, maximum: number): value is number {
  return (
    isFiniteNumber(value) &&
    value >= minimum &&
    value <= maximum &&
    Number.isInteger(value * 2)
  )
}

function malformed(message: string, status: number | null = 200): never {
  throw new ApiClientError(message, {
    kind: 'UNEXPECTED_PAYLOAD',
    status,
    errorCode: 'UNEXPECTED_PAYLOAD',
  })
}

function parseIdentity(value: unknown, status: number): ResponseIdentity {
  if (!isRecord(value)) {
    return malformed('API response identity was missing.', status)
  }

  if (
    typeof value.request_id !== 'string' ||
    value.api_namespace !== API_NAMESPACE ||
    !(
      typeof value.contract_version === 'string' ||
      value.contract_version === null
    ) ||
    typeof value.data_version !== 'string' ||
    typeof value.release_id !== 'string'
  ) {
    return malformed('API response identity was malformed.', status)
  }

  return value as unknown as ResponseIdentity
}

function parseErrorEnvelope(
  payload: unknown,
  status: number,
): ApiErrorEnvelope | null {
  if (
    !isRecord(payload) ||
    payload.status !== 'ERROR' ||
    !isRecord(payload.error)
  ) {
    return null
  }

  const identity = parseIdentity(payload.identity, status)
  const error = payload.error

  if (
    typeof error.error_code !== 'string' ||
    typeof error.message !== 'string' ||
    !isPath(error.field_path) ||
    typeof error.retryable !== 'boolean'
  ) {
    return null
  }

  return {
    status: 'ERROR',
    identity,
    error: {
      error_code: error.error_code,
      message: error.message,
      field_path: [...error.field_path],
      retryable: error.retryable,
    },
  }
}

function requireCommonSuccessEnvelope(
  payload: unknown,
  endpoint: string,
  contractVersion: string,
  status: number,
): { identity: ResponseIdentity; data: Record<string, unknown> } {
  if (
    !isRecord(payload) ||
    payload.endpoint !== endpoint ||
    payload.status !== 'SUCCESS' ||
    !isRecord(payload.data)
  ) {
    return malformed('API success response contract was not recognized.', status)
  }

  const identity = parseIdentity(payload.identity, status)

  if (identity.contract_version !== contractVersion) {
    return malformed('API success response contract identity was malformed.', status)
  }

  return { identity, data: payload.data }
}

function validatePrbComponents(
  value: unknown,
): value is OfficialPrbComponents {
  return (
    isRecord(value) &&
    isFiniteNumber(value.strategic_alignment) &&
    isFiniteNumber(value.critical_asset) &&
    isFiniteNumber(value.community_consideration) &&
    isFiniteNumber(value.efficiency) &&
    isFiniteNumber(value.timeliness_readiness) &&
    isFiniteNumber(value.climate_resilience)
  )
}

function validateRuntimeProject(value: unknown): boolean {
  if (!isRecord(value)) return false

  const categoryValid = [
    'Transportation',
    'Parks & Open Space',
    'Watershed',
    'Community Facilities',
  ].includes(String(value.presentation_category))

  const councilDistrict = value.council_district
  const omImpact = value.om_impact
  const components = value.prb_components

  if (!validatePrbComponents(components)) return false

  const componentTotal = Object.values(components).reduce(
    (sum, component) => sum + component,
    0,
  )

  return (
    typeof value.decision_unit_id === 'string' &&
    (typeof value.canonical_project_id === 'string' ||
      value.canonical_project_id === null) &&
    typeof value.governed_name === 'string' &&
    categoryValid &&
    typeof value.source_department === 'string' &&
    typeof value.source_domain === 'string' &&
    isPositiveWholeNumber(value.model_request_dollars) &&
    typeof value.model_request_authority === 'string' &&
    typeof value.model_request_authority_source_id === 'string' &&
    typeof value.request_version_conflict === 'boolean' &&
    isHalfPoint(value.funding_priority_score, 0, 100) &&
    componentTotal === value.funding_priority_score &&
    isPositiveWholeNumber(value.funding_priority_rank) &&
    typeof value.is_tied === 'boolean' &&
    isWholeNumber(value.tie_group_size) &&
    isWholeNumber(value.display_order_within_tie) &&
    value.display_tiebreak_has_analytical_meaning === false &&
    isRecord(councilDistrict) &&
    typeof councilDistrict.assignment_type === 'string' &&
    Array.isArray(councilDistrict.districts) &&
    councilDistrict.districts.every(isWholeNumber) &&
    (typeof councilDistrict.source_value === 'string' ||
      councilDistrict.source_value === null) &&
    councilDistrict.analyst_review_only === true &&
    councilDistrict.hard_portfolio_constraint === false &&
    isRecord(omImpact) &&
    (omImpact.value === 'YES' || omImpact.value === 'NO') &&
    omImpact.analyst_review_only === true &&
    omImpact.hard_portfolio_constraint === false &&
    omImpact.additional_score_preference_authorized === false &&
    isStringArray(value.provenance_refs)
  )
}

export function parseBootstrap(
  payload: unknown,
  status = 200,
): BootstrapSuccessEnvelope {
  const { identity, data } = requireCommonSuccessEnvelope(
    payload,
    '/api/v1/bootstrap',
    CATALOG_CONTRACT_VERSION,
    status,
  )

  const catalog = data.catalog
  const mapContext = data.map_context
  const config = data.public_configuration

  if (!isRecord(catalog) || !isRecord(mapContext) || !isRecord(config)) {
    return malformed('Bootstrap response data was incomplete.', status)
  }

  const counts = catalog.category_counts
  const projects = catalog.projects

  if (
    catalog.contract_version !== CATALOG_CONTRACT_VERSION ||
    catalog.data_version !== identity.data_version ||
    catalog.historical_decision_snapshot_date !== '2026-01-21' ||
    catalog.model_scope !== 'CROSS_CATEGORY_PRB_PROJECT_MODEL' ||
    catalog.methodology_name !==
      'PRIORITY_CONSTRAINED_ANALYST_GOVERNED_PORTFOLIO_CONSTRUCTION' ||
    catalog.cross_category_ranking_authorized !== true ||
    catalog.portfolio_selection_authorized !== true ||
    catalog.runtime_integration_authorized !== true ||
    !isPositiveWholeNumber(catalog.project_count) ||
    !isPositiveWholeNumber(catalog.governed_request_total_dollars) ||
    !isRecord(counts) ||
    !isWholeNumber(counts.transportation) ||
    !isWholeNumber(counts.parks_open_space) ||
    !isWholeNumber(counts.watershed) ||
    !isWholeNumber(counts.community_facilities) ||
    !isWholeNumber(catalog.unique_funding_priority_score_count) ||
    !isWholeNumber(catalog.tied_score_group_count) ||
    !isWholeNumber(catalog.projects_in_tied_score_groups) ||
    !Array.isArray(projects) ||
    projects.length !== catalog.project_count ||
    !projects.every(validateRuntimeProject)
  ) {
    return malformed('Bootstrap catalog was malformed.', status)
  }

  const decisionUnitIds = projects.map((project) =>
    (project as Record<string, unknown>).decision_unit_id,
  )

  if (new Set(decisionUnitIds).size !== decisionUnitIds.length) {
    return malformed('Bootstrap catalog contained duplicate project identities.', status)
  }

  const categoryTotal =
    counts.transportation +
    counts.parks_open_space +
    counts.watershed +
    counts.community_facilities
  const requestTotal = projects.reduce(
    (sum, project) =>
      sum + Number((project as Record<string, unknown>).model_request_dollars),
    0,
  )

  if (
    categoryTotal !== catalog.project_count ||
    requestTotal !== catalog.governed_request_total_dollars
  ) {
    return malformed('Bootstrap catalog totals did not reconcile.', status)
  }

  if (
    mapContext.type !== 'FeatureCollection' ||
    mapContext.contract_version !== MAP_CONTEXT_CONTRACT_VERSION ||
    mapContext.data_version !== identity.data_version ||
    mapContext.historical_decision_snapshot_date !== '2026-01-21' ||
    mapContext.project_identity_key !== 'decision_unit_id' ||
    mapContext.geometry_authority !== 'GOVERNED_RUNTIME_GEOMETRY_ONLY' ||
    mapContext.mapping_status !== 'PARTIAL_GOVERNED_RUNTIME_GEOMETRY_AVAILABLE' ||
    !isWholeNumber(mapContext.analytical_project_count) ||
    !isWholeNumber(mapContext.mapped_project_count) ||
    !isWholeNumber(mapContext.unmapped_project_count) ||
    mapContext.geometry_required_for_model_eligibility !== false ||
    mapContext.geometry_required_for_portfolio_selection !== false ||
    mapContext.fabricated_geometry !== false ||
    mapContext.derived_geocoded_geometry !== false ||
    mapContext.inferred_or_centroid_geometry !== false ||
    mapContext.governance_decision_id !== 'D-116' ||
    !isSha256(mapContext.governance_reconciliation_sha256) ||
    !isSha256(mapContext.candidate_geometry_snapshot_sha256) ||
    mapContext.crs_contract !== 'RFC_7946_EPSG_4326' ||
    !isStringArray(mapContext.limitations) ||
    !Array.isArray(mapContext.features) ||
    !mapContext.features.every(validateRuntimeMapFeature)
  ) {
    return malformed('Bootstrap map context was malformed.', status)
  }

  if (
    mapContext.analytical_project_count !== catalog.project_count ||
    mapContext.mapped_project_count + mapContext.unmapped_project_count !==
      mapContext.analytical_project_count
  ) {
    return malformed('Bootstrap map counts did not reconcile.', status)
  }
  const mapFeatureIds = mapContext.features.map(
    (feature) => (feature as RuntimeMapFeature).properties.decision_unit_id,
  )

  const catalogDecisionUnitIds = new Set(
    projects.map(
      (project) =>
        (project as Record<string, unknown>).decision_unit_id as string,
    ),
  )

  if (
    mapContext.features.length !== mapContext.mapped_project_count ||
    new Set(mapFeatureIds).size !== mapFeatureIds.length ||
    mapFeatureIds.some((decisionUnitId) => !catalogDecisionUnitIds.has(decisionUnitId))
  ) {
    return malformed('Bootstrap map features did not reconcile with the catalog.', status)
  }

  if (
    typeof config.environment_label !== 'string' ||
    typeof config.osm_tile_url !== 'string' ||
    typeof config.osm_attribution !== 'string' ||
    typeof config.fixture_mode !== 'boolean'
  ) {
    return malformed('Bootstrap public configuration was malformed.', status)
  }

  return payload as BootstrapSuccessEnvelope
}

function validateSelectedProject(value: unknown): boolean {
  return (
    isRecord(value) &&
    typeof value.decision_unit_id === 'string' &&
    isPositiveWholeNumber(value.model_request_dollars) &&
    isHalfPoint(value.funding_priority_score, 0, 100) &&
    isPositiveWholeNumber(value.funding_priority_rank) &&
    [
      'AUTO_COMPLETE_TIER',
      'AUTO_UNIQUE_BUDGET_FEASIBLE',
      'ANALYST_BOUNDARY_RESOLUTION',
    ].includes(String(value.selection_source))
  )
}

function validateBoundary(value: unknown): boolean {
  if (!isRecord(value) || !Array.isArray(value.candidates)) return false

  const candidatesValid =
    isHalfPoint(value.funding_priority_score, 0, 100) &&
    isPositiveWholeNumber(value.funding_priority_rank) &&
    isNonNegativeWholeNumber(value.remaining_budget_before_tier_dollars) &&
    isPositiveWholeNumber(value.full_tier_request_dollars) &&
    value.candidates.length > 0 &&
    value.candidates.every(
      (candidate) =>
        isRecord(candidate) &&
        typeof candidate.decision_unit_id === 'string' &&
        isPositiveWholeNumber(candidate.model_request_dollars) &&
        isHalfPoint(candidate.funding_priority_score, 0, 100) &&
        isPositiveWholeNumber(candidate.funding_priority_rank) &&
        typeof candidate.individually_budget_feasible === 'boolean',
    )

  if (!candidatesValid) return false

  const candidates = value.candidates as Array<Record<string, unknown>>
  const ids = candidates.map((candidate) => candidate.decision_unit_id)
  const requestTotal = candidates.reduce(
    (total, candidate) => total + Number(candidate.model_request_dollars),
    0,
  )

  return (
    new Set(ids).size === ids.length &&
    requestTotal === value.full_tier_request_dollars &&
    candidates.every(
      (candidate) =>
        candidate.funding_priority_score === value.funding_priority_score &&
        candidate.funding_priority_rank === value.funding_priority_rank,
    )
  )
}

export function parseFundingPlan(
  payload: unknown,
  status = 200,
): FundingPlanSuccessEnvelope {
  const { identity, data } = requireCommonSuccessEnvelope(
    payload,
    '/api/v1/plans/evaluate',
    FUNDING_PLAN_CONTRACT_VERSION,
    status,
  )

  const boundary = data.unresolved_boundary

  if (
    data.contract_version !== FUNDING_PLAN_CONTRACT_VERSION ||
    data.data_version !== identity.data_version ||
    !['COMPLETE', 'ANALYST_RESOLUTION_REQUIRED'].includes(String(data.status)) ||
    !isNonNegativeWholeNumber(data.available_budget_dollars) ||
    !Array.isArray(data.selected_projects) ||
    !data.selected_projects.every(validateSelectedProject) ||
    !isNonNegativeWholeNumber(data.included_total_dollars) ||
    !isNonNegativeWholeNumber(data.remainder_dollars) ||
    !(boundary === null || validateBoundary(boundary)) ||
    !Array.isArray(data.warnings) ||
    !data.warnings.every(
      (warning) =>
        isRecord(warning) &&
        warning.warning_code === 'HIGHER_PRIORITY_FEASIBLE_PROJECT_REMAINS' &&
        typeof warning.message === 'string' &&
        isStringArray(warning.decision_unit_ids) &&
        warning.decision_unit_ids.length > 0 &&
        new Set(warning.decision_unit_ids).size ===
          warning.decision_unit_ids.length,
    ) ||
    !Array.isArray(data.applied_analyst_overrides) ||
    !data.applied_analyst_overrides.every(
      (override) =>
        isRecord(override) &&
        isHalfPoint(override.funding_priority_score, 0, 100) &&
        isPositiveWholeNumber(override.funding_priority_rank) &&
        override.acknowledged === true &&
        isStringArray(override.decision_unit_ids_left_feasible) &&
        override.decision_unit_ids_left_feasible.length > 0 &&
        new Set(override.decision_unit_ids_left_feasible).size ===
          override.decision_unit_ids_left_feasible.length,
    ) ||
    typeof data.plan_fingerprint !== 'string' ||
    !/^[0-9a-f]{64}$/.test(data.plan_fingerprint)
  ) {
    return malformed('Funding Plan response data was malformed.', status)
  }

  const selectedProjects = data.selected_projects as Array<
    Record<string, unknown>
  >
  const selectedIds = selectedProjects.map(
    (project) => project.decision_unit_id,
  )
  const selectedTotal = selectedProjects.reduce(
    (total, project) => total + Number(project.model_request_dollars),
    0,
  )

  if (
    new Set(selectedIds).size !== selectedIds.length ||
    selectedTotal !== data.included_total_dollars ||
    data.included_total_dollars + data.remainder_dollars !==
      data.available_budget_dollars ||
    (data.status === 'COMPLETE' && boundary !== null) ||
    (data.status === 'ANALYST_RESOLUTION_REQUIRED' && boundary === null)
  ) {
    return malformed('Funding Plan response totals or boundary state did not reconcile.', status)
  }

  return payload as FundingPlanSuccessEnvelope
}

function validateBenchmarkOutcome(value: unknown): boolean {
  if (
    !isRecord(value) ||
    typeof value.decision_unit_id !== 'string' ||
    value.decision_unit_id.length === 0 ||
    !(
      typeof value.canonical_project_id === 'string' ||
      value.canonical_project_id === null
    ) ||
    typeof value.governed_name !== 'string' ||
    value.governed_name.length === 0 ||
    ![
      'Transportation',
      'Parks & Open Space',
      'Watershed',
      'Community Facilities',
    ].includes(String(value.presentation_category)) ||
    typeof value.historically_recommended !== 'boolean' ||
    !(
      isPositiveWholeNumber(value.january_recommendation_dollars) ||
      value.january_recommendation_dollars === null
    ) ||
    typeof value.source_conflict_flag !== 'boolean' ||
    typeof value.request_version_conflict !== 'boolean' ||
    value.outcome_role !== 'BENCHMARK_OUTCOME_ONLY'
  ) {
    return false
  }

  return (
    value.historically_recommended ===
    (value.january_recommendation_dollars !== null)
  )
}

export function parseHistoricalBenchmark(
  payload: unknown,
  status = 200,
): HistoricalBenchmarkSuccessEnvelope {
  const { identity, data } = requireCommonSuccessEnvelope(
    payload,
    '/api/v1/benchmark',
    BENCHMARK_CONTRACT_VERSION,
    status,
  )

  const benchmark = data.benchmark

  if (!isRecord(benchmark)) {
    return malformed('Historical benchmark response was incomplete.', status)
  }

  if (
    benchmark.contract_version !== BENCHMARK_CONTRACT_VERSION ||
    benchmark.data_version !== identity.data_version ||
    benchmark.historical_decision_snapshot_date !== '2026-01-21' ||
    typeof benchmark.source_id !== 'string' ||
    benchmark.source_id.length === 0 ||
    typeof benchmark.source_snapshot_sha256 !== 'string' ||
    !/^[0-9a-f]{64}$/.test(benchmark.source_snapshot_sha256) ||
    benchmark.outcome_role !== 'BENCHMARK_OUTCOME_ONLY' ||
    benchmark.analytical_project_count !== 106 ||
    benchmark.full_initial_recommendation_dollars !== 700_000_000 ||
    benchmark.matched_analytical_cohort_dollars !== 332_000_000 ||
    benchmark.outside_analytical_cohort_dollars !== 368_000_000 ||
    benchmark.historically_recommended_project_count !== 20 ||
    benchmark.ranking_input !== false ||
    benchmark.portfolio_selection_input !== false ||
    !Array.isArray(benchmark.category_summaries) ||
    benchmark.category_summaries.length !== 4 ||
    !benchmark.category_summaries.every(
      (summary) =>
        isRecord(summary) &&
        [
          'Transportation',
          'Parks & Open Space',
          'Watershed',
          'Community Facilities',
        ].includes(String(summary.presentation_category)) &&
        isPositiveWholeNumber(summary.analytical_project_count) &&
        isNonNegativeWholeNumber(summary.historically_recommended_project_count) &&
        isNonNegativeWholeNumber(summary.recommendation_total_dollars),
    ) ||
    !Array.isArray(benchmark.project_outcomes) ||
    benchmark.project_outcomes.length !== 106 ||
    !benchmark.project_outcomes.every(validateBenchmarkOutcome) ||
    !isStringArray(benchmark.limitations) ||
    benchmark.limitations.length === 0 ||
    benchmark.limitations.some((limitation) => limitation.trim().length === 0)
  ) {
    return malformed('Historical benchmark response data was malformed.', status)
  }


  const outcomes = benchmark.project_outcomes as Array<Record<string, unknown>>
  const outcomeIds = outcomes.map((outcome) => outcome.decision_unit_id)
  const historicallyRecommended = outcomes.filter(
    (outcome) => outcome.historically_recommended === true,
  )
  const recommendedDollars = historicallyRecommended.reduce(
    (total, outcome) => total + Number(outcome.january_recommendation_dollars),
    0,
  )
  const summaries = benchmark.category_summaries as Array<
    Record<string, unknown>
  >
  const categoryNames = summaries.map(
    (summary) => summary.presentation_category,
  )
  const expectedCategoryFacts: Record<
    string,
    { projects: number; recommended: number; dollars: number }
  > = {
    Transportation: { projects: 9, recommended: 2, dollars: 28_000_000 },
    'Parks & Open Space': { projects: 22, recommended: 1, dollars: 55_000_000 },
    Watershed: { projects: 37, recommended: 12, dollars: 125_000_000 },
    'Community Facilities': {
      projects: 38,
      recommended: 5,
      dollars: 124_000_000,
    },
  }
  const categoriesReconcile = summaries.every((summary) => {
    const category = String(summary.presentation_category)
    const facts = expectedCategoryFacts[category]
    const categoryOutcomes = outcomes.filter(
      (outcome) => outcome.presentation_category === category,
    )
    const recommended = categoryOutcomes.filter(
      (outcome) => outcome.historically_recommended === true,
    )

    return (
      facts !== undefined &&
      summary.analytical_project_count === facts.projects &&
      summary.historically_recommended_project_count === facts.recommended &&
      summary.recommendation_total_dollars === facts.dollars &&
      categoryOutcomes.length === facts.projects &&
      recommended.length === facts.recommended &&
      recommended.reduce(
        (total, outcome) =>
          total + Number(outcome.january_recommendation_dollars),
        0,
      ) === facts.dollars
    )
  })

  if (
    benchmark.full_initial_recommendation_dollars !==
      benchmark.matched_analytical_cohort_dollars +
        benchmark.outside_analytical_cohort_dollars ||
    outcomes.length !== benchmark.analytical_project_count ||
    new Set(outcomeIds).size !== outcomeIds.length ||
    historicallyRecommended.length !==
      benchmark.historically_recommended_project_count ||
    recommendedDollars !== benchmark.matched_analytical_cohort_dollars ||
    new Set(categoryNames).size !== 4 ||
    !categoriesReconcile
  ) {
    return malformed('Historical benchmark totals did not reconcile.', status)
  }

  return payload as HistoricalBenchmarkSuccessEnvelope
}

function isAbortError(error: unknown): boolean {
  return (
    (error instanceof DOMException && error.name === 'AbortError') ||
    (error instanceof Error && error.name === 'AbortError')
  )
}

async function requestJson<T>(
  endpoint: string,
  init: RequestInit,
  parseSuccess: (payload: unknown, status: number) => T,
): Promise<T> {
  let response: Response

  try {
    response = await fetch(endpoint, init)
  } catch (error: unknown) {
    if (isAbortError(error)) {
      throw new ApiClientError('Request was cancelled.', {
        kind: 'REQUEST_ABORTED',
        errorCode: 'REQUEST_ABORTED',
        cause: error,
      })
    }

    throw new ApiClientError('The ClimateCapital API is unavailable.', {
      kind: 'NETWORK_ERROR',
      errorCode: 'BACKEND_UNAVAILABLE',
      retryable: true,
      cause: error,
    })
  }

  let payload: unknown

  try {
    payload = await response.json()
  } catch (error: unknown) {
    if (response.ok) {
      throw new ApiClientError('API returned an unreadable success response.', {
        kind: 'UNEXPECTED_PAYLOAD',
        status: response.status,
        errorCode: 'UNEXPECTED_PAYLOAD',
        cause: error,
      })
    }

    throw new ApiClientError(`API request failed with HTTP ${response.status}.`, {
      kind: 'API_ERROR',
      status: response.status,
      errorCode: 'HTTP_ERROR',
      retryable: response.status >= 500,
      cause: error,
    })
  }

  if (!response.ok) {
    const envelope = parseErrorEnvelope(payload, response.status)

    if (envelope !== null) {
      throw new ApiClientError(envelope.error.message, {
        kind: 'API_ERROR',
        status: response.status,
        errorCode: envelope.error.error_code,
        fieldPath: envelope.error.field_path,
        retryable: envelope.error.retryable,
        identity: envelope.identity,
      })
    }

    throw new ApiClientError(`API request failed with HTTP ${response.status}.`, {
      kind: 'API_ERROR',
      status: response.status,
      errorCode: 'HTTP_ERROR',
      retryable: response.status >= 500,
    })
  }

  return parseSuccess(payload, response.status)
}

export function fetchBootstrap(signal?: AbortSignal): Promise<BootstrapSuccessEnvelope> {
  return requestJson(
    '/api/v1/bootstrap',
    {
      method: 'GET',
      headers: { Accept: 'application/json' },
      signal,
    },
    parseBootstrap,
  )
}

export function evaluateFundingPlan(
  request: FundingPlanInput,
  signal?: AbortSignal,
): Promise<FundingPlanSuccessEnvelope> {
  return requestJson(
    '/api/v1/plans/evaluate',
    {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
      signal,
    },
    parseFundingPlan,
  )
}

export function fetchHistoricalBenchmark(
  signal?: AbortSignal,
): Promise<HistoricalBenchmarkSuccessEnvelope> {
  return requestJson(
    '/api/v1/benchmark',
    {
      method: 'GET',
      headers: { Accept: 'application/json' },
      signal,
    },
    parseHistoricalBenchmark,
  )
}
