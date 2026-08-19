'use client'

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react'
import { useRouter } from 'next/navigation'
import { authApi } from '@/lib/api/auth'
import { setUnauthorizedHandler, tokenStore } from '@/lib/api/client'
import type {
  LoginPayload,
  RegisterPayload,
  User,
} from '@/lib/api/types'

interface AuthContextValue {
  user: User | null
  isLoading: boolean
  isAuthenticated: boolean
  login: (payload: LoginPayload) => Promise<void>
  register: (payload: RegisterPayload) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()

  const [hasToken, setHasToken] = useState(false)
  const [tokenChecked, setTokenChecked] = useState(false)

  useEffect(() => {
    const accessToken = tokenStore.getAccessToken()

    setHasToken(Boolean(accessToken))
    setTokenChecked(true)
  }, [])

  const clearSession = useCallback(() => {
    tokenStore.clear()
    setHasToken(false)
  }, [])

  useEffect(() => {
    setUnauthorizedHandler(() => {
      clearSession()
      router.push('/login?expired=1')
    })

    return () => {
      setUnauthorizedHandler(null)
    }
  }, [clearSession, router])

  const login = useCallback(
    async (payload: LoginPayload) => {
      await authApi.login(payload)
      setHasToken(true)
    },
    [],
  )

  const register = useCallback(
    async (payload: RegisterPayload) => {
      await authApi.register(payload)
      setHasToken(true)
    },
    [],
  )

  const logout = useCallback(() => {
    const refreshToken = tokenStore.getRefreshToken()

    if (refreshToken) {
      void authApi.logout(refreshToken).catch(() => {
        // The local session is still cleared below.
      })
    } else {
      tokenStore.clear()
    }

    setHasToken(false)
    router.push('/login')
  }, [router])

  const value = useMemo<AuthContextValue>(
    () => ({
      user: null,

      isLoading: !tokenChecked,

      isAuthenticated: tokenChecked && hasToken,

      login,
      register,
      logout,
    }),
    [
      tokenChecked,
      hasToken,
      login,
      register,
      logout,
    ],
  )

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)

  if (!ctx) {
    throw new Error(
      'useAuth must be used within AuthProvider',
    )
  }

  return ctx
}