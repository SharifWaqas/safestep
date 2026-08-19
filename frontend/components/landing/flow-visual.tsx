import { ImageUp, ShieldCheck, MessageSquare, Check, ArrowRight } from 'lucide-react'

const steps = [
  { icon: ImageUp, label: 'Screenshot', tone: 'bg-muted text-foreground' },
  { icon: ShieldCheck, label: 'SafeStep', tone: 'bg-primary text-primary-foreground' },
  { icon: MessageSquare, label: 'Clear explanation', tone: 'bg-muted text-foreground' },
  { icon: Check, label: 'Safe action', tone: 'bg-safe text-safe-foreground' },
]

/** Simple, non-decorative representation of how SafeStep processes a message. */
export function FlowVisual() {
  return (
    <div className="rounded-2xl border bg-card p-6 sm:p-8">
      <ol className="flex flex-col items-stretch gap-3 sm:flex-row sm:items-center sm:justify-between">
        {steps.map((step, i) => {
          const Icon = step.icon
          return (
            <li
              key={step.label}
              className="flex items-center gap-3 sm:flex-col sm:gap-2 sm:text-center"
            >
              <span
                className={`flex size-14 shrink-0 items-center justify-center rounded-2xl ${step.tone}`}
                aria-hidden="true"
              >
                <Icon className="size-7" />
              </span>
              <span className="text-base font-semibold sm:text-lg">
                {step.label}
              </span>
              {i < steps.length - 1 && (
                <ArrowRight
                  className="ml-auto size-5 shrink-0 rotate-90 text-muted-foreground sm:ml-0 sm:hidden"
                  aria-hidden="true"
                />
              )}
            </li>
          )
        })}
      </ol>
    </div>
  )
}
