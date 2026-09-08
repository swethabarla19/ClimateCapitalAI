import { MapContainer, TileLayer, ZoomControl } from 'react-leaflet'
import type { PublicConfiguration, RuntimeMapContext } from '../api/contracts'
import { AppIcon } from './AppIcon'

interface AustinContextMapProps {
  mapContext: RuntimeMapContext
  publicConfiguration: PublicConfiguration
}

const AUSTIN_CENTER: [number, number] = [30.2672, -97.7431]

export function AustinContextMap({
  mapContext,
  publicConfiguration,
}: AustinContextMapProps) {
  return (
    <section className="map-panel" aria-labelledby="map-heading">
      <div className="map-heading-row">
        <div>
          <p className="eyebrow">Austin context map</p>
          <h2 id="map-heading">Explore the city</h2>
        </div>
        <details className="map-layers-control">
          <summary>
            <AppIcon name="layers" size={17} />
            Layers
          </summary>
          <div className="map-layers-popover">
            <strong>Map layers</strong>
            <span className="layer-row">
              <span className="layer-swatch layer-swatch-map" aria-hidden="true" />
              Austin basemap
              <small>Visible</small>
            </span>
            <span className="layer-row layer-row-unavailable">
              <span className="layer-swatch" aria-hidden="true" />
              Governed project locations
              <small>Unavailable</small>
            </span>
            <p>
              The governed runtime contains no trustworthy project geometry or
              supported contextual overlays. No locations are inferred.
            </p>
          </div>
        </details>
      </div>

      <div className="austin-map-frame">
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
          <ZoomControl position="bottomright" />
        </MapContainer>

        <div className="map-location-card" role="note">
          <div className="map-location-icon" aria-hidden="true">
            <AppIcon name="map" size={20} />
          </div>
          <div>
            <strong>Project locations not shown</strong>
            <span>
              {mapContext.mapped_project_count} mapped ·{' '}
              {mapContext.unmapped_project_count} unmapped
            </span>
            <p>
              Use the project list for the complete governed portfolio. Pins are
              withheld because this release has no supported project coordinates.
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}
