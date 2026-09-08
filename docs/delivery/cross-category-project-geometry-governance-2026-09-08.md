# Cross-Category Project Geometry Governance — 2026-09-08

> **Status:** Governed under D-116
> **Scope:** Project map evidence only; no analytical, portfolio, benchmark, or
> frontend behavior change

## Decision

The 106 candidate records were reconciled individually. Seventy-four
HIGH-confidence, source-native official features are promoted into the governed
runtime map context. Thirty-two projects remain explicitly unmapped.

No address was geocoded, no coordinate was inferred, no centroid was computed,
and no project geometry was fabricated. The published runtime-v2 bundle remains
unchanged at 0 mapped / 106 unmapped. Runtime-v3 is the new active bundle and
reports 74 mapped / 32 unmapped.

The governed 106-project catalog and Historical Benchmark in runtime-v3 are
byte-for-byte identical to runtime-v2. Geometry does not change model eligibility,
Funding Priority, Funding Plan selection, request values, PRB scores/ranks, or
benchmark outcomes.

## Promoted coverage

| Category | Point | Polygon | Total | Unmapped |
| --- | ---: | ---: | ---: | ---: |
| Transportation | 0 | 1 | 1 | 8 |
| Parks & Open Space | 13 | 8 | 21 | 1 |
| Watershed | 35 | 0 | 35 | 2 |
| Community Facilities | 16 | 1 | 17 | 21 |
| **Total** | **64** | **10** | **74** | **32** |

| Display role | Count | Meaning |
| --- | ---: | --- |
| `PROJECT_DISPLAY_POINT` | 42 | Official project display point, not a construction footprint |
| `FACILITY_SITE_CONTEXT` | 22 | Existing facility location context, not necessarily the project footprint |
| `PARK_SITE_CONTEXT` | 8 | Whole-park context, not necessarily the project footprint |
| `PROJECT_SITE` | 1 | Source-native Barton Springs Bridge project-site polygon |
| `PROJECT_PARCEL` | 1 | Official Canyon Creek parcel linked by APD evidence, not necessarily the construction footprint |
| `PROJECT_CORRIDOR` | 0 | No authoritative project line was promoted |

Historical-fit classes among promoted features are 35 exact-snapshot Watershed
display points, 18 pre-snapshot official features, and 21 later-refreshed features
accepted only for stable-location context. Later status, budget, schedule, scope,
and other project facts are not governed from those sources.

## Candidates remaining unmapped

| `decision_unit_id` | Candidate | Disposition | Reason |
| --- | --- | --- | --- |
| `community-facilities/acme/elizabet-ney-museum` | MEDIUM polygon | Held | Multiple museum/storage representations exist; no unique ADA restroom/storage project footprint is established. |
| `community-facilities/acme/zilker-hillside-theatre` | MEDIUM address-only | Held | Official address exists, but no source-native theatre geometry was found; nearby assets and park centroids are invalid substitutes. |
| `community-facilities/ems/demand-station-1` | MEDIUM point | Held | Official sources conflict between Demand 01 labels and the governed 401 E 5th Street address. |
| `community-facilities/ems/demand-station-2` | MEDIUM point | Held | Pre- and post-snapshot official sources place Demand 02 at conflicting locations. |
| `community-facilities/ems/demand-station-9` | NO_MATCH | Rejected | No defensible project-specific site or geometry was found. |
| `community-facilities/fire/education-building-b` | LOW | Rejected | Generic training-campus context does not prove a unique project site. |
| `community-facilities/fleet/consolidated-service-center` | NO_MATCH | Rejected | No defensible project-specific site or geometry was found. |
| `community-facilities/fleet/fuel-station-central` | NO_MATCH | Rejected | No defensible project-specific site or geometry was found. |
| `community-facilities/fleet/fuel-station-northwest` | NO_MATCH | Rejected | No defensible project-specific site or geometry was found. |
| `community-facilities/fleet/fuel-station-southeast` | NO_MATCH | Rejected | No defensible project-specific site or geometry was found. |
| `community-facilities/hso/north-austin-homeless-resource-center` | NO_MATCH | Rejected | No official project site was established for the proposed/new facility. |
| `community-facilities/library/colony-park-branch-library` | NO_MATCH | Rejected | No official project site was established for the proposed branch. |
| `community-facilities/municipal-court/customer-service-center` | NO_MATCH | Rejected | No defensible project-specific site or geometry was found. |
| `community-facilities/police/air-operations` | NO_MATCH | Rejected | No defensible project-specific site or geometry was found. |
| `community-facilities/police/central-west-substation` | NO_MATCH | Rejected | No defensible project-specific site or geometry was found. |
| `community-facilities/police/downtown-substation` | NO_MATCH | Rejected | No defensible project-specific site or geometry was found. |
| `community-facilities/police/northeast-substation` | NO_MATCH | Rejected | No defensible project-specific site or geometry was found. |
| `community-facilities/police/scenario-based-training` | LOW | Rejected | Adjacent-campus context does not establish the new project's parcel or footprint. |
| `community-facilities/police/southwest-substation` | NO_MATCH | Rejected | No defensible project-specific site or geometry was found. |
| `community-facilities/public-health/colony-park` | NO_MATCH | Rejected | No official project site was established for the proposed/new facility. |
| `community-facilities/public-health/northeast` | NO_MATCH | Rejected | No official project site was established for the proposed/new facility. |
| `parks/bolm-maintenance-center` | MEDIUM polygon | Held | The whole 68.1-acre park polygon materially overstates the approximately 10-acre candidate area; the project parcel/footprint is unresolved. |
| `transportation/act-plan-6th-street` | MEDIUM, no geometry | Held | Official corridor identity exists, but no authoritative project line or footprint was found. |
| `transportation/act-plan-7th-street` | MEDIUM, no geometry | Held | Official corridor identity exists, but no authoritative project line or footprint was found. |
| `transportation/delwau-ln-replacement` | MEDIUM, no geometry | Held | Official bridge identity exists, but no authoritative project geometry was found. |
| `transportation/e-7th-st` | MEDIUM, no geometry | Held | Official bridge/railroad-crossing identity exists, but no authoritative project geometry was found. |
| `transportation/hart-ln-retaining-walls` | MEDIUM, no geometry | Held | Official asset identity exists, but no authoritative project geometry was found. |
| `transportation/river-plantation-dr` | MEDIUM, no geometry | Held | Official bridge identity exists, but no authoritative project geometry was found. |
| `transportation/w-slaughter-ln` | MEDIUM, no geometry | Held | Official bridge identity exists, but no authoritative project geometry was found. |
| `transportation/west-william-cannon-rehab` | MEDIUM, no geometry | Held | Official bridge identity exists, but no authoritative project geometry was found. |
| `watershed/5789.127` | HIGH point | Held | The exact CIP ID conflicts in scope/name: GIS describes West Bouldin/Hether storm-drain work while the governed row describes Zilker/Bluebonnet/Hether water/wastewater renewal. |
| `watershed/5789.150` | HIGH point | Held | It is a citywide renewal program; one display point would imply misleading geographic precision. |

District, ZIP, neighborhood, road-name midpoint, department headquarters, and
similarly named facility proxies remain prohibited for these projects.

## Governed artifacts and validation

- `data/governed/cross_category/reconciliation/project-geometry-governance.json`
  records all 106 decisions, candidate/source provenance, feature IDs,
  historical-fit judgments, display roles, caveats, and unmapped reasons.
- `data/governed/cross_category/runtime_v3/map-context.geojson` contains only the
  74 promoted source-native features.
- `data/governed/cross_category/runtime_v3/manifest.json` pins the map,
  governance-reconciliation, candidate-geometry, catalog, and benchmark hashes.
- `data/governed/cross_category/runtime_v3/catalog.json` and `benchmark.json` are
  byte-identical copies of the frozen runtime-v2 artifacts.
- `data/reconnaissance/external_gis/2026-09-08/CANDIDATE_NOT_GOVERNED_source_geometries.geojson`
  preserves the 80 captured candidate source features and remains conspicuously
  labeled research/not governed.

The governed contracts reject non-HIGH promotion, derived geometry, unresolved
historical fit, ambiguous promotion, missing source feature identity, display-role
and geometry-type mismatch, duplicate IDs, incorrect counts/category coverage,
and any feature for citywide `5789.150`. Runtime loading reconciles feature IDs,
names, categories, counts, artifact hashes, and governance hashes across the
catalog, map, and manifest.

## Remaining governance concerns

- Later-refreshed park/PARD, AFM, and CPE geometry is governed only for stable
  location. If those source shapes change, the pinned snapshot must not be silently
  refreshed; a new review is required.
- Park/facility/parcel context requires explicit UI labeling before map rendering
  is implemented.
- Source attribution and reuse/license metadata should be rechecked before final
  public deployment; this checkpoint governs evidentiary identity and display
  semantics, not an unstated license grant.
- The 32 unmapped projects require new official evidence or a separately approved
  display-semantic decision; visual completeness alone is not sufficient.
