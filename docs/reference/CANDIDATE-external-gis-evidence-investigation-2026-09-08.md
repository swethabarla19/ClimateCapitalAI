# CANDIDATE / RESEARCH / NOT YET GOVERNED

# External GIS Evidence Investigation — 106-Project Universe

**Research date:** September 8, 2026
**Historical decision snapshot:** January 21, 2026
**Identity key:** `decision_unit_id`
**Authority status:** Research only; not approved for governed runtime use

## Governance Boundary

This investigation evaluates whether official external GIS evidence can be
reconciled to the 106 governed ClimateCapital decision units. It does not make
candidate geometry authoritative.

The governed state remains unchanged:

- mapped projects: **0/106**
- unmapped projects: **106/106**
- `fabricated_geometry=false`

No runtime geometry, analytical input, Funding Priority, Funding Plan,
benchmark, project identity, request, count, or recommendation behavior was
changed.

## Result

The official-source investigation found 76 HIGH-confidence source-native
geometry candidates. Two Watershed rows are nevertheless held: `5789.127` has
an exact project-ID match but a material source-name/scope conflict, and
citywide program `5789.150` needs an approved rule before a single display point
could be shown without implying false geographic precision.

Accordingly:

- **74 projects can defensibly proceed to explicit geometry governance review**
  now, with the geometry role shown in the candidate artifact.
- **32 projects need more evidence or conflict resolution** and should remain
  explicitly unmapped.
- No address was geocoded during this investigation, so there are **0**
  HIGH-confidence official-address-derived geometries.
- The results support mixed geometry types and explicit display semantics;
  they do not support forcing every project into a pin.

“Eligible for governance review” is not runtime authorization. A separate,
explicit approval is still required before any candidate can change the 0/106
governed geometry state.

## Confidence Summary

| Category | HIGH source-native | HIGH address-derived | MEDIUM | LOW | NO_MATCH | Total |
|---|---:|---:|---:|---:|---:|---:|
| Watershed | 37 | 0 | 0 | 0 | 0 | 37 |
| Parks & Open Space | 21 | 0 | 1 | 0 | 0 | 22 |
| Transportation | 1 | 0 | 8 | 0 | 0 | 9 |
| Community Facilities | 17 | 0 | 4 | 2 | 15 | 38 |
| **Total** | **76** | **0** | **13** | **2** | **15** | **106** |

The HIGH total and the eligible total differ by two because `5789.127` is held
for identity/scope review and citywide program `5789.150` is held for display-
semantics review.

## Geometry-Type Summary

| Category | Point | Line | Polygon | Address-only | No geometry | Total |
|---|---:|---:|---:|---:|---:|---:|
| Watershed | 37 | 0 | 0 | 0 | 0 | 37 |
| Parks & Open Space | 13 | 0 | 9 | 0 | 0 | 22 |
| Transportation | 0 | 0 | 1 | 0 | 8 | 9 |
| Community Facilities | 18 | 0 | 2 | 1 | 17 | 38 |
| **Total** | **68** | **0** | **12** | **1** | **25** | **106** |

These are primary candidate representations, not a claim that a point is a
construction footprint. The artifact distinguishes:

- official project display point;
- official project geometry;
- official project parcel;
- existing facility-site context;
- existing park-site context;
- conflicting location; and
- unmapped project.

## Matching Standard Applied

Every candidate row records the governed identity, official source and URL,
ArcGIS item/service/layer and feature ID when applicable, geometry type and
origin, source vintage, historical-fit judgment, match identifiers and method,
confidence, ambiguity, multiple-feature state, display role, and governance
eligibility.

The investigation used:

- exact official project/CIP IDs where available;
- exact official facility, station, branch, park, address, or parcel linkage;
- official project narratives only when they tied the governed project to a
  unique named site; and
- official corridor/bridge descriptions as MEDIUM evidence when no defensible
  source-native feature was available.

It did not use Google Maps, search-snippet coordinates, district/ZIP/
neighborhood centroids, road-name midpoints, department headquarters, or
manually estimated coordinates.

## Watershed — 37/37 HIGH Source-Native Candidates

The strongest finding is the official City layer
[WPD CIP Projects (Points for display only)](https://services.arcgis.com/0L95CJ0VTaxqcmED/arcgis/rest/services/WPD%20CIP%20Projects%20%28Points%20for%20display%20only%29/FeatureServer/0),
ArcGIS item `1ccd6a4f4f424a73b3b99c82052b8fcb`.

All 37 governed Watershed projects reconcile one-to-one by exact canonical
three-decimal CIP ID. The earlier apparent misses for IDs ending in zero were
an API-number formatting issue: for example, `10878.010` appeared as
`10878.01`. Decimal canonicalization resolves these without fuzzy matching.

The source-native points have feature `FME_DATE` values from
`2026-01-21T19:05:22.414Z` through `2026-01-21T19:05:24.635Z`, on the historical
snapshot date. The layer title also sets a vital semantic limit: these are
**display points**, not engineering footprints.

Richer secondary evidence exists for 29 Watershed projects:

- 26 exact-ID project shapes in the official
  [Capital Projects Explorer](https://capitalprojects.austintexas.gov/projects)
  API; and
- 15 exact-ID polygons in official
  [RNA Projects layer 8](https://maps.austintexas.gov/arcgis/rest/services/LongRangeCIP/RNAProjects/MapServer/8),
  with overlap between the two sets.

Those richer shapes were updated or captured after the January snapshot and
are preserved only as secondary candidates. They were not automatically
preferred over the historically aligned WPD display points.

Two projects are held:

- `watershed/5789.127` — the exact GIS CIP ID exists, but the GIS feature name
  describes West Bouldin/Hether storm-drain improvements while the governed
  name describes Zilker/Bluebonnet/Hether water-and-wastewater pipeline
  renewal. Exact ID supports HIGH identity confidence, but the scope difference
  prevents near-term promotion.
- `watershed/5789.150` — the official source-native display point is valid
  evidence, but the decision unit is a citywide renewal program. A single point
  remains unmapped until governance approves a display rule that cannot be read
  as the program's geographic extent.

## Transportation — 1 HIGH, 8 MEDIUM

`transportation/barton-springs-bridge` has a unique source-native polygon in
the official [Capital Projects Explorer](https://capitalprojects.austintexas.gov/projects)
under project ID `5873.031`, “Barton Springs Rd. Bridge over Barton Creek.”

The public CPE row was refreshed on August 19, 2026. The bridge location itself
is stable and can describe the January decision unit, but all later project
status or descriptive attributes must remain isolated from the historical
snapshot.

The other eight Transportation projects have strong official corridor or
bridge-asset identity evidence in the
[ACT Plan presentation](https://www.austintexas.gov/sites/default/files/files/Capital_Delivery/2026%20Bond%20Development/2025.11.19-2026-Bond--Complete-Streets-and-ACT-Plan-Presentation-BEATF.pdf),
the [official PRB record](https://services.austintexas.gov/edims/document.cfm?id=466344),
or the [bridge asset memorandum](https://services.austintexas.gov/edims/document.cfm?id=471428),
but no defensible source-native project line or footprint was found.

They remain MEDIUM and unmapped. A road-name midpoint would be fabricated. An
official corridor/polyline or bridge footprint is the appropriate future
evidence type.

## Parks & Open Space — 21 HIGH, 1 MEDIUM

The investigation used official City/PARD sources:

- [City park boundaries](https://services.arcgis.com/0L95CJ0VTaxqcmED/arcgis/rest/services/BOUNDARIES_city_of_austin_parks/FeatureServer/0),
  item `8a140d1a6bfc46a8b34d2ba3e1db1c9`;
- [PARD facility points](https://services.arcgis.com/0L95CJ0VTaxqcmED/arcgis/rest/services/pard_facility_points/FeatureServer/0),
  item `27aa5e7c4be74a439078b3fef086296c`; and
- [APR CIP project points](https://services.arcgis.com/0L95CJ0VTaxqcmED/arcgis/rest/services/APR_CIP_Points/FeatureServer/0),
  item `01518974d257431885f54906cfa545b9`.

Twenty-one projects have a unique, official park, facility asset, or capital
project feature. These are legitimate project-site/display candidates only
when their role remains explicit. A named park polygon is context for work at
that park; it is not automatically the capital project footprint.

`parks/bolm-maintenance-center` remains MEDIUM. Official
[PARD bond material](https://www.austintexas.gov/sites/default/files/files/Capital_Delivery/2026%20Bond%20Development/Bond%20Content/25-1008-2026-Bond---APR-Buildings-Rec-Centers--Aquatics-Programs.pdf)
ties the future central maintenance site to an approximately 10-acre reserved
area in northwest Bolm District Park, but the available GIS polygon covers the
entire roughly 68-acre park. Displaying the whole park as project geometry
would materially overstate the project site.

## Community Facilities — 17 HIGH, 4 MEDIUM, 2 LOW, 15 NO_MATCH

HIGH candidates cover unique official existing facilities or project sites
for:

- five ACME/cultural projects;
- Austin Animal Center;
- four unambiguous EMS locations;
- four numbered fire stations;
- Hampton and Milwood library branches; and
- Canyon Creek Northwest Police Substation.

Canyon Creek is the strongest parcel match. An official APD design record
identifies `9804 N FM 620 Rd` and parcel `0167370280`; the official
[TCAD parcel layer](https://services.arcgis.com/0L95CJ0VTaxqcmED/arcgis/rest/services/EXTERNAL_tcad_parcel/FeatureServer/0)
returns one source-native parcel polygon (`OBJECTID_1=284001`). The project
linkage is documented in the
[official APD design record](https://services.austintexas.gov/edims/document.cfm?id=381512).

MEDIUM candidates:

- Elisabet Ney Museum — unique museum site, but the governed restroom/storage
  scope spans multiple official asset features;
- Zilker Hillside Theatre — exact official address, but no source-native theatre
  geometry and no derived geocode was created;
- EMS Demand Station 1 — the governed `401 E 5th St` address conflicts with
  current/pre-snapshot official Demand 1 and EMS facility labels; and
- EMS Demand Station 2 — official sources conflict between `12010 Brodie Ln`
  and `415 W 2nd St`.

LOW candidates:

- Fire Education Building B; and
- Police Scenario Based Training Facility.

Both have plausible departmental campus context, but neither has a uniquely
proven project parcel or facility feature. LOW candidates are not suitable for
production pins.

The 15 NO_MATCH projects are predominantly proposed facilities, acquisition
programs, or new sites whose official sources do not establish a location.
Generic existing facilities were deliberately not substituted.

## Projects That Must Remain Explicitly Unmapped

Thirty-two projects require more evidence or conflict resolution:

### Watershed

- `watershed/5789.127` — exact-ID/name-scope conflict.
- `watershed/5789.150` — citywide-program display semantics unresolved.

### Transportation

- ACT Plan — 6th Street;
- ACT Plan — 7th Street;
- Delwau Lane Replacement;
- E. 7th Street;
- Hart Lane Retaining Walls;
- River Plantation Drive;
- West Slaughter Lane; and
- West William Cannon Drive Rehabilitation.

### Parks & Open Space

- Bolm Maintenance Center — whole-park polygon is too broad.

### Community Facilities

- Elisabet Ney Museum ADA Restroom and Storage Facility;
- Zilker Hillside Theatre;
- EMS Demand Stations 1, 2, and 9;
- Fire Education Building B;
- all four Fleet projects;
- North Austin Homeless Resource Center;
- Colony Park Branch Library;
- Municipal Court Customer Service Center;
- Police Air Operations Facility;
- Police Central West, Downtown, Northeast, and Southwest Substations;
- Police Scenario Based Training Facility;
- Colony Park Public Health Center; and
- Northeast Public Health Center.

## Ambiguity and Multiple-Feature Findings

- 8 rows have an identity, location, scope, extent, or display-semantics
  ambiguity.
- 39 rows have multiple possible authoritative features or geometry
  representations.
- The union is 42 rows; some rows are in both groups.

| Category | Ambiguity | Multiple features/representations | Union |
|---|---:|---:|---:|
| Watershed | 2 | 29 | 29 |
| Parks & Open Space | 1 | 2 | 3 |
| Transportation | 0 | 0 | 0 |
| Community Facilities | 5 | 8 | 10 |
| **Total** | **8** | **39** | **42** |

Most multiple-representation cases are not identity failures. In Watershed,
29 exact IDs have the historically aligned WPD point plus one or more later
polygon representations. The review question is which geometry semantics and
vintage to govern, not which project the source describes.

## Historical-Fit Assessment

Sources aligned at or before the January snapshot include:

- WPD display-point feature load: January 21, 2026;
- APR CIP item: January 13, 2026;
- fire stations: September 30, 2025;
- EMS stations: October 1, 2025;
- library branches: March 11, 2025; and
- the Canyon Creek APD design/parcel evidence: 2022 design record plus parcel
  service metadata from September 2025.

Sources with post-snapshot refreshes include:

- Capital Projects Explorer rows: August 19, 2026;
- RNA snapshot: September 1, 2026;
- park boundaries and PARD facility points: April 2026; and
- AFM managed facilities: June 2026.

Later refreshes do not automatically invalidate stable bridge, park, or
existing-facility locations. They do create a historical-snapshot concern:
only the stable location/geometry may be considered, and later project status,
scope, schedule, budget, or other attributes must not contaminate the January
decision snapshot. The CPE/RNA Watershed polygons should remain secondary
until their geometry vintage and representation semantics are explicitly
approved.

## Map Recommendation

1. **Production-ready candidate count:** 74 projects can defensibly proceed to
   governance review now. None is authorized in runtime yet.
2. **Needs more evidence:** 32 projects should remain explicitly unmapped.
3. **Strongest coverage:** Watershed is strongest by exact official project ID
   and snapshot-aligned display points; Parks is next for established named
   sites; Community Facilities is strong only for existing, uniquely identified
   facilities; Transportation remains weakest.
4. **Mixed geometry:** Support point, line, polygon, parcel, and address-derived
   representations with an explicit `display_role`. Do not convert lines or
   polygons into pins merely for UI uniformity.
5. **Unmapped behavior:** Show a clear “location not established in governed
   evidence” state. Never fall back to district/ZIP/neighborhood centroids or
   generic facilities.
6. **Historical concern:** Yes. CPE, RNA, park/PARD, and AFM sources include
   post-snapshot refreshes. Stable location may still be usable, but later
   project attributes and geometry evolution require isolation and review.

## Candidate Artifacts

- `data/reconnaissance/external_gis/2026-09-08/CANDIDATE_NOT_GOVERNED_project_geometry_reconciliation.csv`
- `data/reconnaissance/external_gis/2026-09-08/CANDIDATE_NOT_GOVERNED_summary.json`

The CSV contains exactly one row for each of the 106 governed
`decision_unit_id` values. Neither artifact is imported by or referenced from
the governed runtime.

## Verification

- 106 candidate rows read successfully.
- 106 unique `decision_unit_id` values.
- Category totals reconcile to 9 Transportation, 22 Parks & Open Space, 37
  Watershed, and 38 Community Facilities.
- Confidence totals reconcile to 106.
- Geometry-type totals reconcile to 106.
- Every row is labeled `CANDIDATE / RESEARCH / NOT YET GOVERNED`.
- Governed runtime remains 0 mapped / 106 unmapped with
  `fabricated_geometry=false`.
