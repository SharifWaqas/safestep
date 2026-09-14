import { apiClient, jsonHeaders, tokenStore } from './client'
import { USE_MOCKS } from './config'
import { mockApi } from './mock'
import type {
  AuthTokens,
  LoginPayload,
  LoginResponse,
  RegisterPayload,
  RegisterResponse,
  User,
  AuthResponse
} from './types'

const ENDPOINTS = {
  login: '/auth/login',
  register: '/auth/register',
  refresh: '/auth/refresh',
  logout: '/auth/logout',
} as const

function storeTokens(tokens: AuthTokens): void {
  tokenStore.setTokens(
    tokens.access_token,
    tokens.refresh_token,
  )
}

function mapUser(user: LoginResponse['user']): User {
  return {
    id: user.id,
    email: user.email,
    name: user.full_name,
  }
}

export const authApi = {
  async login(
    payload: LoginPayload,
  ): Promise<AuthResponse> {
    const response: LoginResponse = USE_MOCKS
      ? await mockApi.login(payload)
      : await apiClient.post<LoginResponse>(
          ENDPOINTS.login,
          JSON.stringify(payload),
          {
            headers: jsonHeaders(),
            skipAuth: true,
          },
        )

    storeTokens(response)

    return {
      ...response,
      user: mapUser(response.user),
    }
  },

  async register(
    payload: RegisterPayload,
  ): Promise<AuthResponse> {
    const response: RegisterResponse = USE_MOCKS
      ? await mockApi.register(payload)
      : await apiClient.post<RegisterResponse>(
          ENDPOINTS.register,
          JSON.stringify(payload),
          {
            headers: jsonHeaders(),
            skipAuth: true,
          },
        )

    storeTokens(response)

    return {
      ...response,
      user: mapUser(response.user),
    }
  },

  async refresh(
    refreshToken: string,
  ): Promise<AuthTokens> {
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

    storeTokens(tokens)

    return tokens
  },

  async logout(): Promise<void> {
    const refreshToken = tokenStore.getRefreshToken()

    try {
      if (refreshToken) {
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
      }
    } finally {
      tokenStore.clear()
    }
  },

  getAccessToken(): string | null {
    return tokenStore.getAccessToken()
  },

  hasSession(): boolean {
    return tokenStore.getAccessToken() !== null
  },
}