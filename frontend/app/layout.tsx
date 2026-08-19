import { Analytics } from '@vercel/analytics/next'
import type { Metadata, Viewport } from 'next'
import { Public_Sans, Plus_Jakarta_Sans } from 'next/font/google'
import { Toaster } from '@/components/ui/sonner'
import { AuthProvider } from '@/components/auth/auth-provider'
import { AccessibilityProvider } from '@/components/settings/accessibility-provider'
import './globals.css'

const publicSans = Public_Sans({
  subsets: ['latin'],
  variable: '--font-public-sans',
  display: 'swap',
})

const jakarta = Plus_Jakarta_Sans({
  subsets: ['latin'],
  weight: ['600', '700', '800'],
  variable: '--font-jakarta',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'SafeStep — Understand suspicious messages before you act',
  description:
    'SafeStep helps you understand suspicious messages, links, and screenshots before you take action. Upload a screenshot and get a calm, clear explanation.',
  generator: 'v0.app',
}

export const viewport: Viewport = {
  colorScheme: 'light',
  themeColor: '#ffffff',
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className={`${publicSans.variable} ${jakarta.variable}`}>
      <body className="antialiased">
        <AccessibilityProvider>
          <AuthProvider>{children}</AuthProvider>
        </AccessibilityProvider>
        <Toaster position="top-center" />
        {process.env.NODE_ENV === 'production' && <Analytics />}
      </body>
    </html>
  )
}
