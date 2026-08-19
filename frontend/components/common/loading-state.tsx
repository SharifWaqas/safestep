import { Skeleton } from '@/components/ui/skeleton'

/** Generic centered loading indicator for full-page auth checks. */
export function LoadingState({ label = 'Loading…' }: { label?: string }) {
  return (
    <div className="flex min-h-[40vh] flex-col items-center justify-center gap-4">
      <Skeleton className="size-12 rounded-2xl" />
      <p className="text-lg text-muted-foreground">{label}</p>
    </div>
  )
}

/** Skeleton list used while analyses load on the History page. */
export function CardListSkeleton({ count = 3 }: { count?: number }) {
  return (
    <ul className="flex flex-col gap-4" aria-hidden="true">
      {Array.from({ length: count }).map((_, i) => (
        <li key={i} className="rounded-2xl border bg-card p-5">
          <div className="flex items-center gap-4">
            <Skeleton className="size-12 rounded-xl" />
            <div className="flex-1">
              <Skeleton className="h-5 w-1/3 rounded-md" />
              <Skeleton className="mt-2 h-4 w-2/3 rounded-md" />
            </div>
            <Skeleton className="h-8 w-20 rounded-full" />
          </div>
        </li>
      ))}
    </ul>
  )
}
