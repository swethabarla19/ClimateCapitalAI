import {
  BENCHMARK_CONTRACT_VERSION,
  CATALOG_CONTRACT_VERSION,
  FUNDING_PLAN_CONTRACT_VERSION,
  MAP_CONTEXT_CONTRACT_VERSION,
  type BootstrapSuccessEnvelope,
  type FundingPlanSuccessEnvelope,
  type HistoricalBenchmarkSuccessEnvelope,
  type PresentationCategory,
  type RuntimeProject,
  type RuntimeMapFeature,
} from '../api/contracts'

export const TEST_DATA_VERSION =
  'climatecapital-austin-2026-01-21-cross-category-v2'
export const TEST_RELEASE_ID =
  'efb3783b2f4c7568012fb9ae590ff40dbf5a46d18a3ff1942a22d424a4b52207'
export const TEST_FINGERPRINT = 'a'.repeat(64)
export const TEST_700_FINGERPRINT = 'b'.repeat(64)
export const TEST_750_FINGERPRINT = 'c'.repeat(64)
export const TEST_RESOLVED_FINGERPRINT = 'd'.repeat(64)

const categories: Array<[PresentationCategory, number, string]> = [
  ['Transportation', 9, 'transportation'],
  ['Parks & Open Space', 22, 'parks-open-space'],
  ['Watershed', 37, 'watershed'],
  ['Community Facilities', 38, 'community-facilities'],
]

const benchmarkCategoryFacts: Record<
  PresentationCategory,
  { recommendedCount: number; recommendationDollars: number }
> = {
  Transportation: {
    recommendedCount: 2,
    recommendationDollars: 28_000_000,
  },
  'Parks & Open Space': {
    recommendedCount: 1,
    recommendationDollars: 55_000_000,
  },
  Watershed: {
    recommendedCount: 12,
    recommendationDollars: 125_000_000,
  },
  'Community Facilities': {
    recommendedCount: 5,
    recommendationDollars: 124_000_000,
  },
}

function project(
  category: PresentationCategory,
  slug: string,
  index: number,
  globalIndex: number,
): RuntimeProject {
  const score =
    globalIndex === 1
      ? 83
      : globalIndex <= 5
        ? 77
        : globalIndex <= 25
          ? 65
          : globalIndex === 26
            ? 54.5
            : 54
  const rank =
    globalIndex === 1
      ? 1
      : globalIndex <= 5
        ? 2
        : globalIndex <= 25
          ? 6
          : globalIndex === 26
            ? 26
            : 27
  const tieGroupSize =
    globalIndex === 1 || globalIndex === 26
      ? 1
      : globalIndex <= 5
        ? 4
        : globalIndex <= 25
          ? 20
          : 80
  const displayOrder =
    globalIndex <= 1
      ? 1
      : globalIndex <= 5
        ? globalIndex - 1
        : globalIndex <= 25
          ? globalIndex - 5
          : globalIndex === 26
            ? 1
            : globalIndex - 26
  let remainingScore = score
  const componentValue = (maximum: number) => {
    const value = Math.min(maximum, remainingScore)
    remainingScore -= value
    return value
  }

  return {
    decision_unit_id: `${slug}/fixture/project-${index}`,
    canonical_project_id:
      category === 'Watershed'
        ? `${String(index).padStart(4, '0')}.001`
        : null,
    governed_name: `${category} fixture project ${index}`,
    presentation_category: category,
    source_department: 'Fixture Department',
    source_domain: `${category} / Fixture`,
    model_request_dollars:
      globalIndex === 1
        ? 1_000_000
        : globalIndex === 106
          ? 100_000_000
          : 18_005_000,
    model_request_authority: 'M3.6_GOVERNED_JANUARY_REQUEST',
    model_request_authority_source_id:
      'austin_2026_bond_initial_draft_2026_01_21',
    request_version_conflict: false,
    funding_priority_score: score,
    funding_priority_rank: rank,
    is_tied: tieGroupSize > 1,
    tie_group_size: tieGroupSize,
    display_order_within_tie: displayOrder,
    display_tiebreak_has_analytical_meaning: false,
    prb_components: {
      strategic_alignment: componentValue(8),
      critical_asset: componentValue(8),
      community_consideration: componentValue(20),
      efficiency: componentValue(20),
      timeliness_readiness: componentValue(24),
      climate_resilience: componentValue(20),
    },
    council_district: {
      assignment_type: 'UNSPECIFIED',
      districts: [],
      source_value: null,
      analyst_review_only: true,
      hard_portfolio_constraint: false,
    },
    om_impact: {
      value: 'NO',
      analyst_review_only: true,
      hard_portfolio_constraint: false,
      additional_score_preference_authorized: false,
    },
    provenance_refs: ['austin_2026_bond_initial_draft_2026_01_21'],
  }
}

export function runtimeProjectsFixture(): RuntimeProject[] {
  let globalIndex = 0

  return categories.flatMap(([category, count, slug]) =>
    Array.from({ length: count }, (_, index) => {
      globalIndex += 1
      return project(category, slug, index + 1, globalIndex)
    }),
  )
}

function runtimeMapFeaturesFixture(
  projects: RuntimeProject[],
): RuntimeMapFeature[] {
  return projects.slice(0, 74).map((project, index) => {
    const longitude = -97.82 + (index % 10) * 0.015
    const latitude = 30.20 + Math.floor(index / 10) * 0.015

    const displayRole =
      index < 42
        ? 'PROJECT_DISPLAY_POINT'
        : index < 64
          ? 'FACILITY_SITE_CONTEXT'
          : index < 72
            ? 'PARK_SITE_CONTEXT'
            : index === 72
              ? 'PROJECT_SITE'
              : 'PROJECT_PARCEL'

    let geometry: RuntimeMapFeature['geometry']

    if (index < 64) {
      geometry = {
        type: 'Point',
        coordinates: [longitude, latitude],
      }
    } else if (index < 73) {
      geometry = {
        type: 'Polygon',
        coordinates: [
          [
            [longitude, latitude],
            [longitude + 0.004, latitude],
            [longitude + 0.004, latitude + 0.004],
            [longitude, latitude + 0.004],
            [longitude, latitude],
          ],
        ],
      }
    } else {
      geometry = {
        type: 'MultiPolygon',
        coordinates: [
          [
            [
              [longitude, latitude],
              [longitude + 0.004, latitude],
              [longitude + 0.004, latitude + 0.004],
              [longitude, latitude + 0.004],
              [longitude, latitude],
            ],
          ],
        ],
      }
    }

    return {
      type: 'Feature',
      id: project.decision_unit_id,
      geometry,
      properties: {
        decision_unit_id: project.decision_unit_id,
        governed_name: project.governed_name,
        presentation_category: project.presentation_category,
        display_role: displayRole,
        geometry_type: geometry.type === 'Point' ? 'point' : 'polygon',
        geometry_origin: 'SOURCE_NATIVE_FEATURE',
        confidence: 'HIGH',
        governance_decision_id: 'D-116',
        caveats:
          displayRole === 'PROJECT_DISPLAY_POINT'
            ? [
                'Official project display point; it is not an engineering or construction footprint.',
              ]
            : [
                'Context geometry; do not imply a capital construction footprint.',
              ],
        historical_fit_class: 'PRE_SNAPSHOT_SOURCE',
        historical_fit_judgment: 'Fixture governed historical-fit evidence.',
        source_agency: 'City of Austin',
        source_title: 'Fixture governed GIS source',
        source_feature_id: String(index + 1),
        source_url: 'https://example.invalid/governed-gis-fixture',
      },
    }
  })
}

export function bootstrapFixture(): BootstrapSuccessEnvelope {
  const projects = runtimeProjectsFixture()
  const mapFeatures = runtimeMapFeaturesFixture(projects)
  return {
    endpoint: '/api/v1/bootstrap',
    status: 'SUCCESS',
    identity: {
      request_id: '123e4567-e89b-12d3-a456-426614174000',
      api_namespace: '/api/v1',
      contract_version: CATALOG_CONTRACT_VERSION,
      data_version: TEST_DATA_VERSION,
      release_id: TEST_RELEASE_ID,
    },
    data: {
      catalog: {
        contract_version: CATALOG_CONTRACT_VERSION,
        data_version: TEST_DATA_VERSION,
        historical_decision_snapshot_date: '2026-01-21',
        model_scope: 'CROSS_CATEGORY_PRB_PROJECT_MODEL',
        methodology_name:
          'PRIORITY_CONSTRAINED_ANALYST_GOVERNED_PORTFOLIO_CONSTRUCTION',
        cross_category_ranking_authorized: true,
        portfolio_selection_authorized: true,
        runtime_integration_authorized: true,
        project_count: 106,
        governed_request_total_dollars: 1_973_520_000,
        category_counts: {
          transportation: 9,
          parks_open_space: 22,
          watershed: 37,
          community_facilities: 38,
        },
        unique_funding_priority_score_count: 35,
        tied_score_group_count: 24,
        projects_in_tied_score_groups: 95,
        projects,
      },
      map_context: {
        type: 'FeatureCollection',
        contract_version: MAP_CONTEXT_CONTRACT_VERSION,
        data_version: TEST_DATA_VERSION,
        historical_decision_snapshot_date: '2026-01-21',
        project_identity_key: 'decision_unit_id',
        geometry_authority: 'GOVERNED_RUNTIME_GEOMETRY_ONLY',
        mapping_status: 'PARTIAL_GOVERNED_RUNTIME_GEOMETRY_AVAILABLE',
        analytical_project_count: 106,
        mapped_project_count: 74,
        unmapped_project_count: 32,
        geometry_required_for_model_eligibility: false,
        geometry_required_for_portfolio_selection: false,
        fabricated_geometry: false,
        derived_geocoded_geometry: false,
        inferred_or_centroid_geometry: false,
        crs_contract: 'RFC_7946_EPSG_4326',
        governance_decision_id: 'D-116',
        governance_reconciliation_sha256: 'a'.repeat(64),
        candidate_geometry_snapshot_sha256: 'b'.repeat(64),
        limitations: [
          'Only governed source-native geometry may be displayed.',
          'Projects without governed geometry remain available outside the map.',
        ],
        features: mapFeatures,
      },
      public_configuration: {
        environment_label: 'test',
        osm_tile_url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
        osm_attribution: '© OpenStreetMap contributors',
        fixture_mode: false,
      },
    },
  }
}

export function planResultFixture(
  budget = 332_000_000,
): FundingPlanSuccessEnvelope {
  return {
    endpoint: '/api/v1/plans/evaluate',
    status: 'SUCCESS',
    identity: {
      request_id: '123e4567-e89b-12d3-a456-426614174001',
      api_namespace: '/api/v1',
      contract_version: FUNDING_PLAN_CONTRACT_VERSION,
      data_version: TEST_DATA_VERSION,
      release_id: TEST_RELEASE_ID,
    },
    data: {
      contract_version: FUNDING_PLAN_CONTRACT_VERSION,
      data_version: TEST_DATA_VERSION,
      status: 'COMPLETE',
      available_budget_dollars: budget,
      selected_projects: [
        {
          decision_unit_id: 'parks-open-space/fixture/project-17',
          model_request_dollars: 18_005_000,
          funding_priority_score: 54.5,
          funding_priority_rank: 26,
          selection_source: 'AUTO_COMPLETE_TIER',
        },
      ],
      included_total_dollars: 18_005_000,
      remainder_dollars: budget - 18_005_000,
      unresolved_boundary: null,
      warnings: [],
      applied_analyst_overrides: [],
      plan_fingerprint: TEST_FINGERPRINT,
    },
  }
}

function selectedProjectFixtures(
  count: number,
  includedTotalDollars: number,
): FundingPlanSuccessEnvelope['data']['selected_projects'] {
  const projects = runtimeProjectsFixture().slice(0, count)
  const baseRequest = Math.floor(includedTotalDollars / count)
  const remainder = includedTotalDollars - baseRequest * count

  return projects.map((entry, index) => ({
    decision_unit_id: entry.decision_unit_id,
    model_request_dollars:
      baseRequest + (index === projects.length - 1 ? remainder : 0),
    funding_priority_score: entry.funding_priority_score,
    funding_priority_rank: entry.funding_priority_rank,
    selection_source:
      index < 12 ? 'AUTO_COMPLETE_TIER' : 'AUTO_UNIQUE_BUDGET_FEASIBLE',
  }))
}

function fundingPlanEnvelope(
  data: FundingPlanSuccessEnvelope['data'],
): FundingPlanSuccessEnvelope {
  return {
    endpoint: '/api/v1/plans/evaluate',
    status: 'SUCCESS',
    identity: {
      request_id: '123e4567-e89b-12d3-a456-426614174010',
      api_namespace: '/api/v1',
      contract_version: FUNDING_PLAN_CONTRACT_VERSION,
      data_version: TEST_DATA_VERSION,
      release_id: TEST_RELEASE_ID,
    },
    data,
  }
}

export function complete332PlanFixture(): FundingPlanSuccessEnvelope {
  const selectedProjects = selectedProjectFixtures(18, 331_825_000)

  return fundingPlanEnvelope({
    contract_version: FUNDING_PLAN_CONTRACT_VERSION,
    data_version: TEST_DATA_VERSION,
    status: 'COMPLETE',
    available_budget_dollars: 332_000_000,
    selected_projects: selectedProjects,
    included_total_dollars: 331_825_000,
    remainder_dollars: 175_000,
    unresolved_boundary: null,
    warnings: [],
    applied_analyst_overrides: [],
    plan_fingerprint: TEST_FINGERPRINT,
  })
}

export function boundary700PlanFixture(): FundingPlanSuccessEnvelope {
  const candidateProjects = runtimeProjectsFixture().slice(30, 35)
  const requests = [60_500_000, 12_000_000, 35_000_000, 4_000_000, 1_500_000]

  return fundingPlanEnvelope({
    contract_version: FUNDING_PLAN_CONTRACT_VERSION,
    data_version: TEST_DATA_VERSION,
    status: 'ANALYST_RESOLUTION_REQUIRED',
    available_budget_dollars: 700_000_000,
    selected_projects: selectedProjectFixtures(27, 591_725_000),
    included_total_dollars: 591_725_000,
    remainder_dollars: 108_275_000,
    unresolved_boundary: {
      funding_priority_score: 67,
      funding_priority_rank: 28,
      remaining_budget_before_tier_dollars: 108_275_000,
      full_tier_request_dollars: 113_000_000,
      candidates: candidateProjects.map((entry, index) => ({
        decision_unit_id: entry.decision_unit_id,
        model_request_dollars: requests[index],
        funding_priority_score: 67,
        funding_priority_rank: 28,
        individually_budget_feasible: true,
      })),
    },
    warnings: [],
    applied_analyst_overrides: [],
    plan_fingerprint: TEST_700_FINGERPRINT,
  })
}

export function boundary750PlanFixture(): FundingPlanSuccessEnvelope {
  const candidateProjects = runtimeProjectsFixture().slice(40, 48)
  const requests = [
    19_000_000,
    24_000_000,
    2_500_000,
    10_000_000,
    13_800_000,
    8_750_000,
    8_100_000,
    7_700_000,
  ]

  return fundingPlanEnvelope({
    contract_version: FUNDING_PLAN_CONTRACT_VERSION,
    data_version: TEST_DATA_VERSION,
    status: 'ANALYST_RESOLUTION_REQUIRED',
    available_budget_dollars: 750_000_000,
    selected_projects: selectedProjectFixtures(36, 716_720_000),
    included_total_dollars: 716_720_000,
    remainder_dollars: 33_280_000,
    unresolved_boundary: {
      funding_priority_score: 65,
      funding_priority_rank: 37,
      remaining_budget_before_tier_dollars: 33_280_000,
      full_tier_request_dollars: 93_850_000,
      candidates: candidateProjects.map((entry, index) => ({
        decision_unit_id: entry.decision_unit_id,
        model_request_dollars: requests[index],
        funding_priority_score: 65,
        funding_priority_rank: 37,
        individually_budget_feasible: true,
      })),
    },
    warnings: [],
    applied_analyst_overrides: [],
    plan_fingerprint: TEST_750_FINGERPRINT,
  })
}

export function resolved700PlanFixture(
  selectedDecisionUnitIds: string[],
  acknowledged = true,
): FundingPlanSuccessEnvelope {
  const boundary = boundary700PlanFixture().data.unresolved_boundary
  if (boundary === null) throw new Error('Expected the 700M boundary fixture.')

  const selectedCandidates = boundary.candidates.filter((candidate) =>
    selectedDecisionUnitIds.includes(candidate.decision_unit_id),
  )
  const selectedProjects = [
    ...boundary700PlanFixture().data.selected_projects,
    ...selectedCandidates.map((candidate) => ({
      decision_unit_id: candidate.decision_unit_id,
      model_request_dollars: candidate.model_request_dollars,
      funding_priority_score: candidate.funding_priority_score,
      funding_priority_rank: candidate.funding_priority_rank,
      selection_source: 'ANALYST_BOUNDARY_RESOLUTION' as const,
    })),
  ]
  const includedTotal = selectedProjects.reduce(
    (total, project) => total + project.model_request_dollars,
    0,
  )
  const selectedSet = new Set(selectedDecisionUnitIds)
  const remainingAfterSelection = 700_000_000 - includedTotal
  const leftFeasible = boundary.candidates.filter(
    (candidate) =>
      !selectedSet.has(candidate.decision_unit_id) &&
      candidate.model_request_dollars <= remainingAfterSelection,
  )

  return fundingPlanEnvelope({
    contract_version: FUNDING_PLAN_CONTRACT_VERSION,
    data_version: TEST_DATA_VERSION,
    status: 'COMPLETE',
    available_budget_dollars: 700_000_000,
    selected_projects: selectedProjects,
    included_total_dollars: includedTotal,
    remainder_dollars: 700_000_000 - includedTotal,
    unresolved_boundary: null,
    warnings:
      acknowledged && leftFeasible.length > 0
        ? [
            {
              warning_code: 'HIGHER_PRIORITY_FEASIBLE_PROJECT_REMAINS',
              message:
                'One or more unselected same-priority projects remain budget-feasible.',
              decision_unit_ids: leftFeasible.map(
                (candidate) => candidate.decision_unit_id,
              ),
            },
          ]
        : [],
    applied_analyst_overrides:
      acknowledged && leftFeasible.length > 0
        ? [
            {
              funding_priority_score: 67,
              funding_priority_rank: 28,
              acknowledged: true,
              decision_unit_ids_left_feasible: leftFeasible.map(
                (candidate) => candidate.decision_unit_id,
              ),
            },
          ]
        : [],
    plan_fingerprint: TEST_RESOLVED_FINGERPRINT,
  })
}

export function benchmarkFixture(): HistoricalBenchmarkSuccessEnvelope {
  const projects = runtimeProjectsFixture()
  const categoryIndexes = new Map<PresentationCategory, number>()
  const outcomes = projects.map((entry) => {
    const categoryIndex = categoryIndexes.get(entry.presentation_category) ?? 0
    categoryIndexes.set(entry.presentation_category, categoryIndex + 1)
    const facts = benchmarkCategoryFacts[entry.presentation_category]
    const historicallyRecommended = categoryIndex < facts.recommendedCount
    const baseRecommendation = Math.floor(
      facts.recommendationDollars / facts.recommendedCount,
    )
    const categoryRemainder =
      facts.recommendationDollars - baseRecommendation * facts.recommendedCount

    return {
      decision_unit_id: entry.decision_unit_id,
      canonical_project_id: entry.canonical_project_id,
      governed_name: entry.governed_name,
      presentation_category: entry.presentation_category,
      historically_recommended: historicallyRecommended,
      january_recommendation_dollars: historicallyRecommended
        ? baseRecommendation +
          (categoryIndex === facts.recommendedCount - 1
            ? categoryRemainder
            : 0)
        : null,
      source_conflict_flag: false,
      request_version_conflict: false,
      outcome_role: 'BENCHMARK_OUTCOME_ONLY' as const,
    }
  })

  return {
    endpoint: '/api/v1/benchmark',
    status: 'SUCCESS',
    identity: {
      request_id: '123e4567-e89b-12d3-a456-426614174002',
      api_namespace: '/api/v1',
      contract_version: BENCHMARK_CONTRACT_VERSION,
      data_version: TEST_DATA_VERSION,
      release_id: TEST_RELEASE_ID,
    },
    data: {
      benchmark: {
        contract_version: BENCHMARK_CONTRACT_VERSION,
        data_version: TEST_DATA_VERSION,
        historical_decision_snapshot_date: '2026-01-21',
        source_id: 'austin_2026_bond_initial_draft_2026_01_21',
        source_snapshot_sha256: 'b'.repeat(64),
        outcome_role: 'BENCHMARK_OUTCOME_ONLY',
        analytical_project_count: 106,
        full_initial_recommendation_dollars: 700_000_000,
        matched_analytical_cohort_dollars: 332_000_000,
        outside_analytical_cohort_dollars: 368_000_000,
        historically_recommended_project_count: 20,
        ranking_input: false,
        portfolio_selection_input: false,
        category_summaries: categories.map(([category, count]) => ({
          presentation_category: category,
          analytical_project_count: count,
          historically_recommended_project_count:
            benchmarkCategoryFacts[category].recommendedCount,
          recommendation_total_dollars:
            benchmarkCategoryFacts[category].recommendationDollars,
        })),
        project_outcomes: outcomes,
        limitations: [
          'Historical recommendation membership is benchmark evidence only.',
        ],
      },
    },
  }
}
