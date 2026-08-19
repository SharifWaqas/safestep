import {
  ShieldCheck,
  ShieldAlert,
  ShieldQuestion,
  ShieldOff,
  OctagonAlert,
  Link2,
  Globe,
  Clock,
  TriangleAlert,
  KeyRound,
  CircleDollarSign,
  CreditCard,
  BadgeAlert,
  UserX,
  LogIn,
  Gift,
  Tag,
  type LucideIcon,
} from 'lucide-react'
import type { RiskFactorKey, RiskLevel } from '@/lib/api/types'

/**
 * Maps each risk level to an icon. Meaning is ALWAYS carried by icon + text,
 * never by color alone.
 */
export const RISK_LEVEL_ICON: Record<RiskLevel, LucideIcon> = {
  SAFE: ShieldCheck,
  LOW: ShieldQuestion,
  MEDIUM: ShieldAlert,
  HIGH: ShieldAlert,
  VERY_HIGH: OctagonAlert,
}

export const RISK_FALLBACK_ICON: LucideIcon = ShieldOff

const RISK_FACTOR_ICON: Record<string, LucideIcon> = {
  suspicious_link: Link2,
  suspicious_domain: Globe,
  urgency_language: Clock,
  threat_language: TriangleAlert,
  credential_request: KeyRound,
  financial_request: CircleDollarSign,
  payment_request: CreditCard,
  brand_impersonation: BadgeAlert,
  unknown_sender: UserX,
  login_form: LogIn,
  reward_language: Gift,
  unrealistic_price: Tag,
}

export function riskFactorIcon(key: RiskFactorKey): LucideIcon {
  return RISK_FACTOR_ICON[key] ?? TriangleAlert
}
