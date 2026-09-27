'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useParams } from 'next/navigation'

import { analysesApi } from '@/lib/api/analyses'
import type { Analysis } from '@/lib/api/types'
import { AnalysisResult } from '@/components/analysis/analysis-result'

export default function AnalysisPage() {
  const params = useParams()
  const analysisId = params.analysis_id as string

  const [analysis, setAnalysis] = useState<Analysis | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadAnalysis() {
      if (!analysisId) return

      try {
        setIsLoading(true)
        setError(null)

        const result = await analysesApi.get(analysisId)

        setAnalysis(result)
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : 'We could not load this analysis.',
        )
      } finally {
        setIsLoading(false)
      }
    }

    void loadAnalysis()
  }, [analysisId])

  if (isLoading) {
    return (
      <main className="mx-auto flex min-h-dvh w-full max-w-4xl items-center justify-center px-4 py-10">
        <div className="text-center" role="status" aria-live="polite">
          <div
            className="mx-auto mb-4 size-10 animate-spin rounded-full border-4 border-muted border-t-primary"
            aria-hidden="true"
          />

          <h1 className="text-2xl font-bold">
            Analyzing your message...
          </h1>

          <p className="mt-2 text-muted-foreground">
            SafeStep is looking for signs that could indicate a scam.
          </p>
        </div>
      </main>
    )
  }

  if (error || !analysis) {
    return (
      <main className="mx-auto flex min-h-dvh w-full max-w-2xl items-center justify-center px-4 py-10">
        <div
          role="alert"
          className="w-full rounded-2xl border bg-card p-8 text-center"
        >
          <h1 className="text-2xl font-bold">
            We couldn't load the analysis
          </h1>

          <p className="mt-3 text-muted-foreground">
            {error ?? 'This analysis could not be found.'}
          </p>

          <Link
            href="/analyze"
            className="mt-6 inline-flex rounded-lg bg-primary px-5 py-3 font-medium text-primary-foreground hover:opacity-90"
          >
            Analyze another message
          </Link>
        </div>
      </main>
    )
  }

  const result = analysis.ai_result

  return (
    <main className="mx-auto w-full max-w-4xl px-4 py-10 sm:px-6">
      <div className="mb-8">
        <Link
          href="/analyze"
          className="text-sm font-medium text-primary hover:underline"
        >
          ← Analyze another message
        </Link>

        <h1 className="mt-6 text-3xl font-bold tracking-tight">
          Your SafeStep analysis
        </h1>

        <p className="mt-2 text-muted-foreground">
          Here's what SafeStep found in your message.
        </p>
      </div>

      {result ? (
        <AnalysisResult analysis={analysis} />
      ) : (
        <section className="rounded-2xl border bg-card p-6">
          <h2 className="text-xl font-bold">
            Analysis unavailable
          </h2>

          <p className="mt-2 text-muted-foreground">
            SafeStep completed the request, but there was no AI result to
            display.
          </p>
        </section>
      )}
    </main>
  )
}