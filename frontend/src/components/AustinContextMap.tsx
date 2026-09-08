import { useEffect, useMemo } from 'react'
import {
  CircleMarker,
  MapContainer,
  Polygon,
  TileLayer,
  Tooltip,
  ZoomControl,
  useMap,
} from 'react-leaflet'
import type {
  PublicConfiguration,
  RuntimeMapContext,
  RuntimeMapFeature,
} from '../api/contracts'
import { AppIcon } from './AppIcon'

interface AustinContextMapProps {
  mapContext: RuntimeMapContext
  publicConfiguration: PublicConfiguration
  visibleDecisionUnitIds: ReadonlySet<string>
  selectedDecisionUnitId: string | null
  onSelectProject: (decisionUnitId: string) => void
}

const AUSTIN_CENTER: [number, number] = [30.2672, -97.7431]

function displayRoleLabel(feature: RuntimeMapFeature): string {
  if (feature.properties.display_role === 'PROJECT_DISPLAY_POINT') {
    return 'Project location'
  }

  if (
    feature.properties.display_role === 'PROJECT_SITE' ||
    feature.properties.display_role === 'PROJECT_PARCEL'
  ) {
    return 'Project site'
  }

  if (feature.properties.display_role === 'PARK_SITE_CONTEXT') {
    return 'Park/site context'
  }

  return 'Facility/site context'
}

function roleClass(feature: RuntimeMapFeature): string {
  if (feature.properties.display_role === 'PROJECT_DISPLAY_POINT') {
    return 'map-feature-project'
  }

  if (
    feature.properties.display_role === 'PROJECT_SITE' ||
    feature.properties.display_role === 'PROJECT_PARCEL'
  ) {
    return 'map-feature-project-site'
  }

  if (feature.properties.display_role === 'PARK_SITE_CONTEXT') {
    return 'map-feature-park-context'
  }

  return 'map-feature-facility-context'
}

function polygonPositions(
  feature: RuntimeMapFeature,
): [number, number][][] | [number, number][][][] {
  if (feature.geometry.type === 'Polygon') {
    return feature.geometry.coordinates.map((ring) =>
      ring.map(([longitude, latitude]) => [latitude, longitude] as [number, number]),
    )
  }

  if (feature.geometry.type === 'MultiPolygon') {
    return feature.geometry.coordinates.map((polygon) =>
      polygon.map((ring) =>
        ring.map(
          ([longitude, latitude]) => [latitude, longitude] as [number, number],
        ),
      ),
    )
  }

  return []
}

function selectedFeatureBounds(
  feature: RuntimeMapFeature,
): Array<[number, number]> {
  if (feature.geometry.type === 'Point') {
    const [longitude, latitude] = feature.geometry.coordinates
    return [[latitude, longitude]]
  }

  const positions: Array<[number, number]> = []

  const collect = (value: unknown) => {
    if (
      Array.isArray(value) &&
      value.length === 2 &&
      typeof value[0] === 'number' &&
      typeof value[1] === 'number'
    ) {
      positions.push([value[1], value[0]])
      return
    }

    if (Array.isArray(value)) {
      value.forEach(collect)
    }
  }

  collect(feature.geometry.coordinates)
  return positions
}

function MapSelectionController({
  feature,
}: {
  feature: RuntimeMapFeature | null
}) {
  const map = useMap()

  useEffect(() => {
    if (feature === null) return

    if (feature.geometry.type === 'Point') {
      const [longitude, latitude] = feature.geometry.coordinates
      map.flyTo([latitude, longitude], Math.max(map.getZoom(), 13), {
        duration: 0.5,
      })
      return
    }

    const bounds = selectedFeatureBounds(feature)

    if (bounds.length > 0) {
      map.fitBounds(bounds, {
        padding: [40, 40],
        maxZoom: 14,
      })
    }
  }, [feature, map])

  return null
}

function MapResizeController() {
  const map = useMap()

  useEffect(() => {
    const invalidate = () => map.invalidateSize({ pan: false })
    invalidate()

    if (typeof ResizeObserver !== 'undefined') {
      const observer = new ResizeObserver(invalidate)
      observer.observe(map.getContainer())
      return () => observer.disconnect()
    }

    window.addEventListener('resize', invalidate)
    return () => window.removeEventListener('resize', invalidate)
  }, [map])

  return null
}

export function AustinContextMap({
  mapContext,
  publicConfiguration,
  visibleDecisionUnitIds,
  selectedDecisionUnitId,
  onSelectProject,
}: AustinContextMapProps) {
  const visibleFeatures = useMemo(
    () =>
      mapContext.features.filter((feature) =>
        visibleDecisionUnitIds.has(feature.properties.decision_unit_id),
      ),
    [mapContext.features, visibleDecisionUnitIds],
  )

  const selectedFeature = useMemo(
    () =>
      selectedDecisionUnitId === null
        ? null
        : visibleFeatures.find(
            (feature) =>
              feature.properties.decision_unit_id === selectedDecisionUnitId,
          ) ?? null,
    [selectedDecisionUnitId, visibleFeatures],
  )

  const orderedFeatures = useMemo(
    () => [
      ...visibleFeatures.filter(
        (feature) =>
          feature.properties.decision_unit_id !== selectedDecisionUnitId,
      ),
      ...visibleFeatures.filter(
        (feature) =>
          feature.properties.decision_unit_id === selectedDecisionUnitId,
      ),
    ],
    [selectedDecisionUnitId, visibleFeatures],
  )

  return (
    <section className="map-panel" aria-labelledby="map-heading">
      <div className="map-heading-row">
        <div>
          <p className="eyebrow">Austin project map</p>
          <h2 id="map-heading">Explore project locations</h2>
        </div>

        <details className="map-layers-control">
          <summary>
            <AppIcon name="layers" size={17} />
            Layers
          </summary>

          <div className="map-layers-popover">
            <strong>Map legend</strong>

            <span className="layer-row">
              <span
                className="layer-swatch layer-swatch-project"
                aria-hidden="true"
              />
              Project location
              <small>Governed</small>
            </span>

            <span className="layer-row">
              <span
                className="layer-swatch layer-swatch-facility"
                aria-hidden="true"
              />
              Facility/site context
              <small>Context</small>
            </span>

            <span className="layer-row">
              <span
                className="layer-swatch layer-swatch-park"
                aria-hidden="true"
              />
              Park/site context
              <small>Context</small>
            </span>

            <span className="layer-row layer-row-selected">
              <span
                className="layer-swatch layer-swatch-selected"
                aria-hidden="true"
              />
              Selected project
              <small>Focused</small>
            </span>

            <p>
              Context geometry identifies an official facility, park, parcel, or
              site. It must not be interpreted as a capital-project construction
              footprint.
            </p>
          </div>
        </details>
      </div>

      <div className="austin-map-frame">
        <div className="map-canvas">
          <div className="map-neutral-fallback" aria-hidden="true" />

          <MapContainer
            center={AUSTIN_CENTER}
            zoom={11}
            minZoom={9}
            maxZoom={15}
            scrollWheelZoom={false}
            zoomControl={false}
            attributionControl
            className="austin-map"
          >
            <TileLayer
              url={publicConfiguration.osm_tile_url}
              attribution={publicConfiguration.osm_attribution}
            />

            {orderedFeatures.map((feature) => {
              const selected =
                feature.properties.decision_unit_id === selectedDecisionUnitId
              const className = [
                'governed-map-feature',
                roleClass(feature),
                selected ? 'governed-map-feature-selected' : '',
              ]
                .filter(Boolean)
                .join(' ')

              if (feature.geometry.type === 'Point') {
                const [longitude, latitude] = feature.geometry.coordinates

                return (
                  <CircleMarker
                    key={feature.id}
                    center={[latitude, longitude]}
                    radius={selected ? 9 : 6}
                    pathOptions={{ className }}
                    eventHandlers={{
                      click: () =>
                        onSelectProject(feature.properties.decision_unit_id),
                    }}
                  >
                    <Tooltip>
                      <strong>{feature.properties.governed_name}</strong>
                      <br />
                      {displayRoleLabel(feature)}
                    </Tooltip>
                  </CircleMarker>
                )
              }

              return (
                <Polygon
                  key={feature.id}
                  positions={polygonPositions(feature)}
                  pathOptions={{ className }}
                  eventHandlers={{
                    click: () =>
                      onSelectProject(feature.properties.decision_unit_id),
                  }}
                >
                  <Tooltip>
                    <strong>{feature.properties.governed_name}</strong>
                    <br />
                    {displayRoleLabel(feature)}
                  </Tooltip>
                </Polygon>
              )
            })}

            <MapSelectionController feature={selectedFeature} />
            <MapResizeController />
            <ZoomControl position="bottomright" />
          </MapContainer>
        </div>

        <div className="map-location-card" role="note">
          <div className="map-location-icon" aria-hidden="true">
            <AppIcon name="map" size={20} />
          </div>

          <div>
            <strong>Governed project geography</strong>
            <span>
              {mapContext.mapped_project_count} mapped ·{' '}
              {mapContext.unmapped_project_count} location unavailable
            </span>
            <p>
              Showing {visibleFeatures.length} mapped result
              {visibleFeatures.length === 1 ? '' : 's'}. Only approved
              source-native geometry is shown; projects without it remain in the
              list.
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}
