import Link from 'next/link'
import type { LucideIcon } from 'lucide-react'
import { TriangleAlert } from 'lucide-react'
import { Button } from '@/components/ui/button'

interface ErrorStateProps {
  icon?: LucideIcon
  title: string
  description: string
  /** Primary action — usually a retry callback. */
  onRetry?: () => void
  retryLabel?: string
  /** Optional secondary link (e.g. back to a safe page). */
  secondaryHref?: string
  secondaryLabel?: string
}

/**
 * A calm, human-readable error surface. Never shows tracebacks or codes —
 * only plain-language guidance and a clear next step.
 */
export function ErrorState({
  icon: Icon = TriangleAlert,
  title,
  description,
  onRetry,
  retryLabel = 'Try again',
  secondaryHref,
  secondaryLabel,
}: ErrorStateProps) {
  return (
    <div className="mx-auto flex max-w-lg flex-col items-center rounded-2xl border bg-card p-8 text-center sm:p-10">
      <span
        className="flex size-14 items-center justify-center rounded-2xl bg-high-subtle text-high"
        aria-hidden="true"
      >
        <Icon className="size-7" />
      </span>
      <h2 className="mt-5 text-2xl font-bold tracking-tight text-balance">
        {title}
      </h2>
      <p className="mt-2 text-pretty text-lg text-muted-foreground">
        {description}
      </p>
      <div className="mt-6 flex flex-wrap justify-center gap-3">
        {onRetry && (
          <Button
            size="lg"
            onClick={onRetry}
            className="h-12 px-6 text-base"
          >
            {retryLabel}
          </Button>
        )}
        {secondaryHref && secondaryLabel && (
          <Button
            variant="outline"
            size="lg"
            className="h-12 px-6 text-base"
            render={<Link href={secondaryHref}>{secondaryLabel}</Link>}
          />
        )}
      </div>
    </div>
  )
}
