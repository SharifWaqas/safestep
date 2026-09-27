import { cn } from '@/lib/utils'
import type { RiskScore } from '@/lib/api/types'
import { riskFactorLabel, scoreBand } from '@/lib/risk'
import { riskFactorIcon } from '@/lib/risk-visuals'

interface RiskFactorCardProps {
  factor: RiskScore
}

const bandTone: Record<
  string,
  { text: string; bar: string; badge: string }
> = {
  safe: {
    text: 'text-safe',
    bar: 'bg-safe',
    badge: 'bg-safe-subtle text-safe',
  },
  medium: {
    text: 'text-medium-foreground',
    bar: 'bg-medium',
    badge: 'bg-medium-subtle text-medium-foreground',
  },
  high: {
    text: 'text-high',
    bar: 'bg-high',
    badge: 'bg-high-subtle text-high',
  },
  critical: {
    text: 'text-critical',
    bar: 'bg-critical',
    badge: 'bg-critical-subtle text-critical',
  },
}

/**
 * A single detected warning sign presented in plain language.
 *
 * The UI emphasizes the human-readable warning level and explanation.
 * The underlying score remains available to assistive technology through
 * the meter but is not presented as a technical percentage to the user.
 */
export function RiskFactorCard({ factor }: RiskFactorCardProps) {
  const label = riskFactorLabel(factor.risk_factor)
  const band = scoreBand(factor.score)
  const tone = bandTone[band.token]
  const Icon = riskFactorIcon(factor.risk_factor)

  return (
    <li className="flex gap-4 rounded-2xl border bg-card p-5 sm:p-6">
      <span
        className={cn(
          'flex size-12 shrink-0 items-center justify-center rounded-xl bg-muted',
          tone.text,
        )}
        aria-hidden="true"
      >
        <Icon className="size-6" />
      </span>

      <div className="min-w-0 flex-1">
        <div className="flex flex-col items-start gap-2 sm:flex-row sm:items-center sm:justify-between">
          <h4 className="text-xl font-bold leading-tight">
            {label}
          </h4>

          <span
            className={cn(
              'rounded-full px-3 py-1 text-sm font-bold',
              tone.badge,
            )}
          >
            {band.label}
          </span>
        </div>

        <p className="mt-3 text-lg leading-8 text-foreground/80">
          {factor.explanation}
        </p>

        <div className="mt-4">
          <div
            className="h-2.5 w-full overflow-hidden rounded-full bg-muted"
            role="meter"
            aria-valuenow={band.percent}
            aria-valuemin={0}
            aria-valuemax={100}
            aria-label={`${label} warning strength: ${band.label}`}
          >
            <div
              className={cn('h-full rounded-full', tone.bar)}
              style={{ width: `${Math.max(band.percent, 6)}%` }}
            />
          </div>
        </div>
      </div>
    </li>
  )
}