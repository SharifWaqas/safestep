'use client'

import { ImageUp, X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { formatFileSize } from '@/lib/upload-utils'

interface ImagePreviewProps {
  file: File
  previewUrl: string
  onRemove: () => void
  onReplace: () => void
}

/** Shows the selected screenshot with its name, size, and remove/replace actions. */
export function ImagePreview({
  file,
  previewUrl,
  onRemove,
  onReplace,
}: ImagePreviewProps) {
  return (
    <div className="rounded-2xl border bg-card p-4 sm:p-5">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start">
        <div className="overflow-hidden rounded-xl border bg-muted">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={previewUrl || '/placeholder.svg'}
            alt="Preview of the screenshot you selected"
            className="mx-auto max-h-64 w-full object-contain sm:w-64"
          />
        </div>
        <div className="min-w-0 flex-1">
          <p className="text-sm font-medium uppercase tracking-wide text-muted-foreground">
            Selected image
          </p>
          <p className="mt-1 truncate text-lg font-semibold" title={file.name}>
            {file.name}
          </p>
          <p className="text-muted-foreground">{formatFileSize(file.size)}</p>

          <div className="mt-4 flex flex-wrap gap-3">
            <Button
              type="button"
              variant="outline"
              size="lg"
              onClick={onReplace}
              className="h-12 px-5 text-base"
            >
              <ImageUp data-icon="inline-start" />
              Choose a different image
            </Button>
            <Button
              type="button"
              variant="ghost"
              size="lg"
              onClick={onRemove}
              className="h-12 px-5 text-base"
            >
              <X data-icon="inline-start" />
              Remove
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
