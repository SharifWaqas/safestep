'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

import { UploadDropzone } from '@/components/upload/upload-dropzone'
import { ImagePreview } from '@/components/upload/image-preview'
import { uploadsApi } from '@/lib/api/uploads'
import { analysesApi } from '@/lib/api/analyses'

export default function AnalyzePage() {
  const router = useRouter()

  const [file, setFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState('')
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  /*
   * Create a temporary browser URL for the selected image.
   * Clean it up when the file changes or the component unmounts.
   */
  useEffect(() => {
    if (!file) {
      setPreviewUrl('')
      return
    }

    const url = URL.createObjectURL(file)
    setPreviewUrl(url)

    return () => {
      URL.revokeObjectURL(url)
    }
  }, [file])

  function handleFileSelected(selectedFile: File) {
    setError(null)
    setFile(selectedFile)
  }

  function handleUploadError(message: string) {
    setError(message)
  }

  function handleRemove() {
    if (isUploading) return

    setFile(null)
    setError(null)
  }

  function handleReplace() {
    if (isUploading) return

    setFile(null)
    setError(null)
  }

  async function handleAnalyze() {
    if (!file || isUploading) return

    setIsUploading(true)
    setError(null)

    try {
      /*
       * Step 1:
       * Upload the screenshot to FastAPI.
       *
       * POST /uploads
       */
      const upload = await uploadsApi.create(file)

      /*
       * Step 2:
       * Start the analysis using the upload ID.
       *
       * POST /analyses/{upload_id}
       */
      const analysis = await analysesApi.create(upload.upload_id)

      /*
       * Step 3:
       * Navigate to the analysis result page.
       *
       * We will build this page next.
       */
      router.push(`/analysis/${analysis.analysis_id}`)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Something went wrong. Please try again.',
      )
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <main className="mx-auto w-full max-w-4xl px-4 py-10 sm:px-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">
          Analyze a message
        </h1>

        <p className="mt-2 text-muted-foreground">
          Upload a screenshot of a suspicious message and SafeStep will
          explain what you should look out for.
        </p>
      </div>

      <div className="rounded-2xl border bg-card p-6">
        {!file ? (
          <UploadDropzone
            onFileSelected={handleFileSelected}
            onError={handleUploadError}
          />
        ) : (
          <div className="space-y-6">
            <ImagePreview
              file={file}
              previewUrl={previewUrl}
              onRemove={handleRemove}
              onReplace={handleReplace}
            />

            <button
              type="button"
              onClick={handleAnalyze}
              disabled={isUploading}
              className="w-full rounded-lg bg-primary px-5 py-3 font-medium text-primary-foreground transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {isUploading ? 'Analyzing...' : 'Analyze message'}
            </button>
          </div>
        )}

        {error && (
          <div
            role="alert"
            className="mt-6 rounded-lg border border-destructive/30 bg-destructive/10 p-4 text-sm text-destructive"
          >
            {error}
          </div>
        )}
      </div>
    </main>
  )
}