export const ACCEPTED_IMAGE_TYPES = [
  'image/png',
  'image/jpeg',
] as const

export const ACCEPTED_LABEL = 'PNG or JPG'
export const MAX_FILE_BYTES = 10 * 1024 * 1024 // 10 MB

export function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

/** Returns a user-friendly error message, or null when the file is acceptable. */
export function validateImageFile(file: File): string | null {
  const typeOk =
    (ACCEPTED_IMAGE_TYPES as readonly string[]).includes(file.type) ||
    /\.(png|jpe?g)$/i.test(file.name)

  if (!typeOk) {
    return `That file type is not supported. Please upload an image (${ACCEPTED_LABEL}).`
  }

  if (file.size > MAX_FILE_BYTES) {
    return 'That image is too large. Please choose one under 10 MB.'
  }

  return null
}