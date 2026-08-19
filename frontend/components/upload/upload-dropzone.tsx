'use client'

import { useRef, useState } from 'react'
import { CloudUpload } from 'lucide-react'
import { cn } from '@/lib/utils'
import { ACCEPTED_LABEL, validateImageFile } from '@/lib/upload-utils'

interface UploadDropzoneProps {
  onFileSelected: (file: File) => void
  onError: (message: string) => void
}

/**
 * A large, obvious upload target. Supports click-to-upload, keyboard
 * activation, and drag & drop. Validates the file before handing it up.
 */
export function UploadDropzone({ onFileSelected, onError }: UploadDropzoneProps) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [isDragging, setIsDragging] = useState(false)

  function handleFiles(files: FileList | null) {
    const file = files?.[0]
    if (!file) return
    const error = validateImageFile(file)
    if (error) {
      onError(error)
      return
    }
    onFileSelected(file)
  }

  return (
    <div>
      <input
        ref={inputRef}
        type="file"
        accept="image/png,image/jpeg,image/webp,image/heic,image/heif"
        className="sr-only"
        aria-hidden="true"
        tabIndex={-1}
        onChange={(e) => handleFiles(e.target.files)}
      />
      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault()
          setIsDragging(true)
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={(e) => {
          e.preventDefault()
          setIsDragging(false)
          handleFiles(e.dataTransfer.files)
        }}
        className={cn(
          'flex w-full flex-col items-center justify-center gap-4 rounded-2xl border-2 border-dashed p-8 text-center transition-colors sm:p-12',
          'focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-ring/50',
          isDragging
            ? 'border-primary bg-primary/5'
            : 'border-border bg-card hover:border-primary/50 hover:bg-muted/40',
        )}
      >
        <span
          className="flex size-16 items-center justify-center rounded-2xl bg-primary/10 text-primary"
          aria-hidden="true"
        >
          <CloudUpload className="size-8" />
        </span>
        <span className="text-xl font-semibold">
          Tap to upload a screenshot
        </span>
        <span className="text-pretty text-lg text-muted-foreground">
          Or drag and drop an image here.
        </span>
        <span className="text-base text-muted-foreground">
          Supported formats: {ACCEPTED_LABEL}
        </span>
      </button>
    </div>
  )
}
