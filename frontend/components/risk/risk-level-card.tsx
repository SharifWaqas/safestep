import { cn } from '@/lib/utils'
import type { RiskLevel } from '@/lib/api/types'
import { getRiskMeta } from '@/lib/risk'
import { RISK_LEVEL_ICON } from '@/lib/risk-visuals'

interface RiskLevelCardProps {
  level: RiskLevel
  className?: string
}

const tone: Record<
  string,
  { wrap: string; iconWrap: string; bar: string }
> = {
  safe: {
    wrap: 'bg-safe-subtle border-safe/30',
    iconWrap: 'bg-safe text-safe-foreground',
    bar: 'bg-safe',
  },
  low: {
    wrap: 'bg-low-subtle border-low/30',
    iconWrap: 'bg-low text-low-foreground',
    bar: 'bg-low',
  },
  medium: {
    wrap: 'bg-medium-subtle border-medium/45',
    iconWrap: 'bg-medium text-medium-foreground',
    bar: 'bg-medium',
  },
  high: {
    wrap: 'bg-high-subtle border-high/40',
    iconWrap: 'bg-high text-high-foreground',
    bar: 'bg-high',
  },
  critical: {
    wrap: 'bg-critical-subtle border-critical/40',
    iconWrap: 'bg-critical text-critical-foreground',
    bar: 'bg-critical',
  },
}

const STEP_ORDER = ['safe', 'low', 'medium', 'high', 'critical'] as const

/**
 * Prominent risk summary shown at the top of an analysis result.
 *
 * The component communicates severity through text, iconography, and a
 * stepped meter rather than relying on color alone.
 */
export function RiskLevelCard({
  level,
  className,
}: RiskLevelCardProps) {
  const meta = getRiskMeta(level)
  const t = tone[meta.token]
  const Icon = RISK_LEVEL_ICON[meta.level]
  const activeSteps = meta.weight + 1

  return (
    <section
      aria-labelledby="risk-level-heading"
      className={cn(
        'rounded-3xl border p-6 sm:p-8',
        t.wrap,
        className,
      )}
    >
      <p className="text-base font-bold tracking-tight text-foreground sm:text-lg">
        How concerned should I be?
      </p>

      <div className="mt-5 flex flex-col gap-5 sm:flex-row sm:items-center sm:gap-6">
        <span
          className={cn(
            'flex size-20 shrink-0 items-center justify-center rounded-2xl sm:size-24',
            t.iconWrap,
          )}
          aria-hidden="true"
        >
          <Icon className="size-10 sm:size-12" />
        </span>

        <div className="min-w-0">
          <h2
            id="risk-level-heading"
            className="text-4xl font-extrabold tracking-tight sm:text-5xl"
          >
            {meta.label}
          </h2>

          <p className="mt-2 max-w-2xl text-lg leading-8 text-foreground/85 sm:text-xl">
            {meta.description}
          </p>
        </div>
      </div>

      <div className="mt-7">
        <div
          className="flex items-center gap-2"
          aria-hidden="true"
        >
          {STEP_ORDER.map((_, i) => (
            <span
              key={i}
              className={cn(
                'h-3 flex-1 rounded-full',
                i < activeSteps ? t.bar : 'bg-foreground/10',
              )}
            />
          ))}
        </div>

        <p className="sr-only">
          Risk level {meta.label}. Severity {activeSteps} out of 5.
        </p>

        <div className="mt-2 flex justify-between text-sm font-semibold text-muted-foreground">
          <span>Safer</span>
          <span>More concerning</span>
        </div>
      </div>
    </section>
  )
}