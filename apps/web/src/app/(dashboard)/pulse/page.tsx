'use client'

export default function PulsePage() {
  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl font-bold">PULSE</h1>
          <p className="text-gray-600">Test Suite Factory</p>
        </div>
        <button className="px-4 py-2 bg-blue-600 text-white rounded-lg">
          Generate Tests
        </button>
      </div>

      <div className="grid grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-sm text-gray-500">Generated</p>
          <p className="text-3xl font-bold">0</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-sm text-gray-500">Approved</p>
          <p className="text-3xl font-bold text-green-500">0</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-sm text-gray-500">Pending</p>
          <p className="text-3xl font-bold text-amber-500">0</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-sm text-gray-500">Approval Rate</p>
          <p className="text-3xl font-bold">--%</p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow p-6">
        <h2 className="font-semibold mb-4">Test Cases</h2>
        <p className="text-gray-500 text-center py-8">
          No test cases generated yet.
        </p>
      </div>
    </div>
  )
}
