import Link from 'next/link'
import { ArrowRight, Clock } from 'lucide-react'

import { RiskLevelBadge } from '@/components/risk/risk-level-badge'
import type { Analysis } from '@/lib/api/types'
import { getRiskMeta } from '@/lib/risk'
import { RISK_LEVEL_ICON } from '@/lib/risk-visuals'
import { formatRelative } from '@/lib/format'
import { cn } from '@/lib/utils'

interface AnalysisHistoryCardProps {
  analysis: Analysis
}

const statusLabel: Record<string, string> = {
  completed: 'Completed',
  processing: 'In progress',
  pending: 'Waiting',
  failed: 'Could not finish',
}

export function AnalysisHistoryCard({
  analysis,
}: AnalysisHistoryCardProps) {
  const ai = analysis.ai_result
  const meta = getRiskMeta(ai?.risk_level)
  const Icon = RISK_LEVEL_ICON[meta.level]

  const summary =
    ai?.summary ?? 'This analysis is still being prepared.'

  return (
    <li className="rounded-2xl border bg-card p-5 transition-colors hover:border-primary/40 sm:p-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
        <span
          className={cn(
            'flex size-12 shrink-0 items-center justify-center rounded-xl',
            meta.token === 'safe' && 'bg-safe-subtle text-safe',
            meta.token === 'low' && 'bg-low-subtle text-low',
            meta.token === 'medium' &&
              'bg-medium-subtle text-medium-foreground',
            meta.token === 'high' && 'bg-high-subtle text-high',
            meta.token === 'critical' &&
              'bg-critical-subtle text-critical',
          )}
          aria-hidden="true"
        >
          <Icon className="size-6" />
        </span>

        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
            {ai && (
              <RiskLevelBadge
                level={ai.risk_level}
                size="sm"
              />
            )}

            <span className="inline-flex items-center gap-1.5 text-sm text-muted-foreground">
              <Clock
                className="size-4"
                aria-hidden="true"
              />
              {formatRelative(analysis.started_at)}
            </span>

            <span className="text-sm text-muted-foreground">
              · {statusLabel[analysis.status] ?? analysis.status}
            </span>
          </div>

          <p className="mt-2 line-clamp-2 text-pretty text-lg leading-snug">
            {summary}
          </p>
        </div>

        <Link
          href={`/analysis/${analysis.analysis_id}`}
          className="inline-flex h-10 shrink-0 items-center justify-center gap-1.5 rounded-lg border border-border bg-background px-4 text-sm font-medium whitespace-nowrap transition-all hover:bg-muted hover:text-foreground focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-ring/50"
        >
          View analysis
          <ArrowRight
            className="size-4"
            aria-hidden="true"
          />
        </Link>
      </div>
    </li>
  )
}