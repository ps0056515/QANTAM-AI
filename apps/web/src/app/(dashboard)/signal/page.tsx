'use client'

export default function SignalPage() {
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold">SIGNAL</h1>
        <p className="text-gray-600">Release Quality Score</p>
      </div>

      <div className="grid grid-cols-2 gap-8">
        <div className="bg-white rounded-xl shadow p-8">
          <h2 className="text-lg font-semibold mb-6">Release Quality Score</h2>
          <div className="text-center">
            <div className="text-6xl font-bold text-gray-300 mb-4">--</div>
            <div className="text-xl text-gray-500">No release selected</div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow p-8">
          <h2 className="text-lg font-semibold mb-6">Score Breakdown</h2>
          <div className="space-y-4">
            <div className="flex justify-between">
              <span className="text-gray-600">Coverage (35%)</span>
              <span className="font-medium">--</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Defects (30%)</span>
              <span className="font-medium">--</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Tests (25%)</span>
              <span className="font-medium">--</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">CLARITY (10%)</span>
              <span className="font-medium">--</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
