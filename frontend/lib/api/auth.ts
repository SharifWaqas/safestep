import { apiClient, jsonHeaders, tokenStore } from './client'
import { USE_MOCKS } from './config'
import { mockApi } from './mock'
import type {
  AuthTokens,
  LoginPayload,
  RegisterPayload,
} from './types'

const ENDPOINTS = {
  login: '/auth/login',
  register: '/auth/register',
  refresh: '/auth/refresh',
  logout: '/auth/logout',
} as const

export const authApi = {
  async login(payload: LoginPayload): Promise<AuthTokens> {
    const tokens: AuthTokens = USE_MOCKS
      ? await mockApi.login(payload)
      : await apiClient.post<AuthTokens>(
          ENDPOINTS.login,
          JSON.stringify(payload),
          {
            headers: jsonHeaders(),
            skipAuth: true,
          },
        )

    tokenStore.set(tokens.access_token)

    return tokens
  },

  async register(payload: RegisterPayload): Promise<AuthTokens> {
    const tokens: AuthTokens = USE_MOCKS
      ? await mockApi.register(payload)
      : await apiClient.post<AuthTokens>(
          ENDPOINTS.register,
          JSON.stringify(payload),
          {
            headers: jsonHeaders(),
            skipAuth: true,
          },
        )

    tokenStore.set(tokens.access_token)

    return tokens
  },

  async refresh(refreshToken: string): Promise<AuthTokens> {
    const tokens = await apiClient.post<AuthTokens>(
      ENDPOINTS.refresh,
      JSON.stringify({
        refresh_token: refreshToken,
      }),
      {
        headers: jsonHeaders(),
        skipAuth: true,
      },
    )

    tokenStore.set(tokens.access_token)

    return tokens
  },

  async logout(refreshToken: string): Promise<void> {
    await apiClient.post(
      ENDPOINTS.logout,
      JSON.stringify({
        refresh_token: refreshToken,
      }),
      {
        headers: jsonHeaders(),
        skipAuth: true,
      },
    )

    tokenStore.clear()
  },

  hasSession(): boolean {
    return tokenStore.get() !== null
  },
}