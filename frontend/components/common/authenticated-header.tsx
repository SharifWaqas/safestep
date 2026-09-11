'use client'

import Link from 'next/link'
import { History, LogOut, Settings } from 'lucide-react'

import { useAuth } from '@/components/auth/auth-provider'
import { Logo } from '@/components/brand/logo'

export function AuthenticatedHeader() {
  const { logout } = useAuth()

  return (
    <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80">
      <div className="mx-auto flex h-18 w-full max-w-6xl items-center justify-between gap-4 px-4 py-3 sm:px-6">
        <Logo />

        <nav
          className="flex items-center gap-2 sm:gap-3"
          aria-label="Application navigation"
        >
          <Link
            href="/analyze"
            className="inline-flex h-9 items-center justify-center rounded-lg px-3 text-sm font-medium transition-all hover:bg-muted hover:text-foreground focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-ring/50 sm:h-10"
          >
            Analyze
          </Link>

          <Link
            href="/history"
            className="inline-flex h-9 items-center justify-center gap-1.5 rounded-lg px-3 text-sm font-medium transition-all hover:bg-muted hover:text-foreground focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-ring/50 sm:h-10"
          >
            <History
              className="size-4"
              aria-hidden="true"
            />
            History
          </Link>

          <Link
            href="/settings"
            className="inline-flex h-9 items-center justify-center gap-1.5 rounded-lg px-3 text-sm font-medium transition-all hover:bg-muted hover:text-foreground focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-ring/50 sm:h-10"
          >
            <Settings
              className="size-4"
              aria-hidden="true"
            />
            Settings
          </Link>

          <button
            type="button"
            onClick={logout}
            className="inline-flex h-9 items-center justify-center gap-1.5 rounded-lg border border-border bg-background px-3 text-sm font-medium transition-all hover:bg-muted hover:text-foreground focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-ring/50 sm:h-10"
          >
            <LogOut
              className="size-4"
              aria-hidden="true"
            />
            Log out
          </button>
        </nav>
      </div>
    </header>
  )
}