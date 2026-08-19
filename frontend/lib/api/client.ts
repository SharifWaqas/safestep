/**
 * Central API client for the SafeStep FastAPI backend.
 *
 * All network access goes through here so components never call `fetch` directly.
 * The base URL is configured via NEXT_PUBLIC_API_URL so the app can switch
 * between development and production without code changes.
 */

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, '') ??
  'http://127.0.0.1:8000'

const ACCESS_TOKEN_KEY = 'safestep.access_token'
const REFRESH_TOKEN_KEY = 'safestep.refresh_token'

/** A user-safe error. `message` is always presentable to end users. */
export class ApiError extends Error {
  status: number

  code:
    | 'unauthorized'
    | 'forbidden'
    | 'not_found'
    | 'invalid'
    | 'server'
    | 'network'
    | 'timeout'
    | 'unknown'

  constructor(message: string, status: number, code: ApiError['code']) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.code = code
  }
}

/* ------------------------------------------------------------------ */
/* Token storage                                                       */
/* ------------------------------------------------------------------ */

export const tokenStore = {
  getAccessToken(): string | null {
    if (typeof window === 'undefined') return null

    return window.localStorage.getItem(ACCESS_TOKEN_KEY)
  },

  getRefreshToken(): string | null {
    if (typeof window === 'undefined') return null

    return window.localStorage.getItem(REFRESH_TOKEN_KEY)
  },

  setTokens(accessToken: string, refreshToken: string): void {
    if (typeof window === 'undefined') return

    window.localStorage.setItem(ACCESS_TOKEN_KEY, accessToken)
    window.localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken)
  },

  clear(): void {
    if (typeof window === 'undefined') return

    window.localStorage.removeItem(ACCESS_TOKEN_KEY)
    window.localStorage.removeItem(REFRESH_TOKEN_KEY)
  },
}

/** Called when the backend reports the session is no longer valid (401). */
let onUnauthorized: (() => void) | null = null

export function setUnauthorizedHandler(
  handler: (() => void) | null,
): void {
  onUnauthorized = handler
}

/* ------------------------------------------------------------------ */
/* Error normalization                                                 */
/* ------------------------------------------------------------------ */

function messageForStatus(
  status: number,
  backendDetail?: string,
): string {
  switch (status) {
    case 400:
      return (
        backendDetail ??
        'Something in that request was not quite right.'
      )

    case 401:
      return 'Your session has expired. Please log in again.'

    case 403:
      return 'You do not have permission to do that.'

    case 404:
      return "We couldn't find what you were looking for."

    case 413:
      return 'That file is too large. Please try a smaller image.'

    case 415:
      return 'That file type is not supported. Please upload an image.'

    case 422:
      return (
        backendDetail ??
        'Please check the information you entered.'
      )

    default:
      if (status >= 500) {
        return 'Something went wrong on our side. Please try again in a moment.'
      }

      return 'Something went wrong. Please try again.'
  }
}

function codeForStatus(status: number): ApiError['code'] {
  if (status === 401) return 'unauthorized'
  if (status === 403) return 'forbidden'
  if (status === 404) return 'not_found'

  if (
    status === 400 ||
    status === 422 ||
    status === 413 ||
    status === 415
  ) {
    return 'invalid'
  }

  if (status >= 500) return 'server'

  return 'unknown'
}

/**
 * Extract a human-readable detail from a FastAPI error body without ever
 * exposing tracebacks to users.
 *
 * FastAPI typically returns:
 *
 * {
 *   "detail": "..."
 * }
 *
 * or:
 *
 * {
 *   "detail": [
 *     {
 *       "loc": [...],
 *       "msg": "...",
 *       "type": "..."
 *     }
 *   ]
 * }
 */
async function extractDetail(
  response: Response,
): Promise<string | undefined> {
  try {
    const data = await response.clone().json()

    if (typeof data?.detail === 'string') {
      return data.detail
    }

    if (
      Array.isArray(data?.detail) &&
      data.detail[0]?.msg
    ) {
      return String(data.detail[0].msg)
    }

    if (typeof data?.message === 'string') {
      return data.message
    }
  } catch {
    // Response body was not JSON.
  }

  return undefined
}

/* ------------------------------------------------------------------ */
/* Core request                                                        */
/* ------------------------------------------------------------------ */

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'
  body?: BodyInit | null
  headers?: Record<string, string>

  /** Skip attaching the access token. */
  skipAuth?: boolean

  /** Request timeout in ms. Defaults to 30s. */
  timeout?: number

  signal?: AbortSignal
}

async function request<T>(
  path: string,
  options: RequestOptions = {},
): Promise<T> {
  const {
    method = 'GET',
    body,
    headers = {},
    skipAuth = false,
    timeout = 30_000,
    signal,
  } = options

  const controller = new AbortController()

  const timeoutId = setTimeout(
    () => controller.abort(),
    timeout,
  )

  if (signal) {
    signal.addEventListener(
      'abort',
      () => controller.abort(),
      { once: true },
    )
  }

  const finalHeaders: Record<string, string> = {
    ...headers,
  }

  if (!skipAuth) {
    const accessToken = tokenStore.getAccessToken()

    if (accessToken) {
      finalHeaders.Authorization = `Bearer ${accessToken}`
    }
  }

  let response: Response

  try {
    response = await fetch(
      `${API_BASE_URL}${path}`,
      {
        method,
        body,
        headers: finalHeaders,
        signal: controller.signal,
      },
    )
  } catch (err) {
    clearTimeout(timeoutId)

    if (
      err instanceof DOMException &&
      err.name === 'AbortError'
    ) {
      throw new ApiError(
        'This is taking longer than expected. Please try again.',
        0,
        'timeout',
      )
    }

    throw new ApiError(
      "We couldn't reach SafeStep. Please check your connection and try again.",
      0,
      'network',
    )
  }

  clearTimeout(timeoutId)

  if (!response.ok) {
    const detail = await extractDetail(response)

    if (response.status === 401) {
      onUnauthorized?.()
    }

    throw new ApiError(
      messageForStatus(response.status, detail),
      response.status,
      codeForStatus(response.status),
    )
  }

  if (response.status === 204) {
    return undefined as T
  }

  const contentType =
    response.headers.get('content-type') ?? ''

  if (!contentType.includes('application/json')) {
    return undefined as T
  }

  return (await response.json()) as T
}

/* ------------------------------------------------------------------ */
/* Public API client                                                   */
/* ------------------------------------------------------------------ */

export const apiClient = {
  get: <T>(
    path: string,
    options?: RequestOptions,
  ) =>
    request<T>(
      path,
      {
        ...options,
        method: 'GET',
      },
    ),

  post: <T>(
    path: string,
    body?: BodyInit | null,
    options?: RequestOptions,
  ) =>
    request<T>(
      path,
      {
        ...options,
        method: 'POST',
        body,
      },
    ),

  put: <T>(
    path: string,
    body?: BodyInit | null,
    options?: RequestOptions,
  ) =>
    request<T>(
      path,
      {
        ...options,
        method: 'PUT',
        body,
      },
    ),

  delete: <T>(
    path: string,
    options?: RequestOptions,
  ) =>
    request<T>(
      path,
      {
        ...options,
        method: 'DELETE',
      },
    ),
}

export function jsonHeaders(): Record<string, string> {
  return {
    'Content-Type': 'application/json',
  }
}