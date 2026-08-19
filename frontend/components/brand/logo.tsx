import Link from 'next/link'
import { ShieldCheck } from 'lucide-react'
import { cn } from '@/lib/utils'

interface LogoProps {
  href?: string
  className?: string
  /** Hide the wordmark, show only the shield mark. */
  markOnly?: boolean
  size?: 'sm' | 'md' | 'lg'
}

const sizes = {
  sm: { box: 'size-8', icon: 'size-5', text: 'text-lg' },
  md: { box: 'size-10', icon: 'size-6', text: 'text-xl' },
  lg: { box: 'size-12', icon: 'size-7', text: 'text-2xl' },
}

export function Logo({
  href = '/',
  className,
  markOnly = false,
  size = 'md',
}: LogoProps) {
  const s = sizes[size]
  const content = (
    <span className={cn('flex items-center gap-2.5', className)}>
      <span
        className={cn(
          'flex items-center justify-center rounded-xl bg-primary text-primary-foreground',
          s.box,
        )}
        aria-hidden="true"
      >
        <ShieldCheck className={s.icon} />
      </span>
      {!markOnly && (
        <span className={cn('font-heading font-extrabold tracking-tight', s.text)}>
          SafeStep
        </span>
      )}
    </span>
  )

  if (href) {
    return (
      <Link href={href} className="inline-flex" aria-label="SafeStep home">
        {content}
      </Link>
    )
  }
  return content
}
