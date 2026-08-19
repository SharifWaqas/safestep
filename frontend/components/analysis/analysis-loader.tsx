'use client'

import { useEffect, useState } from 'react'
import { Check, ShieldCheck } from 'lucide-react'
import { Spinner } from '@/components/ui/spinner'
import { cn } from '@/lib/utils'

const STEPS = [
  'Reading the message',
  'Looking for warning signs',
  'Assessing risk',
  'Preparing guidance',
] as const

/**
 * A calm, reassuring loading experience for the (possibly several second)
 * AI analysis. Steps advance on a gentle timer so the interface never looks
 * frozen or broken.
 */
export function AnalysisLoader() {
  const [active, setActive] = useState(0)

  useEffect(() => {
    if (active >= STEPS.length - 1) return
    const timer = setTimeout(() => setActive((s) => s + 1), 1600)
    return () => clearTimeout(timer)
  }, [active])

  return (
    <div className="mx-auto flex max-w-xl flex-col items-center rounded-2xl border bg-card p-8 text-center sm:p-10">
      <span
        className="flex size-16 items-center justify-center rounded-2xl bg-primary/10 text-primary"
        aria-hidden="true"
      >
        <ShieldCheck className="size-8" />
      </span>
      <h2 className="mt-5 text-2xl font-bold tracking-tight">
        SafeStep is reviewing this message
      </h2>
      <p className="mt-2 text-pretty text-lg text-muted-foreground">
        This usually takes a few seconds. Please stay on this page.
      </p>

      <ul
        className="mt-8 flex w-full flex-col gap-3 text-left"
        aria-live="polite"
      >
        {STEPS.map((step, i) => {
          const done = i < active
          const current = i === active
          return (
            <li
              key={step}
              className={cn(
                'flex items-center gap-3 rounded-xl border px-4 py-3 text-lg transition-colors',
                done && 'border-safe/30 bg-safe-subtle',
                current && 'border-primary/30 bg-primary/5',
                !done && !current && 'border-border bg-muted/40',
              )}
            >
              <span className="flex size-7 shrink-0 items-center justify-center">
                {done ? (
                  <span className="flex size-7 items-center justify-center rounded-full bg-safe text-safe-foreground">
                    <Check className="size-4" aria-hidden="true" />
                  </span>
                ) : current ? (
                  <Spinner className="size-6 text-primary" />
                ) : (
                  <span className="size-3 rounded-full bg-foreground/20" />
                )}
              </span>
              <span
                className={cn(
                  'font-medium',
                  done && 'text-foreground',
                  current && 'text-foreground',
                  !done && !current && 'text-muted-foreground',
                )}
              >
                {step}
                {done && <span className="sr-only"> — complete</span>}
                {current && <span className="sr-only"> — in progress</span>}
              </span>
            </li>
          )
        })}
      </ul>
    </div>
  )
}
