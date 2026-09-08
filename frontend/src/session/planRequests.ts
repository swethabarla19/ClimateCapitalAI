import {
  ApiClientError,
  evaluateFundingPlan,
} from '../api/client'
import type {
  FundingPlanInput,
  FundingPlanSuccessEnvelope,
} from '../api/contracts'

export type FundingPlanEvaluator = (
  input: FundingPlanInput,
  signal?: AbortSignal,
) => Promise<FundingPlanSuccessEnvelope>

export interface PlanRequestHandlers {
  onSuccess: (
    response: FundingPlanSuccessEnvelope,
    generation: number,
  ) => void
  onFailure: (error: unknown, generation: number) => void
  onCancelled?: (generation: number) => void
}

/**
 * Owns the in-flight plan request for one mounted workflow.
 *
 * Aborting saves backend/browser work; the generation check is the authority
 * that prevents a late response from an abort-insensitive transport from being
 * applied to newer analyst inputs.
 */
export class PlanRequestCoordinator {
  private controller: AbortController | null = null
  private latestGeneration = 0
  private readonly evaluator: FundingPlanEvaluator

  constructor(
    evaluator: FundingPlanEvaluator = evaluateFundingPlan,
  ) {
    this.evaluator = evaluator
  }

  evaluate(
    input: FundingPlanInput,
    generation: number,
    handlers: PlanRequestHandlers,
  ): void {
    this.controller?.abort()
    this.controller = new AbortController()
    this.latestGeneration = generation
    const controller = this.controller

    void this.evaluator(input, controller.signal)
      .then((response) => {
        if (
          controller.signal.aborted ||
          generation !== this.latestGeneration
        ) {
          return
        }

        handlers.onSuccess(response, generation)
      })
      .catch((error: unknown) => {
        if (
          controller.signal.aborted ||
          generation !== this.latestGeneration ||
          (error instanceof ApiClientError &&
            error.kind === 'REQUEST_ABORTED')
        ) {
          handlers.onCancelled?.(generation)
          return
        }

        handlers.onFailure(error, generation)
      })
  }

  cancel(): void {
    this.controller?.abort()
    this.controller = null
  }
}
