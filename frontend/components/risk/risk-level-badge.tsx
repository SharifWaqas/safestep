import { cn } from '@/lib/utils'
import type { RiskLevel } from '@/lib/api/types'
import { getRiskMeta } from '@/lib/risk'
import { RISK_LEVEL_ICON } from '@/lib/risk-visuals'

interface RiskLevelBadgeProps {
  level: RiskLevel
  size?: 'sm' | 'md'
  className?: string
}

const toneClasses: Record<string, string> = {
  safe: 'bg-safe-subtle text-safe border-safe/25',
  low: 'bg-low-subtle text-low border-low/25',
  medium: 'bg-medium-subtle text-medium-foreground border-medium/40',
  high: 'bg-high-subtle text-high border-high/30',
  critical: 'bg-critical-subtle text-critical border-critical/30',
}

/**
 * Compact, self-describing risk indicator (icon + word).
 * Never relies on color alone — the label and icon carry the meaning.
 */
export function RiskLevelBadge({
  level,
  size = 'md',
  className,
}: RiskLevelBadgeProps) {
  const meta = getRiskMeta(level)
  const Icon = RISK_LEVEL_ICON[meta.level]
  return (
    <span
      className={cn(
        'inline-flex items-center gap-2 rounded-full border font-semibold',
        toneClasses[meta.token],
        size === 'sm' ? 'px-3 py-1 text-sm' : 'px-4 py-1.5 text-base',
        className,
      )}
    >
      <Icon className={size === 'sm' ? 'size-4' : 'size-5'} aria-hidden="true" />
      <span>{meta.label}</span>
    </span>
  )
}
