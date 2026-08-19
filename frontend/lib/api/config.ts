/**
 * Integration configuration.
 *
 * When NEXT_PUBLIC_API_URL is set, the app talks to the real FastAPI backend.
 * When it is NOT set (e.g. an early preview), the app falls back to an isolated
 * mock layer so the interface can be explored. Set NEXT_PUBLIC_API_URL to point
 * at the backend (dev: http://127.0.0.1:8000, prod: https://api.example.com)
 * and the mocks are disabled automatically — no other code changes required.
 *
 * To force one mode, set NEXT_PUBLIC_USE_MOCKS to "true" or "false".
 */

const explicitMockFlag = process.env.NEXT_PUBLIC_USE_MOCKS

export const USE_MOCKS: boolean =
  explicitMockFlag === 'true'
    ? true
    : explicitMockFlag === 'false'
      ? false
      : !process.env.NEXT_PUBLIC_API_URL

/** Small helper so mock calls feel like real network latency. */
export function mockDelay(ms = 600): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms))
}
