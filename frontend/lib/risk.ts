import type { RiskFactorKey, RiskLevel } from '@/lib/api/types'

/* ------------------------------------------------------------------ */
/* Risk levels                                                          */
/* ------------------------------------------------------------------ */

export interface RiskLevelMeta {
  level: RiskLevel
  /** Short label shown to users, e.g. "High risk". */
  label: string
  /** One calm sentence describing what the level means. */
  description: string
  /** Design-token color family name (see globals.css risk tokens). */
  token: 'safe' | 'low' | 'medium' | 'high' | 'critical'
  /** Ordering weight, higher = more dangerous. */
  weight: number
}

export const RISK_LEVELS: Record<RiskLevel, RiskLevelMeta> = {
  SAFE: {
    level: 'SAFE',
    label: 'Safe',
    description: 'This appears to be genuine. Nothing here should worry you.',
    token: 'safe',
    weight: 0,
  },
  LOW: {
    level: 'LOW',
    label: 'Low risk',
    description: 'This looks mostly fine, but stay a little cautious.',
    token: 'low',
    weight: 1,
  },
  MEDIUM: {
    level: 'MEDIUM',
    label: 'Medium risk',
    description: 'This shows some warning signs. Take a moment before acting.',
    token: 'medium',
    weight: 2,
  },
  HIGH: {
    level: 'HIGH',
    label: 'High risk',
    description: 'This shows several warning signs. Please be careful.',
    token: 'high',
    weight: 3,
  },
  VERY_HIGH: {
    level: 'VERY_HIGH',
    label: 'Very high risk',
    description: 'This looks very likely to be a scam. Do not act on it.',
    token: 'critical',
    weight: 4,
  },
}

/** Safe fallback for any unexpected value from the backend. */
export function getRiskMeta(level: string | null | undefined): RiskLevelMeta {
  if (level && level in RISK_LEVELS) {
    return RISK_LEVELS[level as RiskLevel]
  }
  return RISK_LEVELS.MEDIUM
}

/* ------------------------------------------------------------------ */
/* Risk factors — enum key -> human-readable label                      */
/* ------------------------------------------------------------------ */

const RISK_FACTOR_LABELS: Record<string, string> = {
  suspicious_link: 'Suspicious link',
  suspicious_domain: 'Suspicious website address',
  urgency_language: 'Urgency language',
  threat_language: 'Threatening language',
  credential_request: 'Password request',
  financial_request: 'Money request',
  payment_request: 'Payment request',
  brand_impersonation: 'Pretending to be a known company',
  unknown_sender: 'Unknown sender',
  login_form: 'Fake login form',
  reward_language: 'Prize or reward offer',
  unrealistic_price: 'Too-good-to-be-true price',
}

/**
 * Convert a backend enum key like `payment_request` into a friendly label.
 * Falls back to title-casing unknown keys so nothing raw ever reaches users.
 */
export function riskFactorLabel(key: RiskFactorKey): string {
  if (key in RISK_FACTOR_LABELS) return RISK_FACTOR_LABELS[key]
  return key
    .split('_')
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ')
}

/* ------------------------------------------------------------------ */
/* Scores (0..1) -> human-readable bands                                */
/* ------------------------------------------------------------------ */

export interface ScoreBand {
  label: string
  /** 0..100 for progress meters. */
  percent: number
  token: 'safe' | 'medium' | 'high' | 'critical'
}

export function scoreBand(score: number): ScoreBand {
  const clamped = Math.max(0, Math.min(1, score))
  const percent = Math.round(clamped * 100)
  if (clamped < 0.25)
    return { label: 'Minor sign', percent, token: 'safe' }
  if (clamped < 0.5)
    return { label: 'Moderate warning', percent, token: 'medium' }
  if (clamped < 0.75)
    return { label: 'Strong warning', percent, token: 'high' }
  return { label: 'Serious warning', percent, token: 'critical' }
}
