'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

import { useAuth } from '@/components/auth/auth-provider'
import { AuthenticatedHeader } from '@/components/common/authenticated-header'

export default function AuthenticatedLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const { isAuthenticated, isLoading } = useAuth()

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.replace('/login')
    }
  }, [isAuthenticated, isLoading, router])

  if (isLoading || !isAuthenticated) {
    return (
      <main className="flex min-h-dvh items-center justify-center px-4">
        <p className="text-muted-foreground">
          Loading SafeStep...
        </p>
      </main>
    )
  }

  return (
    <div className="flex min-h-dvh flex-col">
      <AuthenticatedHeader />

      <main className="flex-1">
        {children}
      </main>
    </div>
  )
}