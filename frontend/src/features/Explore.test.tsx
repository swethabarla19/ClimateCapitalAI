import { useState } from 'react'
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it } from 'vitest'
import { createInitialSession } from '../session/contracts'
import { SESSION_STORAGE_KEY } from '../session/storage'
import { bootstrapFixture } from '../test/bootstrapFixture'
import { Explore } from './Explore'

function Harness() {
  const bootstrap = bootstrapFixture()
  const [session, setSession] = useState(() => createInitialSession(bootstrap))

  return (
    <Explore
      catalog={bootstrap.data.catalog}
      mapContext={bootstrap.data.map_context}
      publicConfiguration={bootstrap.data.public_configuration}
      session={session}
      onSessionChange={setSession}
    />
  )
}

function projectButtons(): HTMLElement[] {
  return screen.getAllByRole('button', { name: /view details for/i })
}

beforeEach(() => window.sessionStorage.clear())

describe('Explore', () => {
  it('renders all 106 governed projects and exact category counts', () => {
    render(<Harness />)

    expect(projectButtons()).toHaveLength(106)
    expect(screen.getByLabelText('106 of 106 projects')).toBeInTheDocument()

    const categorySummary = screen.getByRole('region', {
      name: /project category counts/i,
    })
    expect(categorySummary).toHaveTextContent('Transportation 9')
    expect(categorySummary).toHaveTextContent('Parks & Open Space 22')
    expect(categorySummary).toHaveTextContent('Watershed 37')
    expect(categorySummary).toHaveTextContent('Community Facilities 38')
  })

  it('combines category filtering and project-name search predictably', async () => {
    const user = userEvent.setup()
    render(<Harness />)

    await user.selectOptions(screen.getByLabelText('Category'), 'Watershed')
    expect(projectButtons()).toHaveLength(37)

    await user.type(
      screen.getByLabelText('Search project name'),
      'Watershed fixture project 9',
    )

    expect(projectButtons()).toHaveLength(1)
    expect(projectButtons()[0]).toHaveAccessibleName(
      'View details for Watershed fixture project 9',
    )
  })

  it('filters by competition-rank range without renumbering projects', async () => {
    const user = userEvent.setup()
    render(<Harness />)

    await user.selectOptions(
      screen.getByLabelText('Funding Priority'),
      'TOP_10',
    )

    expect(projectButtons()).toHaveLength(25)
    expect(screen.getByLabelText('25 of 106 projects')).toBeInTheDocument()
    expect(projectButtons()[0]).toHaveTextContent('83 · Rank 1')
    expect(projectButtons()[1]).toHaveTextContent('77 · Rank 2')
  })

  it('sorts by Funding Priority by default and request amount in both directions', async () => {
    const user = userEvent.setup()
    render(<Harness />)

    expect(projectButtons()[0]).toHaveAccessibleName(
      'View details for Transportation fixture project 1',
    )

    await user.selectOptions(
      screen.getByLabelText('Sort projects'),
      'REQUEST_DESC',
    )
    expect(projectButtons()[0]).toHaveAccessibleName(
      'View details for Community Facilities fixture project 38',
    )

    await user.selectOptions(
      screen.getByLabelText('Sort projects'),
      'REQUEST_ASC',
    )
    expect(projectButtons()[0]).toHaveAccessibleName(
      'View details for Transportation fixture project 1',
    )
  })

  it('preserves shared competition rank and half-point score presentation', async () => {
    const user = userEvent.setup()
    render(<Harness />)

    const tiedProject = screen.getByRole('button', {
      name: 'View details for Transportation fixture project 2',
    })
    expect(tiedProject).toHaveTextContent('77 · Rank 2')
    expect(tiedProject).toHaveTextContent('Shared rank · 4 projects')

    await user.click(
      screen.getByRole('button', {
        name: 'View details for Parks & Open Space fixture project 17',
      }),
    )

    const detail = screen.getByRole('complementary', {
      name: 'Parks & Open Space fixture project 17',
    })
    expect(detail).toHaveTextContent('54.5')
    expect(detail).toHaveTextContent('Rank 26')
  })

  it('selects by decision_unit_id and shows all six official PRB components', async () => {
    const user = userEvent.setup()
    render(<Harness />)

    await user.click(
      screen.getByRole('button', {
        name: 'View details for Transportation fixture project 1',
      }),
    )

    const detail = screen.getByRole('complementary', {
      name: 'Transportation fixture project 1',
    })
    expect(detail).toHaveTextContent('transportation/fixture/project-1')

    for (const [component, maximum] of [
      ['Strategic Alignment', 8],
      ['Critical Asset', 8],
      ['Community Consideration', 20],
      ['Efficiency', 20],
      ['Timeliness & Readiness', 24],
      ['Climate Resilience', 20],
    ] as const) {
      expect(within(detail).getByText(component)).toBeInTheDocument()
      expect(
        within(detail).getByRole('progressbar', {
          name: new RegExp(`^${component}:`),
        }),
      ).toHaveAttribute('max', String(maximum))
    }

    expect(within(detail).getAllByRole('progressbar')).toHaveLength(6)

    const stored = JSON.parse(
      window.sessionStorage.getItem(SESSION_STORAGE_KEY) ?? '{}',
    )
    expect(stored.presentation.selected_decision_unit_id).toBe(
      'transportation/fixture/project-1',
    )
  })

  it('shows an Austin context map with truthful zero-geometry treatment and no pins', () => {
    render(<Harness />)

    expect(
      screen.getByRole('heading', { name: /explore the city/i }),
    ).toBeInTheDocument()
    expect(screen.getByText(/0 mapped · 106 unmapped/i)).toBeInTheDocument()
    expect(screen.getByText(/pins are withheld/i)).toBeInTheDocument()
    expect(screen.queryByRole('img', { name: /project map/i })).toBeNull()
    expect(document.querySelector('.leaflet-marker-icon')).toBeNull()
  })

  it('shows a distinct no-results state and clears all filters', async () => {
    const user = userEvent.setup()
    render(<Harness />)

    await user.type(
      screen.getByLabelText('Search project name'),
      'not a governed project',
    )

    expect(
      screen.getByRole('heading', { name: /no projects match/i }),
    ).toBeInTheDocument()

    await user.click(
      within(screen.getByRole('status')).getByRole('button', {
        name: 'Clear filters',
      }),
    )

    expect(projectButtons()).toHaveLength(106)
    expect(screen.getByLabelText('Search project name')).toHaveValue('')
  })

  it('filters governed request amounts using non-overlapping ranges', async () => {
    const user = userEvent.setup()
    render(<Harness />)

    await user.selectOptions(
      screen.getByLabelText('Governed request'),
      '50M_PLUS',
    )

    expect(projectButtons()).toHaveLength(1)
    expect(projectButtons()[0]).toHaveTextContent('$100,000,000')
  })
})
