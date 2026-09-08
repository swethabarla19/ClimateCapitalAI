import type {
  BrowserSessionState,
  PresentationState,
} from './contracts'
import { saveSession } from './storage'

export function setPresentationRoute(
  session: BrowserSessionState,
  route: PresentationState['route'],
): BrowserSessionState {
  const next: BrowserSessionState = {
    ...session,
    presentation: {
      ...session.presentation,
      route,
    },
  }

  saveSession(next)
  return next
}
