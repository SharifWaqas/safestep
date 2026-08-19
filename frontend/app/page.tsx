import Link from 'next/link'
import {
  ArrowRight,
  ImageUp,
  MessageSquare,
  ShieldCheck,
  Lock,
  Heart,
  Eye,
} from 'lucide-react'
import { Logo } from '@/components/brand/logo'
import { PublicHeader } from '@/components/landing/public-header'
import { FlowVisual } from '@/components/landing/flow-visual'

const howItWorks = [
  {
    icon: ImageUp,
    title: '1. Upload',
    body: 'Take a screenshot of a message, email, or website you are unsure about, and upload it to SafeStep.',
  },
  {
    icon: MessageSquare,
    title: '2. Understand',
    body: 'SafeStep explains, in plain language, what the message is and whether it shows any warning signs.',
  },
  {
    icon: ShieldCheck,
    title: '3. Stay safe',
    body: 'You get clear, calm advice on what to do next — and reassurance so you never have to panic.',
  },
]

const trustPoints = [
  {
    icon: Eye,
    title: 'Understand before you act',
    body: 'SafeStep helps you slow down and see what a message really is, before you click, reply, or pay.',
  },
  {
    icon: Heart,
    title: 'Calm, never alarming',
    body: 'We explain things gently and clearly. No jargon, no scare tactics — just guidance you can trust.',
  },
  {
    icon: Lock,
    title: 'You are in control',
    body: 'You choose what to upload. SafeStep gives advice; you always decide what to do next.',
  },
]

export default function LandingPage() {
  return (
    <div className="flex min-h-dvh flex-col">
      <PublicHeader />

      <main className="flex-1">
        {/* Hero */}
        <section className="mx-auto w-full max-w-6xl px-4 py-14 sm:px-6 sm:py-20">
          <div className="grid items-center gap-10 lg:grid-cols-2 lg:gap-14">
            <div>
              <span className="inline-flex items-center gap-2 rounded-full border bg-card px-4 py-1.5 text-base font-medium text-muted-foreground">
                <ShieldCheck
                  className="size-4 text-primary"
                  aria-hidden="true"
                />
                Your digital safety companion
              </span>

              <h1 className="mt-5 text-balance text-4xl font-extrabold tracking-tight sm:text-5xl lg:text-6xl">
                Not sure if a message is safe?
              </h1>

              <p className="mt-5 max-w-xl text-pretty text-xl leading-relaxed text-muted-foreground">
                SafeStep helps you understand suspicious messages, links, and
                screenshots before you take action.
              </p>

              <div className="mt-8 flex flex-col gap-3 sm:flex-row">
                <Link
                  href="/analyze"
                  className="inline-flex h-14 items-center justify-center gap-2 rounded-md bg-primary px-7 text-lg font-medium text-primary-foreground transition-colors hover:bg-primary/90"
                >
                  Analyze a message
                  <ArrowRight
                    className="size-5"
                    aria-hidden="true"
                  />
                </Link>

                <Link
                  href="#how-it-works"
                  className="inline-flex h-14 items-center justify-center rounded-md border bg-background px-7 text-lg font-medium transition-colors hover:bg-accent hover:text-accent-foreground"
                >
                  Learn how SafeStep works
                </Link>
              </div>

              <p className="mt-4 text-base text-muted-foreground">
                Understand first. Act safely.
              </p>
            </div>

            <div className="lg:pl-4">
              <FlowVisual />
            </div>
          </div>
        </section>

        {/* How it works */}
        <section
          id="how-it-works"
          aria-labelledby="how-it-works-heading"
          className="border-y bg-card/50"
        >
          <div className="mx-auto w-full max-w-6xl px-4 py-14 sm:px-6 sm:py-20">
            <div className="mx-auto max-w-2xl text-center">
              <h2
                id="how-it-works-heading"
                className="text-balance text-3xl font-extrabold tracking-tight sm:text-4xl"
              >
                Three simple steps
              </h2>

              <p className="mt-3 text-pretty text-xl text-muted-foreground">
                SafeStep is designed to be easy for everyone to use.
              </p>
            </div>

            <div className="mt-10 grid gap-6 md:grid-cols-3">
              {howItWorks.map((step) => {
                const Icon = step.icon

                return (
                  <div
                    key={step.title}
                    className="rounded-2xl border bg-background p-7"
                  >
                    <span
                      className="flex size-14 items-center justify-center rounded-2xl bg-primary/10 text-primary"
                      aria-hidden="true"
                    >
                      <Icon className="size-7" />
                    </span>

                    <h3 className="mt-5 text-2xl font-bold tracking-tight">
                      {step.title}
                    </h3>

                    <p className="mt-2 text-pretty text-lg leading-relaxed text-muted-foreground">
                      {step.body}
                    </p>
                  </div>
                )
              })}
            </div>
          </div>
        </section>

        {/* Trust / reassurance */}
        <section
          aria-labelledby="trust-heading"
          className="mx-auto w-full max-w-6xl px-4 py-14 sm:px-6 sm:py-20"
        >
          <div className="mx-auto max-w-2xl text-center">
            <h2
              id="trust-heading"
              className="text-balance text-3xl font-extrabold tracking-tight sm:text-4xl"
            >
              Built to help you feel confident
            </h2>

            <p className="mt-3 text-pretty text-xl text-muted-foreground">
              SafeStep is here to guide you, not to frighten you.
            </p>
          </div>

          <div className="mt-10 grid gap-6 md:grid-cols-3">
            {trustPoints.map((point) => {
              const Icon = point.icon

              return (
                <div
                  key={point.title}
                  className="rounded-2xl border bg-card p-7"
                >
                  <span
                    className="flex size-12 items-center justify-center rounded-xl bg-secondary text-secondary-foreground"
                    aria-hidden="true"
                  >
                    <Icon className="size-6" />
                  </span>

                  <h3 className="mt-5 text-xl font-bold tracking-tight">
                    {point.title}
                  </h3>

                  <p className="mt-2 text-pretty text-lg leading-relaxed text-muted-foreground">
                    {point.body}
                  </p>
                </div>
              )
            })}
          </div>
        </section>

        {/* Call to action */}
        <section className="mx-auto w-full max-w-6xl px-4 pb-16 sm:px-6 sm:pb-24">
          <div className="rounded-3xl border bg-primary px-6 py-12 text-center text-primary-foreground sm:px-10 sm:py-16">
            <h2 className="text-balance text-3xl font-extrabold tracking-tight sm:text-4xl">
              Have a message you are unsure about?
            </h2>

            <p className="mx-auto mt-3 max-w-xl text-pretty text-xl text-primary-foreground/90">
              SafeStep will help you understand it and decide what to do —
              calmly and clearly.
            </p>

            <div className="mt-8 flex justify-center">
              <Link
                href="/analyze"
                className="inline-flex h-14 items-center justify-center gap-2 rounded-md bg-secondary px-7 text-lg font-medium text-secondary-foreground transition-colors hover:bg-secondary/80"
              >
                Analyze a message
                <ArrowRight
                  className="size-5"
                  aria-hidden="true"
                />
              </Link>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t bg-card">
        <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-4 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-6">
          <Logo size="sm" />

          <p className="text-base text-muted-foreground">
            SafeStep gives guidance to help you stay safe. Always verify
            important matters through official channels.
          </p>
        </div>
      </footer>
    </div>
  )
}