import type { PresentationCategory } from '../api/contracts'
import type {
  BrowserSessionState,
  PresentationState,
} from './contracts'
import { saveSession } from './storage'

export type CategoryFilter = 'ALL' | PresentationCategory
export type PriorityFilter = 'ALL' | 'TOP_10' | 'TOP_25' | 'TOP_50'
export type RequestAmountFilter =
  | 'ALL'
  | 'UNDER_5M'
  | '5M_TO_20M'
  | '20M_TO_50M'
  | '50M_PLUS'

export interface ExploreFilters {
  category: CategoryFilter
  priority: PriorityFilter
  requestAmount: RequestAmountFilter
}

const categoryPrefix = 'category:'
const priorityPrefix = 'priority:'
const requestPrefix = 'request:'

function filterValue<T extends string>(
  filterIds: string[],
  prefix: string,
  allowed: readonly T[],
): T | 'ALL' {
  const encoded = filterIds.find((filterId) => filterId.startsWith(prefix))
  const value = encoded?.slice(prefix.length)

  return value !== undefined && allowed.includes(value as T)
    ? (value as T)
    : 'ALL'
}

export function readExploreFilters(
  presentation: PresentationState,
): ExploreFilters {
  return {
    category: filterValue(
      presentation.filter_ids,
      categoryPrefix,
      [
        'Transportation',
        'Parks & Open Space',
        'Watershed',
        'Community Facilities',
      ] as const,
    ),
    priority: filterValue(
      presentation.filter_ids,
      priorityPrefix,
      ['TOP_10', 'TOP_25', 'TOP_50'] as const,
    ),
    requestAmount: filterValue(
      presentation.filter_ids,
      requestPrefix,
      ['UNDER_5M', '5M_TO_20M', '20M_TO_50M', '50M_PLUS'] as const,
    ),
  }
}

function updatePresentation(
  session: BrowserSessionState,
  presentation: PresentationState,
): BrowserSessionState {
  const next = { ...session, presentation }
  saveSession(next)
  return next
}

function replaceFilter(
  filterIds: string[],
  prefix: string,
  value: string,
): string[] {
  const retained = filterIds.filter((filterId) => !filterId.startsWith(prefix))
  return value === 'ALL' ? retained : [...retained, `${prefix}${value}`]
}

export function setExploreSearch(
  session: BrowserSessionState,
  searchText: string,
): BrowserSessionState {
  return updatePresentation(session, {
    ...session.presentation,
    search_text: searchText,
  })
}

export function setExploreCategoryFilter(
  session: BrowserSessionState,
  category: CategoryFilter,
): BrowserSessionState {
  return updatePresentation(session, {
    ...session.presentation,
    filter_ids: replaceFilter(
      session.presentation.filter_ids,
      categoryPrefix,
      category,
    ),
  })
}

export function setExplorePriorityFilter(
  session: BrowserSessionState,
  priority: PriorityFilter,
): BrowserSessionState {
  return updatePresentation(session, {
    ...session.presentation,
    filter_ids: replaceFilter(
      session.presentation.filter_ids,
      priorityPrefix,
      priority,
    ),
  })
}

export function setExploreRequestAmountFilter(
  session: BrowserSessionState,
  requestAmount: RequestAmountFilter,
): BrowserSessionState {
  return updatePresentation(session, {
    ...session.presentation,
    filter_ids: replaceFilter(
      session.presentation.filter_ids,
      requestPrefix,
      requestAmount,
    ),
  })
}

export function setExploreSort(
  session: BrowserSessionState,
  sort: PresentationState['sort'],
): BrowserSessionState {
  return updatePresentation(session, {
    ...session.presentation,
    sort,
  })
}

export function selectExploreProject(
  session: BrowserSessionState,
  decisionUnitId: string | null,
): BrowserSessionState {
  return updatePresentation(session, {
    ...session.presentation,
    selected_decision_unit_id: decisionUnitId,
  })
}

export function resetExploreFilters(
  session: BrowserSessionState,
): BrowserSessionState {
  return updatePresentation(session, {
    ...session.presentation,
    search_text: '',
    filter_ids: [],
  })
}
