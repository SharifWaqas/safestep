import { HelpCircle, Search, ListChecks, ShieldAlert } from 'lucide-react'
import type { Analysis } from '@/lib/api/types'
import { RiskLevelCard } from '@/components/risk/risk-level-card'
import { RiskFactorCard } from '@/components/risk/risk-factor-card'
import { AnalysisSection } from '@/components/analysis/analysis-section'
import { ReassuranceCard } from '@/components/analysis/reassurance-card'

interface AnalysisResultProps {
  analysis: Analysis
}

/**
 * The full analysis result screen content, in a deliberate reading order:
 * risk level -> what is this -> why suspicious -> what to do -> reassurance
 * -> warning signs.
 */
export function AnalysisResult({ analysis }: AnalysisResultProps) {
  const ai = analysis.ai_result
  const factors = [...analysis.risk_scores].sort((a, b) => b.score - a.score)

  if (!ai) {
    return (
      <RiskLevelCard level="MEDIUM" />
    )
  }

  return (
    <div className="flex flex-col gap-6">
      <RiskLevelCard level={ai.risk_level} />

      <AnalysisSection icon={HelpCircle} heading="What is this?">
        {ai.summary}
      </AnalysisSection>

      <AnalysisSection icon={Search} heading="Why is this suspicious?">
        {ai.explanation}
      </AnalysisSection>

      <AnalysisSection
        icon={ListChecks}
        heading="What should I do?"
        emphasized
      >
        {ai.guidance}
      </AnalysisSection>

      <ReassuranceCard message={ai.reassurance} />

      {factors.length > 0 && (
        <section aria-labelledby="warning-signs-heading">
          <div className="flex items-center gap-3">
            <span
              className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-muted text-foreground"
              aria-hidden="true"
            >
              <ShieldAlert className="size-5" />
            </span>
            <h3
              id="warning-signs-heading"
              className="text-xl font-bold tracking-tight sm:text-2xl"
            >
              Warning signs SafeStep found
            </h3>
          </div>
          <ul className="mt-4 flex flex-col gap-3">
            {factors.map((factor, i) => (
              <RiskFactorCard key={`${factor.risk_factor}-${i}`} factor={factor} />
            ))}
          </ul>
        </section>
      )}
    </div>
  )
}
