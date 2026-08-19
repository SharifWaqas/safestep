import { ShieldCheck } from 'lucide-react'

interface ReassuranceCardProps {
  message: string
}

/**
 * A calm, supportive closing note. Uses the "safe" tone regardless of the
 * risk level, because its job is to reassure the person, not alarm them.
 */
export function ReassuranceCard({ message }: ReassuranceCardProps) {
  return (
    <section className="rounded-2xl border border-safe/30 bg-safe-subtle p-6 sm:p-7">
      <div className="flex items-center gap-3">
        <span
          className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-safe text-safe-foreground"
          aria-hidden="true"
        >
          <ShieldCheck className="size-5" />
        </span>
        <h3 className="text-xl font-bold tracking-tight text-safe sm:text-2xl">
          You are okay
        </h3>
      </div>
      <p className="mt-4 text-pretty text-lg leading-relaxed text-foreground/85">
        {message}
      </p>
    </section>
  )
}
