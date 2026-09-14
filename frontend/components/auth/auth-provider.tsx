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
import type { LoginPayload, RegisterPayload, User } from '@/lib/api/types'

interface AuthContextValue {
  user: User | null
  hasToken: boolean
  tokenChecked: boolean
  login: (payload: LoginPayload) => Promise<void>
  register: (payload: RegisterPayload) => Promise<void>
  logout: () => Promise<void>
}

export const AuthContext = createContext<AuthContextValue | undefined>(undefined)

const USER_STORAGE_KEY = 'safestep.user'

export function useAuth() {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }

  return context
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const router = useRouter()

  const [user, setUser] = useState<User | null>(null)
  const [hasToken, setHasToken] = useState(false)
  const [tokenChecked, setTokenChecked] = useState(false)

  useEffect(() => {
    const token = authApi.getAccessToken()
    const storedUser = localStorage.getItem(USER_STORAGE_KEY)

    setHasToken(Boolean(token))

    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser) as User)
      } catch {
        localStorage.removeItem(USER_STORAGE_KEY)
      }
    }

    setTokenChecked(true)
  }, [])

  const clearSession = useCallback(() => {
    tokenStore.clear()
    localStorage.removeItem(USER_STORAGE_KEY)
    setUser(null)
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

  const login = useCallback(async (payload: LoginPayload) => {
    const response = await authApi.login(payload)

    setUser(response.user)
    localStorage.setItem(
      USER_STORAGE_KEY,
      JSON.stringify(response.user),
    )
    setHasToken(true)
  }, [])

  const register = useCallback(async (payload: RegisterPayload) => {
    const response = await authApi.register(payload)

    setUser(response.user)
    localStorage.setItem(
      USER_STORAGE_KEY,
      JSON.stringify(response.user),
    )
    setHasToken(true)
  }, [])

  const logout = useCallback(async () => {
    await authApi.logout()
    localStorage.removeItem(USER_STORAGE_KEY)
    setUser(null)
    setHasToken(false)
    router.push('/login')
  }, [router])

  const value = useMemo(
    () => ({
      user,
      hasToken,
      tokenChecked,
      login,
      register,
      logout,
    }),
    [user, hasToken, tokenChecked, login, register, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}