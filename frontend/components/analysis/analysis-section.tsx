import type { LucideIcon } from 'lucide-react'
import { cn } from '@/lib/utils'

interface AnalysisSectionProps {
  icon: LucideIcon
  heading: string
  children: React.ReactNode
  /** Visually elevate the section (used for guidance). */
  emphasized?: boolean
  className?: string
}

/**
 * A titled block of guidance content with a clear icon + heading and
 * large, readable body text.
 */
export function AnalysisSection({
  icon: Icon,
  heading,
  children,
  emphasized = false,
  className,
}: AnalysisSectionProps) {
  return (
    <section
      className={cn(
        'rounded-2xl border p-6 sm:p-7',
        emphasized
          ? 'border-primary/25 bg-primary/5'
          : 'border-border bg-card',
        className,
      )}
    >
      <div className="flex items-center gap-3">
        <span
          className={cn(
            'flex size-10 shrink-0 items-center justify-center rounded-lg',
            emphasized
              ? 'bg-primary text-primary-foreground'
              : 'bg-muted text-foreground',
          )}
          aria-hidden="true"
        >
          <Icon className="size-5" />
        </span>
        <h3 className="text-xl font-bold tracking-tight sm:text-2xl">
          {heading}
        </h3>
      </div>
      <div className="mt-4 text-pretty text-lg leading-relaxed text-foreground/85">
        {children}
      </div>
    </section>
  )
}
