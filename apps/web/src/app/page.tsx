import Link from 'next/link'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gradient-to-b from-slate-50 to-white">
      <div className="text-center max-w-3xl">
        <h1 className="text-6xl font-bold bg-gradient-to-r from-blue-800 to-blue-500 bg-clip-text text-transparent mb-4">
          QANTAM
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Quality Engineering AI Platform
        </p>
        <p className="text-gray-500 mb-10 max-w-xl mx-auto">
          AI-powered requirement analysis, test generation, release scoring, 
          code review intelligence, and production monitoring - all connected 
          through a Quality Knowledge Graph.
        </p>
        
        <div className="flex gap-4 justify-center mb-12">
          <Link
            href="/clarity"
            className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium shadow-lg shadow-blue-200 transition-all"
          >
            Get Started
          </Link>
          <Link
            href="/login"
            className="px-8 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-medium transition-all"
          >
            Sign In
          </Link>
        </div>

        <div className="flex gap-6 justify-center text-sm">
          <Link
            href="/about"
            className="text-blue-600 hover:text-blue-800 hover:underline flex items-center gap-1"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            About
          </Link>
          <Link
            href="/faq"
            className="text-blue-600 hover:text-blue-800 hover:underline flex items-center gap-1"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            FAQ
          </Link>
          <Link
            href="/status"
            className="text-blue-600 hover:text-blue-800 hover:underline flex items-center gap-1"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
            Sprint Status
          </Link>
        </div>

        <div className="mt-16 grid grid-cols-5 gap-4 text-center">
          <div className="p-4">
            <div className="text-2xl font-bold text-blue-600">CLARITY</div>
            <div className="text-xs text-gray-500 mt-1">Requirement Intel</div>
          </div>
          <div className="p-4">
            <div className="text-2xl font-bold text-blue-600">PULSE</div>
            <div className="text-xs text-gray-500 mt-1">Test Factory</div>
          </div>
          <div className="p-4">
            <div className="text-2xl font-bold text-blue-600">SIGNAL</div>
            <div className="text-xs text-gray-500 mt-1">Release Score</div>
          </div>
          <div className="p-4">
            <div className="text-2xl font-bold text-blue-600">FORGE</div>
            <div className="text-xs text-gray-500 mt-1">Code Review</div>
          </div>
          <div className="p-4">
            <div className="text-2xl font-bold text-blue-600">SENTINEL</div>
            <div className="text-xs text-gray-500 mt-1">Prod Monitor</div>
          </div>
        </div>
      </div>
    </main>
  )
}
