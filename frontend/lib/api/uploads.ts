/**
 * Uploads service — POST /uploads (multipart/form-data).
 */

import { apiClient } from './client'
import { USE_MOCKS } from './config'
import { mockApi } from './mock'
import type { Upload } from './types'

const ENDPOINT = '/uploads'

export const uploadsApi = {
  async create(file: File): Promise<Upload> {
    if (USE_MOCKS) return mockApi.createUpload(file)

    const form = new FormData()
    form.append('file', file)
    // NOTE: don't set Content-Type manually — the browser adds the multipart
    // boundary automatically when the body is FormData.
    return apiClient.post<Upload>(ENDPOINT, form)
  },
}
