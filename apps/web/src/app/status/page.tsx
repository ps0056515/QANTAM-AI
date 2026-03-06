'use client'

import { useEffect } from 'react'
import Link from 'next/link'

export default function StatusPage() {
  useEffect(() => {
    window.location.href = '/docs/SPRINTS.html'
  }, [])

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Sprint Status</h1>
        <p className="text-gray-600 mb-8">Redirecting to sprint tracker...</p>
        <Link href="/" className="text-blue-600 hover:underline">
          Back to Home
        </Link>
      </div>
    </main>
  )
}
