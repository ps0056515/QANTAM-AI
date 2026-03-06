import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'QANTAM - Quality Engineering AI',
  description: 'Intelligent requirement analysis, test generation, and release quality scoring',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">{children}</body>
    </html>
  )
}
