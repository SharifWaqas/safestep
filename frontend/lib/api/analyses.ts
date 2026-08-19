/**
 * Analyses service.
 *   POST /analyses/{upload_id}   -> start an analysis for an upload
 *   GET  /analyses/{analysis_id} -> fetch a completed analysis
 *
 * INTEGRATION NOTE: the history endpoint below (GET /analyses) is assumed.
 * If the backend exposes a different path for listing a user's analyses,
 * update LIST_ENDPOINT — this is the only place it needs to change.
 */

import { apiClient } from './client'
import { USE_MOCKS } from './config'
import { mockApi } from './mock'
import type { Analysis } from './types'

const LIST_ENDPOINT = '/analyses'

export const analysesApi = {
  /** Start analysis for a previously created upload. AI work can take seconds. */
  async create(uploadId: string): Promise<Analysis> {
    if (USE_MOCKS) return mockApi.createAnalysis(uploadId)
    return apiClient.post<Analysis>(`/analyses/${uploadId}`, null, {
      timeout: 60_000,
    })
  },

  async get(analysisId: string): Promise<Analysis> {
    if (USE_MOCKS) return mockApi.getAnalysis(analysisId)
    return apiClient.get<Analysis>(`/analyses/${analysisId}`)
  },

  /** List the current user's analyses for the History page. */
  async list(): Promise<Analysis[]> {
    if (USE_MOCKS) return mockApi.listAnalyses()
    return apiClient.get<Analysis[]>(LIST_ENDPOINT)
  },
}
