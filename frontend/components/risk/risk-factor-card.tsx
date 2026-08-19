import { cn } from '@/lib/utils'
import type { RiskScore } from '@/lib/api/types'
import { riskFactorLabel, scoreBand } from '@/lib/risk'
import { riskFactorIcon } from '@/lib/risk-visuals'

interface RiskFactorCardProps {
  factor: RiskScore
}

const bandTone: Record<string, { text: string; bar: string; wrap: string }> = {
  safe: { text: 'text-safe', bar: 'bg-safe', wrap: 'bg-safe' },
  medium: { text: 'text-medium-foreground', bar: 'bg-medium', wrap: 'bg-medium' },
  high: { text: 'text-high', bar: 'bg-high', wrap: 'bg-high' },
  critical: { text: 'text-critical', bar: 'bg-critical', wrap: 'bg-critical' },
}

/**
 * A single detected warning sign: friendly name, plain-language strength,
 * a short explanation, and an accessible strength meter. The raw decimal is
 * kept available for screen readers but is never the primary message.
 */
export function RiskFactorCard({ factor }: RiskFactorCardProps) {
  const label = riskFactorLabel(factor.risk_factor)
  const band = scoreBand(factor.score)
  const tone = bandTone[band.token]
  const Icon = riskFactorIcon(factor.risk_factor)

  return (
    <li className="flex gap-4 rounded-xl border bg-card p-4 sm:p-5">
      <span
        className={cn(
          'flex size-11 shrink-0 items-center justify-center rounded-lg bg-muted',
          tone.text,
        )}
        aria-hidden="true"
      >
        <Icon className="size-5" />
      </span>
      <div className="min-w-0 flex-1">
        <div className="flex flex-wrap items-center justify-between gap-x-3 gap-y-1">
          <h4 className="text-lg font-semibold leading-tight">{label}</h4>
          <span className={cn('text-sm font-semibold', tone.text)}>
            {band.label}
          </span>
        </div>
        <p className="mt-1 text-pretty text-foreground/75">
          {factor.explanation}
        </p>
        <div className="mt-3">
          <div
            className="h-2 w-full overflow-hidden rounded-full bg-muted"
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
