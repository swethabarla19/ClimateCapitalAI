import type { ReactNode } from 'react'
import { fireEvent, render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { bootstrapFixture } from '../test/bootstrapFixture'
import { AustinContextMap } from './AustinContextMap'

const mapApi = vi.hoisted(() => ({
  fitBounds: vi.fn(),
  flyTo: vi.fn(),
  getContainer: vi.fn(() => document.createElement('div')),
  getZoom: vi.fn(() => 11),
  invalidateSize: vi.fn(),
}))

interface MockContainerProps {
  children?: ReactNode
  className?: string
}

interface MockFeatureProps {
  children?: ReactNode
  eventHandlers?: { click?: () => void }
  pathOptions?: { className?: string }
}

vi.mock('react-leaflet', () => ({
  CircleMarker: ({ children, eventHandlers, pathOptions }: MockFeatureProps) => (
    <button
      type="button"
      data-testid="governed-map-feature"
      data-feature-class={pathOptions?.className}
      onClick={eventHandlers?.click}
    >
      {children}
    </button>
  ),
  MapContainer: ({ children, className }: MockContainerProps) => (
    <div className={className}>{children}</div>
  ),
  Polygon: ({ children, eventHandlers, pathOptions }: MockFeatureProps) => (
    <button
      type="button"
      data-testid="governed-map-feature"
      data-feature-class={pathOptions?.className}
      onClick={eventHandlers?.click}
    >
      {children}
    </button>
  ),
  TileLayer: () => null,
  Tooltip: ({ children }: MockContainerProps) => <span>{children}</span>,
  ZoomControl: () => null,
  useMap: () => mapApi,
}))

function renderMap(
  selectedDecisionUnitId: string | null,
  visibleDecisionUnitIds?: ReadonlySet<string>,
) {
  const bootstrap = bootstrapFixture()
  const visible =
    visibleDecisionUnitIds ??
    new Set(
      bootstrap.data.catalog.projects.map((project) => project.decision_unit_id),
    )
  const onSelectProject = vi.fn()

  render(
    <AustinContextMap
      mapContext={bootstrap.data.map_context}
      publicConfiguration={bootstrap.data.public_configuration}
      visibleDecisionUnitIds={visible}
      selectedDecisionUnitId={selectedDecisionUnitId}
      onSelectProject={onSelectProject}
    />,
  )

  return { bootstrap, onSelectProject }
}

beforeEach(() => {
  vi.clearAllMocks()
})

describe('AustinContextMap', () => {
  it('renders only filtered governed features with distinct role classes', () => {
    const bootstrap = bootstrapFixture()
    const features = bootstrap.data.map_context.features
    const chosen = [features[0], features[42], features[64], features[72]]
    const visible = new Set(
      chosen.map((feature) => feature!.properties.decision_unit_id),
    )

    renderMap(null, visible)

    const rendered = screen.getAllByTestId('governed-map-feature')
    expect(rendered).toHaveLength(4)
    expect(rendered[0]).toHaveAttribute(
      'data-feature-class',
      expect.stringContaining('map-feature-project'),
    )
    expect(rendered[1]).toHaveAttribute(
      'data-feature-class',
      expect.stringContaining('map-feature-facility-context'),
    )
    expect(rendered[2]).toHaveAttribute(
      'data-feature-class',
      expect.stringContaining('map-feature-park-context'),
    )
    expect(rendered[3]).toHaveAttribute(
      'data-feature-class',
      expect.stringContaining('map-feature-project-site'),
    )
    expect(screen.getByText(/showing 4 mapped results/i)).toBeInTheDocument()
  })

  it('selects a project from governed map geometry', () => {
    const { onSelectProject } = renderMap(null)

    fireEvent.click(
      screen.getByRole('button', {
        name: /transportation fixture project 1project location/i,
      }),
    )

    expect(onSelectProject).toHaveBeenCalledWith(
      'transportation/fixture/project-1',
    )
  })

  it('focuses selected point and polygon geometry and raises its visual state', () => {
    const pointId = 'transportation/fixture/project-1'
    const { unmount } = render(
      <AustinContextMap
        mapContext={bootstrapFixture().data.map_context}
        publicConfiguration={bootstrapFixture().data.public_configuration}
        visibleDecisionUnitIds={new Set([pointId])}
        selectedDecisionUnitId={pointId}
        onSelectProject={() => undefined}
      />,
    )

    expect(mapApi.flyTo).toHaveBeenCalledWith(
      expect.any(Array),
      13,
      expect.objectContaining({ duration: 0.5 }),
    )
    expect(screen.getByTestId('governed-map-feature')).toHaveAttribute(
      'data-feature-class',
      expect.stringContaining('governed-map-feature-selected'),
    )

    unmount()
    vi.clearAllMocks()

    const bootstrap = bootstrapFixture()
    const polygonId =
      bootstrap.data.map_context.features[64]!.properties.decision_unit_id
    renderMap(polygonId, new Set([polygonId]))

    expect(mapApi.fitBounds).toHaveBeenCalledWith(
      expect.any(Array),
      expect.objectContaining({ maxZoom: 14 }),
    )
  })

  it('does not move the map when the selected project has no governed geometry', () => {
    renderMap('community-facilities/fixture/project-38')

    expect(mapApi.flyTo).not.toHaveBeenCalled()
    expect(mapApi.fitBounds).not.toHaveBeenCalled()
    expect(mapApi.invalidateSize).toHaveBeenCalledWith({ pan: false })
  })
})
