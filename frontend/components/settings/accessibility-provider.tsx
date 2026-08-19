'use client'

import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react'

export type TextSize = 'default' | 'large' | 'xlarge'

export interface AccessibilityPrefs {
  textSize: TextSize
  highContrast: boolean
  reducedMotion: boolean
}

interface AccessibilityContextValue extends AccessibilityPrefs {
  setTextSize: (size: TextSize) => void
  setHighContrast: (on: boolean) => void
  setReducedMotion: (on: boolean) => void
}

const STORAGE_KEY = 'safestep.accessibility'

const DEFAULTS: AccessibilityPrefs = {
  textSize: 'default',
  highContrast: false,
  reducedMotion: false,
}

const AccessibilityContext = createContext<AccessibilityContextValue | null>(
  null,
)

/**
 * These are purely front-end display preferences (the backend does not need
 * to support them). They are applied as data-attributes on <html> and read by
 * globals.css.
 */
export function AccessibilityProvider({
  children,
}: {
  children: React.ReactNode
}) {
  const [prefs, setPrefs] = useState<AccessibilityPrefs>(DEFAULTS)

  // Load saved preferences on mount.
  useEffect(() => {
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY)
      if (raw) setPrefs({ ...DEFAULTS, ...JSON.parse(raw) })
    } catch {
      /* ignore malformed storage */
    }
  }, [])

  // Reflect preferences onto <html> and persist them.
  useEffect(() => {
    const root = document.documentElement
    root.dataset.textSize = prefs.textSize
    root.dataset.contrast = prefs.highContrast ? 'high' : 'normal'
    root.dataset.reducedMotion = prefs.reducedMotion ? 'true' : 'false'
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs))
    } catch {
      /* ignore quota errors */
    }
  }, [prefs])

  const value = useMemo<AccessibilityContextValue>(
    () => ({
      ...prefs,
      setTextSize: (textSize) => setPrefs((p) => ({ ...p, textSize })),
      setHighContrast: (highContrast) =>
        setPrefs((p) => ({ ...p, highContrast })),
      setReducedMotion: (reducedMotion) =>
        setPrefs((p) => ({ ...p, reducedMotion })),
    }),
    [prefs],
  )

  return (
    <AccessibilityContext.Provider value={value}>
      {children}
    </AccessibilityContext.Provider>
  )
}

export function useAccessibility(): AccessibilityContextValue {
  const ctx = useContext(AccessibilityContext)
  if (!ctx)
    throw new Error(
      'useAccessibility must be used within AccessibilityProvider',
    )
  return ctx
}
