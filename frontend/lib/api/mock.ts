/**
 * ISOLATED MOCK LAYER — for previewing the UI without the real backend.
 *
 * This entire file can be deleted once NEXT_PUBLIC_API_URL points at the real
 * FastAPI backend. Nothing here pretends to be the backend: the service layer
 * only reaches for these functions when USE_MOCKS is true (see lib/api/config).
 */

import type {
  Analysis,
  AuthTokens,
  LoginPayload,
  RegisterPayload,
  Upload,
} from './types'
import { mockDelay } from './config'

function uid(prefix: string): string {
  return `${prefix}-${Math.random().toString(36).slice(2, 10)}`
}

const sampleAnalyses: Analysis[] = [
  {
    analysis_id: 'a-1001',
    upload_id: 'u-1001',
    status: 'completed',
    started_at: '2026-08-18T14:12:00Z',
    completed_at: '2026-08-18T14:12:07Z',
    ai_result: {
      risk_level: 'HIGH',
      summary:
        'This looks like a text message claiming to be from your bank, asking you to confirm a payment by tapping a link.',
      explanation:
        'Real banks do not ask you to confirm payments through a link in a text message. The message uses urgent wording to make you act quickly, and the link does not go to your bank’s official website.',
      guidance:
        'Do not tap the link and do not enter any details. If you want to check your account, open your bank’s official app or type their website address yourself. You can also call the phone number on the back of your bank card.',
      reassurance:
        'You have not done anything wrong by receiving this message. As long as you did not tap the link or share any details, your money and information are safe.',
    },
    risk_scores: [
      {
        risk_factor: 'suspicious_link',
        score: 0.82,
        explanation: 'The link does not lead to your bank’s real website.',
      },
      {
        risk_factor: 'urgency_language',
        score: 0.74,
        explanation: 'The message pressures you to act immediately.',
      },
      {
        risk_factor: 'brand_impersonation',
        score: 0.68,
        explanation: 'It pretends to be from a bank you may recognise.',
      },
      {
        risk_factor: 'payment_request',
        score: 0.45,
        explanation: 'It refers to a payment to make you worried.',
      },
    ],
  },
  {
    analysis_id: 'a-1002',
    upload_id: 'u-1002',
    status: 'completed',
    started_at: '2026-08-15T09:30:00Z',
    completed_at: '2026-08-15T09:30:05Z',
    ai_result: {
      risk_level: 'SAFE',
      summary:
        'This is an order confirmation email from a shop, letting you know your order has shipped.',
      explanation:
        'The message matches a normal shipping update. It does not ask for any personal details, passwords, or payments, and the sender address matches the shop.',
      guidance:
        'No action is needed. If you want to track your parcel, you can visit the shop’s website directly rather than using any links, just to be safe.',
      reassurance:
        'This message appears to be genuine. There is nothing here that should worry you.',
    },
    risk_scores: [
      {
        risk_factor: 'unknown_sender',
        score: 0.12,
        explanation: 'The sender is a recognisable shop.',
      },
    ],
  },
  {
    analysis_id: 'a-1003',
    upload_id: 'u-1003',
    status: 'completed',
    started_at: '2026-08-10T17:45:00Z',
    completed_at: '2026-08-10T17:45:09Z',
    ai_result: {
      risk_level: 'MEDIUM',
      summary:
        'This is an email saying you have won a prize and need to click a link to claim it.',
      explanation:
        'Messages that say you have won a prize you did not enter are a common trick. They try to get you excited so you click without thinking. The reward offer is a warning sign.',
      guidance:
        'Do not click the link or reply. It is safe to simply delete this message. Real prizes do not require you to hand over personal details to claim them.',
      reassurance:
        'Receiving this does not mean anyone has your information. Deleting it is enough to stay safe.',
    },
    risk_scores: [
      {
        risk_factor: 'reward_language',
        score: 0.66,
        explanation: 'It promises a prize to tempt you.',
      },
      {
        risk_factor: 'suspicious_link',
        score: 0.4,
        explanation: 'The link destination is unclear.',
      },
      {
        risk_factor: 'unknown_sender',
        score: 0.38,
        explanation: 'The sender is not someone you know.',
      },
    ],
  },
]

// A working copy so newly-created analyses persist for the session.
let store: Analysis[] = [...sampleAnalyses]

export const mockApi = {
  async login(payload: LoginPayload): Promise<AuthTokens> {
    await mockDelay()

    if (!payload.email || !payload.password) {
      throw new Error('missing credentials')
    }

    return {
      access_token: 'mock-token',
      refresh_token: 'mock-refresh-token',
      token_type: 'Bearer',
      expires_in: 3600,
    }
  },

  async register(_payload: RegisterPayload): Promise<AuthTokens> {
    await mockDelay()

    return {
      access_token: 'mock-token',
      refresh_token: 'mock-refresh-token',
      token_type: 'Bearer',
      expires_in: 3600,
    }
  },

  async createUpload(file: File): Promise<Upload> {
    await mockDelay(700)

    return {
      upload_id: uid('u'),
      filename: file.name,
      content_type: file.type,
      size: file.size,
      created_at: new Date().toISOString(),
    }
  },

  async createAnalysis(uploadId: string): Promise<Analysis> {
    await mockDelay(2600)

    const template = sampleAnalyses[0]

    const analysis: Analysis = {
      ...template,
      analysis_id: uid('a'),
      upload_id: uploadId,
      started_at: new Date().toISOString(),
      completed_at: new Date().toISOString(),
    }

    store = [analysis, ...store]

    return analysis
  },

  async getAnalysis(analysisId: string): Promise<Analysis> {
    await mockDelay(300)

    const found = store.find(
      (analysis) => analysis.analysis_id === analysisId,
    )

    if (!found) {
      throw new Error('not found')
    }

    return found
  },

  async listAnalyses(): Promise<Analysis[]> {
    await mockDelay(400)

    return store
  },
}