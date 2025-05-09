/*************************************************************************************************

Welcome to Baml! To use this generated code, please run one of the following:

$ npm install @boundaryml/baml
$ yarn add @boundaryml/baml
$ pnpm add @boundaryml/baml

*************************************************************************************************/

// This file was generated by BAML: do not edit it. Instead, edit the BAML
// files and re-generate this code.
//
/* eslint-disable */
// tslint:disable
// @ts-nocheck
// biome-ignore format: autogenerated code
'use client'

import type { BamlErrors } from '@boundaryml/baml/errors'
import { toBamlError } from '@boundaryml/baml/errors'
import { useCallback, useMemo, useReducer, useTransition } from 'react'
import * as Actions from './server'
import * as StreamingActions from './server_streaming'
import type { StreamingServerTypes } from './server_streaming_types'

/**
 * Type representing a BAML stream response.
 *
 * @template PartialType The type of the partial response.
 * @template FinalType The type of the final response.
 */
type BamlStreamResponse<PartialType, FinalType> = {
  partial?: PartialType
  final?: FinalType
  error?: BamlErrors
}

/**
 * A server action that returns either a ReadableStream of Uint8Array or a final output.
 */
export type ServerAction<Input = any, Output = any> = (
  ...args: Input extends any[] ? Input : [Input]
) => Promise<Output> | ReadableStream<Uint8Array>

/**
 * Type representing all function names except 'stream' and 'stream_types'
 */
export type FunctionNames = keyof typeof Actions

/**
 * Helper type to derive the partial return type for an action.
 */
type StreamDataType<FunctionName extends FunctionNames> = StreamingServerTypes[FunctionName]

/**
 * Helper type to derive the final return type for an action.
 */
type FinalDataType<FunctionName extends FunctionNames> = (typeof Actions)[FunctionName] extends (...args: any) => any
  ? Awaited<ReturnType<(typeof Actions)[FunctionName]>>
  : never

/**
 * Configuration options for BAML React hooks.
 */
export type HookInput<FunctionName extends FunctionNames, Options extends { stream?: boolean } = { stream?: true }> = {
  stream?: Options['stream']
  onStreamData?: Options['stream'] extends false ? never : (response?: StreamDataType<FunctionName>) => void
  onFinalData?: (response?: FinalDataType<FunctionName>) => void
  onData?: (response?: Options['stream'] extends false ? FinalDataType<FunctionName> : FinalDataType<FunctionName> | StreamDataType<FunctionName>) => void
  onError?: (error: BamlErrors) => void
}

export type NonStreamingHookStatus = 'idle' | 'pending' | 'success' | 'error'
export type StreamingHookStatus = NonStreamingHookStatus | 'streaming'

export type HookStatus<Options extends { stream?: boolean } = { stream?: true }> = Options['stream'] extends false
  ? NonStreamingHookStatus
  : StreamingHookStatus

/**
 * Return type for BAML React hooks.
 */
export type HookOutput<FunctionName extends FunctionNames, Options extends { stream?: boolean } = { stream?: true }> = {
  data?: Options['stream'] extends false ? FinalDataType<FunctionName> : FinalDataType<FunctionName> | StreamDataType<FunctionName>
  finalData?: FinalDataType<FunctionName>
  streamData?: Options['stream'] extends false ? never : StreamDataType<FunctionName>
  isLoading: boolean
  isPending: boolean
  isStreaming: Options['stream'] extends false ? never : boolean
  isSuccess: boolean
  isError: boolean
  error?: BamlErrors
  status: HookStatus<Options>
  mutate: (
    ...args: Parameters<(typeof Actions)[FunctionName]>
  ) => Options['stream'] extends false ? Promise<FinalDataType<FunctionName>> : Promise<ReadableStream<Uint8Array>>
  reset: () => void
}

/**
 * Type guard to check if the hook props are configured for streaming mode.
 *
 * @template FunctionName - The name of the BAML function.
 * @param props - The hook props.
 * @returns {boolean} True if the props indicate streaming mode.
 */
function isStreamingProps<FunctionName extends FunctionNames>(
  props: HookInput<FunctionName, { stream?: boolean }>,
): props is HookInput<FunctionName, { stream?: true }> {
  return props.stream !== false
}

/**
 * Type guard to check if the hook props are configured for non‑streaming mode.
 *
 * @template FunctionName - The name of the BAML function.
 * @param props - The hook props.
 * @returns {boolean} True if the props indicate non‑streaming mode.
 */
function isNotStreamingProps<FunctionName extends FunctionNames>(
  props: HookInput<FunctionName, { stream?: boolean }>,
): props is HookInput<FunctionName, { stream: false }> {
  return props.stream === false
}

interface HookState<TPartial, TFinal> {
  isSuccess: boolean
  isStreaming: boolean
  error?: BamlErrors
  finalData?: TFinal
  streamData?: TPartial
}

type HookStateAction<TPartial, TFinal> =
  | { type: 'START_REQUEST' }
  | { type: 'SET_ERROR'; payload: BamlErrors }
  | { type: 'SET_PARTIAL'; payload: TPartial }
  | { type: 'SET_FINAL'; payload: TFinal }
  | { type: 'RESET' }

/**
 * Reducer function to manage the hook state transitions.
 *
 * @template TPartial - The type of the partial (streaming) data.
 * @template TFinal - The type of the final (non‑streaming) data.
 * @param state - The current hook state.
 * @param action - The action to apply.
 * @returns The updated state.
 */
function hookReducer<TPartial, TFinal>(
  state: HookState<TPartial, TFinal>,
  action: HookStateAction<TPartial, TFinal>,
): HookState<TPartial, TFinal> {
  switch (action.type) {
    case 'START_REQUEST':
      return {
        ...state,
        isSuccess: false,
        error: undefined,
        isStreaming: false,
        finalData: undefined,
        streamData: undefined,
      }
    case 'SET_ERROR':
      return {
        ...state,
        isSuccess: false,
        isStreaming: false,
        error: action.payload,
      }
    case 'SET_PARTIAL':
      return {
        ...state,
        isStreaming: true,
        streamData: action.payload,
      }
    case 'SET_FINAL':
      return {
        ...state,
        isSuccess: true,
        isStreaming: false,
        finalData: action.payload,
      }
    case 'RESET':
      return {
        isSuccess: false,
        isStreaming: false,
        error: undefined,
        finalData: undefined,
        streamData: undefined,
      }
    default:
      return state
  }
}

/**
 * Base hook for executing BAML server actions, supporting both streaming and non‑streaming modes.
 *
 * This hook provides a unified interface for handling loading states, partial updates, errors,
 * and final responses. It is designed to be used directly with any BAML server action.
 *
 * Features:
 * - **Streaming Support:** Real‑time partial updates via `streamData`, progress indicators, and incremental UI updates.
 * - **State Management:** Manages loading state (`isLoading`), success/error flags, and final/partial results.
 * - **Error Handling:** Supports type‑safe error handling for BamlValidationError, BamlClientFinishReasonError, and standard errors.
 *
 * @param Action - The server action to invoke.
 * @param props - Configuration props for the hook.
 * @returns An object with the current state and a `mutate` function to trigger the action.
 *
 * @example
 * ```tsx
 * const { data, error, isLoading, mutate } = useBamlAction(StreamingActions.TestAws, { stream: true });
 * ```
 */
 function useBamlAction<FunctionName extends FunctionNames>(
  action: ServerAction,
  props: HookInput<FunctionName, { stream: false }>,
): HookOutput<FunctionName, { stream: false }>
function useBamlAction<FunctionName extends FunctionNames>(
  action: ServerAction,
  props?: HookInput<FunctionName, { stream?: true }>,
): HookOutput<FunctionName, { stream: true }>
function useBamlAction<FunctionName extends FunctionNames>(
  action: ServerAction,
  props: HookInput<FunctionName, { stream?: boolean }> = {},
): HookOutput<FunctionName, { stream: true }> | HookOutput<FunctionName, { stream: false }> {
  const { onFinalData, onError } = props
  const [isLoading, startTransition] = useTransition()

  const [state, dispatch] = useReducer(hookReducer<StreamDataType<FunctionName>, FinalDataType<FunctionName>>, {
    isSuccess: false,
    error: undefined,
    finalData: undefined,
    isStreaming: false,
    streamData: undefined,
  })

  const mutate = useCallback(
    async (...input: Parameters<ServerAction>) => {
      dispatch({ type: 'START_REQUEST' })
      try {
        let response: Awaited<ReturnType<ServerAction>>
        startTransition(async () => {
          // Transform any BamlImage or BamlAudio inputs to their JSON representation
          const transformedInput = input.map(arg => {
            // Check if the argument is an instance of BamlImage or BamlAudio
            // We check the constructor name since the actual classes might be proxied in browser environments
            if (arg && typeof arg === 'object' &&
                (arg.constructor.name === 'BamlImage' || arg.constructor.name === 'BamlAudio')) {
              return arg.toJSON();
            }
            return arg;
          });

          response = await action(...transformedInput)

          if (isStreamingProps(props) && response instanceof ReadableStream) {
            const reader = response.getReader()
            const decoder = new TextDecoder()
            try {
              while (true) {
                const { value, done } = await reader.read()
                if (done) break
                if (value) {
                  const chunk = decoder.decode(value, { stream: true }).trim()
                  try {
                    const parsed: BamlStreamResponse<
                      StreamDataType<FunctionName>,
                      FinalDataType<FunctionName>
                    > = JSON.parse(chunk)
                    if (parsed.error) {
                       if (parsed.error instanceof Error) {
                        throw parsed.error
                      }

                      const parsedError = JSON.parse(parsed.error)
                      const finalError = toBamlError(parsedError)
                      throw finalError
                    }
                    if (parsed.partial !== undefined) {
                      dispatch({ type: 'SET_PARTIAL', payload: parsed.partial })
                      if (isStreamingProps(props)) {
                        props.onStreamData?.(parsed.partial)
                      }
                      props.onData?.(parsed.partial)
                    }
                    if (parsed.final !== undefined) {
                      dispatch({ type: 'SET_FINAL', payload: parsed.final })
                      onFinalData?.(parsed.final)
                      props.onData?.(parsed.final)
                      return
                    }
                  } catch (err: unknown) {
                    dispatch({
                      type: 'SET_ERROR',
                      payload: err as BamlErrors,
                    })
                    onError?.(err as BamlErrors)
                    break
                  }
                }
              }
            } finally {
              reader.releaseLock()
            }
            return
          }
          // Non‑streaming case
          dispatch({ type: 'SET_FINAL', payload: response })
          onFinalData?.(response)
        })
        return response
      } catch (error_: unknown) {
        dispatch({ type: 'SET_ERROR', payload: error_ as BamlErrors })
        onError?.(error_ as BamlErrors)
        throw error_
      }
    },
    [action, onFinalData, onError, props],
  )

  const status = useMemo<HookStatus<{ stream: typeof props.stream }>>(() => {
    if (state.error) return 'error'
    if (state.isSuccess) return 'success'
    if (state.isStreaming) return 'streaming'
    if (isLoading) return 'pending'
    return 'idle'
  }, [isLoading, state.error, state.isSuccess, state.isStreaming])

  let data:
		| FinalDataType<FunctionName>
		| StreamDataType<FunctionName>
		| undefined = state.finalData;
  if (state.isStreaming) data = state.streamData

  const result = {
    data,
    finalData: state.finalData,
    error: state.error,
    isError: status === 'error',
    isSuccess: status === 'success',
    isStreaming: status === 'streaming',
    isPending: status === 'pending',
    isLoading: status === 'pending' || status === 'streaming',
    mutate,
    status,
    reset: () => dispatch({ type: 'RESET' }),
  } satisfies HookOutput<FunctionName, { stream: typeof props.stream }>

  return {
    ...result,
    streamData: isStreamingProps(props) ? state.streamData : undefined,
  } satisfies HookOutput<FunctionName, { stream: typeof props.stream }>
}
/**
 * A specialized hook for the AnalyzeNDARisks BAML function that supports both streaming and non‑streaming responses.
 *
 * **Input Types:**
 *
 * - nda: NDA
 *
 *
 * **Return Type:**
 * - **Non‑streaming:** RiskAnalysis
 * - **Streaming Partial:** partial_types.RiskAnalysis
 * - **Streaming Final:** RiskAnalysis
 *
 * **Usage Patterns:**
 * 1. **Non‑streaming (Default)**
 *    - Best for quick responses and simple UI updates.
 * 2. **Streaming**
 *    - Ideal for long‑running operations or real‑time feedback.
 *
 * **Edge Cases:**
 * - Ensure robust error handling via `onError`.
 * - Handle cases where partial data may be incomplete or missing.
 *
 * @example
 * ```tsx
 * // Basic non‑streaming usage:
 * const { data, error, isLoading, mutate } = useAnalyzeNDARisks({ stream: false});
 *
 * // Streaming usage:
 * const { data, streamData, isLoading, error, mutate } = useAnalyzeNDARisks({
 *   stream: true | undefined,
 *   onStreamData: (partial) => console.log('Partial update:', partial),
 *   onFinalData: (final) => console.log('Final result:', final),
 *   onError: (err) => console.error('Error:', err),
 * });
 * ```
 */
export function useAnalyzeNDARisks(props: HookInput<'AnalyzeNDARisks', { stream: false }>): HookOutput<'AnalyzeNDARisks', { stream: false }>
export function useAnalyzeNDARisks(props?: HookInput<'AnalyzeNDARisks', { stream?: true }>): HookOutput<'AnalyzeNDARisks', { stream: true }>
export function useAnalyzeNDARisks(
  props: HookInput<'AnalyzeNDARisks', { stream?: boolean }> = {},
): HookOutput<'AnalyzeNDARisks', { stream: true }> | HookOutput<'AnalyzeNDARisks', { stream: false }> {
  let action = Actions.AnalyzeNDARisks;
  if (isStreamingProps(props)) {
    action = StreamingActions.AnalyzeNDARisks;
  }
  return useBamlAction(action, props)
}
/**
 * A specialized hook for the ExecuteBAML BAML function that supports both streaming and non‑streaming responses.
 *
 * **Input Types:**
 *
 * - content: string | Image | Audio | Image[]
 *
 *
 * **Return Type:**
 * - **Non‑streaming:** Response
 * - **Streaming Partial:** partial_types.Response
 * - **Streaming Final:** Response
 *
 * **Usage Patterns:**
 * 1. **Non‑streaming (Default)**
 *    - Best for quick responses and simple UI updates.
 * 2. **Streaming**
 *    - Ideal for long‑running operations or real‑time feedback.
 *
 * **Edge Cases:**
 * - Ensure robust error handling via `onError`.
 * - Handle cases where partial data may be incomplete or missing.
 *
 * @example
 * ```tsx
 * // Basic non‑streaming usage:
 * const { data, error, isLoading, mutate } = useExecuteBAML({ stream: false});
 *
 * // Streaming usage:
 * const { data, streamData, isLoading, error, mutate } = useExecuteBAML({
 *   stream: true | undefined,
 *   onStreamData: (partial) => console.log('Partial update:', partial),
 *   onFinalData: (final) => console.log('Final result:', final),
 *   onError: (err) => console.error('Error:', err),
 * });
 * ```
 */
export function useExecuteBAML(props: HookInput<'ExecuteBAML', { stream: false }>): HookOutput<'ExecuteBAML', { stream: false }>
export function useExecuteBAML(props?: HookInput<'ExecuteBAML', { stream?: true }>): HookOutput<'ExecuteBAML', { stream: true }>
export function useExecuteBAML(
  props: HookInput<'ExecuteBAML', { stream?: boolean }> = {},
): HookOutput<'ExecuteBAML', { stream: true }> | HookOutput<'ExecuteBAML', { stream: false }> {
  let action = Actions.ExecuteBAML;
  if (isStreamingProps(props)) {
    action = StreamingActions.ExecuteBAML;
  }
  return useBamlAction(action, props)
}
/**
 * A specialized hook for the ExtractNDA BAML function that supports both streaming and non‑streaming responses.
 *
 * **Input Types:**
 *
 * - document: string | Image | Image[]
 *
 *
 * **Return Type:**
 * - **Non‑streaming:** NDA
 * - **Streaming Partial:** partial_types.NDA
 * - **Streaming Final:** NDA
 *
 * **Usage Patterns:**
 * 1. **Non‑streaming (Default)**
 *    - Best for quick responses and simple UI updates.
 * 2. **Streaming**
 *    - Ideal for long‑running operations or real‑time feedback.
 *
 * **Edge Cases:**
 * - Ensure robust error handling via `onError`.
 * - Handle cases where partial data may be incomplete or missing.
 *
 * @example
 * ```tsx
 * // Basic non‑streaming usage:
 * const { data, error, isLoading, mutate } = useExtractNDA({ stream: false});
 *
 * // Streaming usage:
 * const { data, streamData, isLoading, error, mutate } = useExtractNDA({
 *   stream: true | undefined,
 *   onStreamData: (partial) => console.log('Partial update:', partial),
 *   onFinalData: (final) => console.log('Final result:', final),
 *   onError: (err) => console.error('Error:', err),
 * });
 * ```
 */
export function useExtractNDA(props: HookInput<'ExtractNDA', { stream: false }>): HookOutput<'ExtractNDA', { stream: false }>
export function useExtractNDA(props?: HookInput<'ExtractNDA', { stream?: true }>): HookOutput<'ExtractNDA', { stream: true }>
export function useExtractNDA(
  props: HookInput<'ExtractNDA', { stream?: boolean }> = {},
): HookOutput<'ExtractNDA', { stream: true }> | HookOutput<'ExtractNDA', { stream: false }> {
  let action = Actions.ExtractNDA;
  if (isStreamingProps(props)) {
    action = StreamingActions.ExtractNDA;
  }
  return useBamlAction(action, props)
}
/**
 * A specialized hook for the GenerateBAML BAML function that supports both streaming and non‑streaming responses.
 *
 * **Input Types:**
 *
 * - content: string | Image | Audio | Image[]
 *
 *
 * **Return Type:**
 * - **Non‑streaming:** Schema
 * - **Streaming Partial:** partial_types.Schema
 * - **Streaming Final:** Schema
 *
 * **Usage Patterns:**
 * 1. **Non‑streaming (Default)**
 *    - Best for quick responses and simple UI updates.
 * 2. **Streaming**
 *    - Ideal for long‑running operations or real‑time feedback.
 *
 * **Edge Cases:**
 * - Ensure robust error handling via `onError`.
 * - Handle cases where partial data may be incomplete or missing.
 *
 * @example
 * ```tsx
 * // Basic non‑streaming usage:
 * const { data, error, isLoading, mutate } = useGenerateBAML({ stream: false});
 *
 * // Streaming usage:
 * const { data, streamData, isLoading, error, mutate } = useGenerateBAML({
 *   stream: true | undefined,
 *   onStreamData: (partial) => console.log('Partial update:', partial),
 *   onFinalData: (final) => console.log('Final result:', final),
 *   onError: (err) => console.error('Error:', err),
 * });
 * ```
 */
export function useGenerateBAML(props: HookInput<'GenerateBAML', { stream: false }>): HookOutput<'GenerateBAML', { stream: false }>
export function useGenerateBAML(props?: HookInput<'GenerateBAML', { stream?: true }>): HookOutput<'GenerateBAML', { stream: true }>
export function useGenerateBAML(
  props: HookInput<'GenerateBAML', { stream?: boolean }> = {},
): HookOutput<'GenerateBAML', { stream: true }> | HookOutput<'GenerateBAML', { stream: false }> {
  let action = Actions.GenerateBAML;
  if (isStreamingProps(props)) {
    action = StreamingActions.GenerateBAML;
  }
  return useBamlAction(action, props)
}
/**
 * A specialized hook for the TrackDeadlines BAML function that supports both streaming and non‑streaming responses.
 *
 * **Input Types:**
 *
 * - nda: NDA
 *
 *
 * **Return Type:**
 * - **Non‑streaming:** DeadlineReport
 * - **Streaming Partial:** partial_types.DeadlineReport
 * - **Streaming Final:** DeadlineReport
 *
 * **Usage Patterns:**
 * 1. **Non‑streaming (Default)**
 *    - Best for quick responses and simple UI updates.
 * 2. **Streaming**
 *    - Ideal for long‑running operations or real‑time feedback.
 *
 * **Edge Cases:**
 * - Ensure robust error handling via `onError`.
 * - Handle cases where partial data may be incomplete or missing.
 *
 * @example
 * ```tsx
 * // Basic non‑streaming usage:
 * const { data, error, isLoading, mutate } = useTrackDeadlines({ stream: false});
 *
 * // Streaming usage:
 * const { data, streamData, isLoading, error, mutate } = useTrackDeadlines({
 *   stream: true | undefined,
 *   onStreamData: (partial) => console.log('Partial update:', partial),
 *   onFinalData: (final) => console.log('Final result:', final),
 *   onError: (err) => console.error('Error:', err),
 * });
 * ```
 */
export function useTrackDeadlines(props: HookInput<'TrackDeadlines', { stream: false }>): HookOutput<'TrackDeadlines', { stream: false }>
export function useTrackDeadlines(props?: HookInput<'TrackDeadlines', { stream?: true }>): HookOutput<'TrackDeadlines', { stream: true }>
export function useTrackDeadlines(
  props: HookInput<'TrackDeadlines', { stream?: boolean }> = {},
): HookOutput<'TrackDeadlines', { stream: true }> | HookOutput<'TrackDeadlines', { stream: false }> {
  let action = Actions.TrackDeadlines;
  if (isStreamingProps(props)) {
    action = StreamingActions.TrackDeadlines;
  }
  return useBamlAction(action, props)
}