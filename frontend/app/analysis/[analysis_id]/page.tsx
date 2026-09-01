'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useParams } from 'next/navigation'

import { analysesApi } from '@/lib/api/analyses'
import type { Analysis } from '@/lib/api/types'

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
        <div className="text-center">
          <div className="mx-auto mb-4 size-10 animate-spin rounded-full border-4 border-muted border-t-primary" />

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
        <div className="w-full rounded-2xl border bg-card p-8 text-center">
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
        <div className="space-y-6">
          {/* Risk level */}
          <section className="rounded-2xl border bg-card p-6">
            <p className="text-sm font-medium uppercase tracking-wide text-muted-foreground">
              Risk level
            </p>

            <div className="mt-3 flex items-center gap-3">
              <span className="rounded-full bg-primary/10 px-4 py-2 text-lg font-bold text-primary">
                {result.risk_level.replace('_', ' ')}
              </span>
            </div>

            <h2 className="mt-6 text-2xl font-bold">
              {result.summary}
            </h2>

            <p className="mt-3 leading-7 text-muted-foreground">
              {result.explanation}
            </p>
          </section>

          {/* Guidance */}
          <section className="rounded-2xl border bg-card p-6">
            <h2 className="text-xl font-bold">
              What you should do
            </h2>

            <p className="mt-3 leading-7 text-muted-foreground">
              {result.guidance}
            </p>
          </section>

          {/* Reassurance */}
          <section className="rounded-2xl border bg-card p-6">
            <h2 className="text-xl font-bold">
              A little reassurance
            </h2>

            <p className="mt-3 leading-7 text-muted-foreground">
              {result.reassurance}
            </p>
          </section>

          {/* Risk factors */}
          {analysis.risk_scores.length > 0 && (
            <section className="rounded-2xl border bg-card p-6">
              <h2 className="text-xl font-bold">
                Why SafeStep flagged this
              </h2>

              <div className="mt-5 space-y-4">
                {analysis.risk_scores.map((risk) => (
                  <div
                    key={risk.risk_factor}
                    className="rounded-xl border p-4"
                  >
                    <div className="flex items-center justify-between gap-4">
                      <p className="font-semibold">
                        {risk.risk_factor
                          .replaceAll('_', ' ')
                          .replace(/\b\w/g, (letter) =>
                            letter.toUpperCase(),
                          )}
                      </p>

                      <span className="text-sm font-medium text-muted-foreground">
                        {Math.round(risk.score * 100)}%
                      </span>
                    </div>

                    <div className="mt-3 h-2 overflow-hidden rounded-full bg-muted">
                      <div
                        className="h-full rounded-full bg-primary"
                        style={{
                          width: `${Math.min(
                            Math.max(risk.score * 100, 0),
                            100,
                          )}%`,
                        }}
                      />
                    </div>

                    <p className="mt-3 text-sm leading-6 text-muted-foreground">
                      {risk.explanation}
                    </p>
                  </div>
                ))}
              </div>
            </section>
          )}
        </div>
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