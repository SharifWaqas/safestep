'use client'

import { Accessibility, Eye, Gauge, Settings2 } from 'lucide-react'

import { useAccessibility } from '@/components/settings/accessibility-provider'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Switch } from '@/components/ui/switch'

export default function SettingsPage() {
  const {
    textSize,
    highContrast,
    reducedMotion,
    setTextSize,
    setHighContrast,
    setReducedMotion,
  } = useAccessibility()

  return (
    <main className="mx-auto w-full max-w-4xl px-4 py-10 sm:px-6">
      <div className="mb-8">
        <div className="flex items-center gap-3">
          <span
            className="flex size-11 items-center justify-center rounded-xl bg-primary/10 text-primary"
            aria-hidden="true"
          >
            <Settings2 className="size-6" />
          </span>

          <div>
            <h1 className="text-3xl font-bold tracking-tight">
              Settings
            </h1>

            <p className="mt-1 text-muted-foreground">
              Adjust SafeStep to make it easier and more comfortable to use.
            </p>
          </div>
        </div>
      </div>

      <section
        aria-labelledby="accessibility-heading"
        className="rounded-2xl border bg-card p-6 sm:p-8"
      >
        <div className="flex items-start gap-4">
          <span
            className="flex size-11 shrink-0 items-center justify-center rounded-xl bg-secondary text-secondary-foreground"
            aria-hidden="true"
          >
            <Accessibility className="size-6" />
          </span>

          <div>
            <h2
              id="accessibility-heading"
              className="text-2xl font-bold tracking-tight"
            >
              Accessibility
            </h2>

            <p className="mt-1 text-muted-foreground">
              Personalize the way SafeStep looks and behaves.
            </p>
          </div>
        </div>

        <div className="mt-8 divide-y">
          <div className="flex flex-col gap-4 py-5 first:pt-0 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-start gap-3">
              <Eye
                className="mt-0.5 size-5 shrink-0 text-muted-foreground"
                aria-hidden="true"
              />

              <div>
                <Label
                  htmlFor="text-size"
                  className="text-base"
                >
                  Text size
                </Label>

                <p className="mt-1 text-sm text-muted-foreground">
                  Choose the text size used throughout SafeStep.
                </p>
              </div>
            </div>

            <Select
              value={textSize}
              onValueChange={(value) => {
                if (
                  value === 'default' ||
                  value === 'large' ||
                  value === 'xlarge'
                ) {
                  setTextSize(value)
                }
              }}
            >
              <SelectTrigger
                id="text-size"
                size="default"
                className="w-full sm:w-40"
                aria-label="Text size"
              >
                <SelectValue />
              </SelectTrigger>

              <SelectContent>
                <SelectItem value="default">
                  Default
                </SelectItem>

                <SelectItem value="large">
                  Large
                </SelectItem>

                <SelectItem value="xlarge">
                  Extra large
                </SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="flex items-center justify-between gap-4 py-5">
            <div className="flex items-start gap-3">
              <Gauge
                className="mt-0.5 size-5 shrink-0 text-muted-foreground"
                aria-hidden="true"
              />

              <div>
                <p className="text-base font-medium">
                  High contrast
                </p>

                <p className="mt-1 text-sm text-muted-foreground">
                  Increase visual contrast between interface elements.
                </p>
              </div>
            </div>

            <Switch
              checked={highContrast}
              onCheckedChange={setHighContrast}
              aria-label="High contrast"
            />
          </div>

          <div className="flex items-center justify-between gap-4 py-5 last:pb-0">
            <div className="flex items-start gap-3">
              <span
                className="mt-0.5 flex size-5 items-center justify-center text-muted-foreground"
                aria-hidden="true"
              >
                <span className="size-3 rounded-full border-2" />
              </span>

              <div>
                <p className="text-base font-medium">
                  Reduced motion
                </p>

                <p className="mt-1 text-sm text-muted-foreground">
                  Reduce animations and motion effects throughout the app.
                </p>
              </div>
            </div>

            <Switch
              checked={reducedMotion}
              onCheckedChange={setReducedMotion}
              aria-label="Reduced motion"
            />
          </div>
        </div>
      </section>
    </main>
  )
}