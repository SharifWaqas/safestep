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
 * The large, prominent risk-level component shown at the top of a result.
 * Communicates with an icon, a word, a plain-language sentence, and a
 * stepped severity meter (not color alone).
 */
export function RiskLevelCard({ level, className }: RiskLevelCardProps) {
  const meta = getRiskMeta(level)
  const t = tone[meta.token]
  const Icon = RISK_LEVEL_ICON[meta.level]
  const activeSteps = meta.weight + 1

  return (
    <section
      aria-labelledby="risk-level-heading"
      className={cn('rounded-2xl border p-6 sm:p-8', t.wrap, className)}
    >
      <p className="text-sm font-semibold uppercase tracking-wide text-muted-foreground">
        Risk assessment
      </p>
      <div className="mt-4 flex items-center gap-4 sm:gap-5">
        <span
          className={cn(
            'flex size-16 shrink-0 items-center justify-center rounded-2xl sm:size-20',
            t.iconWrap,
          )}
          aria-hidden="true"
        >
          <Icon className="size-9 sm:size-11" />
        </span>
        <div className="min-w-0">
          <h2
            id="risk-level-heading"
            className="text-3xl font-extrabold tracking-tight sm:text-4xl"
          >
            {meta.label}
          </h2>
          <p className="mt-1 text-pretty text-lg text-foreground/80">
            {meta.description}
          </p>
        </div>
      </div>

      {/* Stepped severity meter — 5 segments, filled by weight. */}
      <div className="mt-6">
        <div className="flex items-center gap-1.5" aria-hidden="true">
          {STEP_ORDER.map((_, i) => (
            <span
              key={i}
              className={cn(
                'h-2.5 flex-1 rounded-full',
                i < activeSteps ? t.bar : 'bg-foreground/10',
              )}
            />
          ))}
        </div>
        <p className="sr-only">
          Severity {activeSteps} out of 5.
        </p>
        <div className="mt-2 flex justify-between text-xs font-medium text-muted-foreground">
          <span>Safe</span>
          <span>Very high risk</span>
        </div>
      </div>
    </section>
  )
}
