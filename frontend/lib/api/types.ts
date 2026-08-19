/**
 * Types matching the existing SafeStep FastAPI backend response contracts.
 * DO NOT change these to match the UI — the UI adapts to the backend.
 */

export type RiskLevel = 'SAFE' | 'LOW' | 'MEDIUM' | 'HIGH' | 'VERY_HIGH'

export type AnalysisStatus =
  | 'pending'
  | 'processing'
  | 'completed'
  | 'failed'

/** Known risk factor keys returned by the backend. Unknown keys are handled gracefully. */
export type RiskFactorKey =
  | 'suspicious_link'
  | 'suspicious_domain'
  | 'urgency_language'
  | 'threat_language'
  | 'credential_request'
  | 'financial_request'
  | 'payment_request'
  | 'brand_impersonation'
  | 'unknown_sender'
  | 'login_form'
  | 'reward_language'
  | 'unrealistic_price'
  | (string & {})

export interface RiskScore {
  risk_factor: RiskFactorKey
  /** Score between 0 and 1 */
  score: number
  explanation: string
}

export interface AiResult {
  summary: string
  explanation: string
  guidance: string
  reassurance: string
  risk_level: RiskLevel
}

export interface Analysis {
  analysis_id: string
  upload_id: string
  status: AnalysisStatus
  started_at: string
  completed_at: string | null
  ai_result: AiResult | null
  risk_scores: RiskScore[]
}

export interface Upload {
  upload_id: string
  filename?: string
  content_type?: string
  size?: number
  created_at?: string
}

export interface User {
  id: string
  email: string
  name?: string
  created_at?: string
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export interface LoginPayload {
  email: string
  password: string
}

export interface RegisterPayload {
  full_name: string
  email: string
  password: string
}