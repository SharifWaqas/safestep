import Link from 'next/link'
import { Logo } from '@/components/brand/logo'

export function PublicHeader() {
  return (
    <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80">
      <div className="mx-auto flex h-18 w-full max-w-6xl items-center justify-between gap-4 px-4 py-3 sm:px-6">
        <Logo />

        <nav
          className="flex items-center gap-2 sm:gap-3"
          aria-label="Main navigation"
        >
          <Link
            href="/login"
            className="inline-flex h-11 items-center justify-center rounded-md px-4 text-base font-medium transition-colors hover:bg-accent hover:text-accent-foreground"
          >
            Log in
          </Link>

          <Link
            href="/register"
            className="inline-flex h-11 items-center justify-center rounded-md bg-primary px-4 text-base font-medium text-primary-foreground transition-colors hover:bg-primary/90 sm:px-5"
          >
            Create account
          </Link>
        </nav>
      </div>
    </header>
  )
}