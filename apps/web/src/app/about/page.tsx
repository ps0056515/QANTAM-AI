'use client'

import { useEffect } from 'react'
import Link from 'next/link'

export default function AboutPage() {
  useEffect(() => {
    window.location.href = '/docs/ABOUT.html'
  }, [])

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">About QANTAM</h1>
        <p className="text-gray-600 mb-8">Redirecting to documentation...</p>
        <Link href="/" className="text-blue-600 hover:underline">
          Back to Home
        </Link>
      </div>
    </main>
  )
}
