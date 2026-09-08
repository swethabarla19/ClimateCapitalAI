import type { BootstrapSuccessEnvelope } from '../api/contracts'
import {
  cloneFundingPlanInput,
  createInitialSession,
  runtimeIdentityFromBootstrap,
  type BrowserSessionState,
  type PresentationState,
} from './contracts'
import {
  clearSession,
  loadStoredSessionCandidate,
  saveSession,
} from './storage'

export type SessionInitializationStatus =
  | 'NEW'
  | 'RESTORED_INPUTS'
  | 'RESET_INVALID'
  | 'RESET_STALE'

export interface SessionInitializationResult {
  status: SessionInitializationStatus
  session: BrowserSessionState
}

function clonePresentation(
  value: PresentationState,
): PresentationState {
  return {
    ...value,
    filter_ids: [...value.filter_ids],
  }
}

function safePresentationAcrossRelease(
  fresh: PresentationState,
  stored: PresentationState,
): PresentationState {
  return {
    ...fresh,
    route: stored.route,
    search_text: stored.search_text,
    sort: stored.sort,
  }
}

export function initializeSessionFromBootstrap(
  bootstrap: BootstrapSuccessEnvelope,
): SessionInitializationResult {
  const fresh = createInitialSession(bootstrap)
  const stored = loadStoredSessionCandidate(
    runtimeIdentityFromBootstrap(bootstrap),
  )

  if (stored.status === 'MISSING') {
    saveSession(fresh)
    return { status: 'NEW', session: fresh }
  }

  if (stored.status === 'INVALID') {
    clearSession()
    saveSession(fresh)
    return { status: 'RESET_INVALID', session: fresh }
  }

  if (stored.status === 'STALE') {
    const reset: BrowserSessionState = {
      ...fresh,
      presentation: safePresentationAcrossRelease(
        fresh.presentation,
        stored.session.presentation,
      ),
    }

    clearSession()
    saveSession(reset)
    return { status: 'RESET_STALE', session: reset }
  }

  const restored: BrowserSessionState = {
    ...fresh,
    presentation: clonePresentation(stored.session.presentation),
    working_plan: {
      ...cloneFundingPlanInput(stored.session.working_plan),
      data_version: fresh.runtime_identity.data_version,
      expected_fingerprint: null,
    },
  }

  saveSession(restored)

  return {
    status: 'RESTORED_INPUTS',
    session: restored,
  }
}
