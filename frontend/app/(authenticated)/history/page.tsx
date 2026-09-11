'use client'

import { useCallback, useEffect, useState } from 'react'
import Link from 'next/link'
import { History, ShieldCheck } from 'lucide-react'

import { AnalysisHistoryCard } from '@/components/history/analysis-history-card'
import { CardListSkeleton } from '@/components/common/loading-state'
import { ErrorState } from '@/components/common/error-state'
import {
  Empty,
  EmptyContent,
  EmptyDescription,
  EmptyHeader,
  EmptyMedia,
  EmptyTitle,
} from '@/components/ui/empty'
import { analysesApi } from '@/lib/api/analyses'
import type { Analysis } from '@/lib/api/types'

export default function HistoryPage() {
  const [analyses, setAnalyses] = useState<Analysis[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const loadHistory = useCallback(async () => {
    try {
      setIsLoading(true)
      setError(null)

      const result = await analysesApi.list()

      setAnalyses(result)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'We could not load your analysis history.',
      )
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    void loadHistory()
  }, [loadHistory])

  return (
    <main className="mx-auto w-full max-w-4xl px-4 py-10 sm:px-6">
      <div className="mb-8">
        <div className="flex items-center gap-3">
          <span
            className="flex size-11 items-center justify-center rounded-xl bg-primary/10 text-primary"
            aria-hidden="true"
          >
            <History className="size-6" />
          </span>

          <div>
            <h1 className="text-3xl font-bold tracking-tight">
              Analysis history
            </h1>

            <p className="mt-1 text-muted-foreground">
              Review the messages you have analyzed with SafeStep.
            </p>
          </div>
        </div>
      </div>

      {isLoading && <CardListSkeleton />}

      {!isLoading && error && (
        <ErrorState
          title="We couldn't load your history"
          description={error}
          onRetry={loadHistory}
          secondaryHref="/analyze"
          secondaryLabel="Analyze a message"
        />
      )}

      {!isLoading && !error && analyses.length === 0 && (
        <Empty className="min-h-[360px] bg-card">
          <EmptyHeader>
            <EmptyMedia
              variant="icon"
              className="size-12 rounded-xl"
            >
              <ShieldCheck className="size-6" />
            </EmptyMedia>

            <EmptyTitle className="text-xl">
              No analyses yet
            </EmptyTitle>

            <EmptyDescription className="text-base">
              When you analyze a suspicious message, your results will
              appear here so you can review them later.
            </EmptyDescription>
          </EmptyHeader>

          <EmptyContent>
            <Link
              href="/analyze"
              className="inline-flex h-12 items-center justify-center rounded-lg bg-primary px-6 text-base font-medium text-primary-foreground transition-all hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-ring/50"
            >
              Analyze a message
            </Link>
          </EmptyContent>
        </Empty>
      )}

      {!isLoading && !error && analyses.length > 0 && (
        <ul className="flex flex-col gap-4">
          {analyses.map((analysis) => (
            <AnalysisHistoryCard
              key={analysis.analysis_id}
              analysis={analysis}
            />
          ))}
        </ul>
      )}
    </main>
  )
}