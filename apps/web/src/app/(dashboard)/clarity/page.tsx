'use client'

import { useState } from 'react'

interface Flag {
  id: string
  flag_type: string
  flagged_text: string
  explanation: string
  suggested_rewrite: string
  confidence_score: number
  status: string
}

interface Requirement {
  id: string
  text: string
  rqs_score: number
  status: string
  flags: Flag[]
}

export default function ClarityPage() {
  const [requirements, setRequirements] = useState<Requirement[]>([])
  const [showModal, setShowModal] = useState(false)
  const [inputText, setInputText] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [selectedReq, setSelectedReq] = useState<Requirement | null>(null)

  const handleUpload = async () => {
    if (!inputText.trim()) return
    
    setIsAnalyzing(true)
    
    // Simulate AI analysis (in production, this calls the API)
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Parse requirements from input (split by double newline or numbered items)
    const reqTexts = inputText
      .split(/\n\n|\n(?=\d+\.)/)
      .map(t => t.trim())
      .filter(t => t.length > 10)
    
    const newReqs: Requirement[] = reqTexts.map((text, i) => {
      // Simulate ambiguity detection
      const flags: Flag[] = []
      
      const vagueWords = ['quickly', 'fast', 'appropriate', 'efficiently', 'user-friendly', 'easy', 'simple', 'good', 'better', 'properly']
      vagueWords.forEach(word => {
        if (text.toLowerCase().includes(word)) {
          flags.push({
            id: `flag-${Date.now()}-${Math.random()}`,
            flag_type: 'vague_language',
            flagged_text: word,
            explanation: `"${word}" is subjective and not measurable`,
            suggested_rewrite: `Replace "${word}" with specific metrics or criteria`,
            confidence_score: 85,
            status: 'pending'
          })
        }
      })
      
      if (text.includes('should') && !text.includes('must')) {
        flags.push({
          id: `flag-${Date.now()}-${Math.random()}`,
          flag_type: 'weak_requirement',
          flagged_text: 'should',
          explanation: '"Should" indicates optional behavior, use "must" for mandatory requirements',
          suggested_rewrite: 'Replace "should" with "must" or "shall"',
          confidence_score: 75,
          status: 'pending'
        })
      }
      
      const rqsScore = Math.max(0, 100 - (flags.length * 15))
      
      return {
        id: `req-${Date.now()}-${i}`,
        text: text.replace(/^\d+\.\s*/, ''),
        rqs_score: rqsScore,
        status: 'analysed',
        flags
      }
    })
    
    setRequirements(prev => [...prev, ...newReqs])
    setIsAnalyzing(false)
    setShowModal(false)
    setInputText('')
  }

  const handleApproveFlag = (reqId: string, flagId: string) => {
    setRequirements(prev => prev.map(req => {
      if (req.id === reqId) {
        return {
          ...req,
          flags: req.flags.map(f => 
            f.id === flagId ? { ...f, status: 'approved' } : f
          )
        }
      }
      return req
    }))
  }

  const handleDismissFlag = (reqId: string, flagId: string) => {
    setRequirements(prev => prev.map(req => {
      if (req.id === reqId) {
        return {
          ...req,
          flags: req.flags.map(f => 
            f.id === flagId ? { ...f, status: 'dismissed' } : f
          ),
          rqs_score: Math.min(100, req.rqs_score + 15)
        }
      }
      return req
    }))
  }

  const totalFlags = requirements.reduce((sum, r) => sum + r.flags.filter(f => f.status === 'pending').length, 0)
  const avgRqs = requirements.length > 0 
    ? Math.round(requirements.reduce((sum, r) => sum + r.rqs_score, 0) / requirements.length)
    : null

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl font-bold">CLARITY</h1>
          <p className="text-gray-600">Requirement Intelligence</p>
        </div>
        <button 
          onClick={() => setShowModal(true)}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          Upload Requirements
        </button>
      </div>

      <div className="grid grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-sm text-gray-500">Total Requirements</p>
          <p className="text-3xl font-bold">{requirements.length}</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-sm text-gray-500">Flags Detected</p>
          <p className="text-3xl font-bold text-amber-500">{totalFlags}</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow">
          <p className="text-sm text-gray-500">Average RQS</p>
          <p className={`text-3xl font-bold ${avgRqs && avgRqs >= 80 ? 'text-green-500' : avgRqs && avgRqs >= 60 ? 'text-amber-500' : avgRqs ? 'text-red-500' : ''}`}>
            {avgRqs !== null ? avgRqs : '--'}
          </p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow">
        <div className="p-6 border-b">
          <h2 className="font-semibold">Requirements</h2>
        </div>
        <div className="p-6">
          {requirements.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-gray-400 text-5xl mb-4">📋</div>
              <p className="text-gray-500 mb-4">No requirements uploaded yet.</p>
              <button 
                onClick={() => setShowModal(true)}
                className="text-blue-600 hover:underline"
              >
                Upload your first requirements
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {requirements.map((req) => (
                <div 
                  key={req.id} 
                  className={`border rounded-lg p-4 cursor-pointer transition ${selectedReq?.id === req.id ? 'border-blue-500 bg-blue-50' : 'hover:border-gray-300'}`}
                  onClick={() => setSelectedReq(selectedReq?.id === req.id ? null : req)}
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <p className="text-gray-800">{req.text}</p>
                      <div className="flex gap-2 mt-2">
                        {req.flags.filter(f => f.status === 'pending').length > 0 && (
                          <span className="text-xs px-2 py-1 bg-amber-100 text-amber-700 rounded">
                            {req.flags.filter(f => f.status === 'pending').length} flags
                          </span>
                        )}
                        <span className={`text-xs px-2 py-1 rounded ${
                          req.rqs_score >= 80 ? 'bg-green-100 text-green-700' :
                          req.rqs_score >= 60 ? 'bg-amber-100 text-amber-700' :
                          'bg-red-100 text-red-700'
                        }`}>
                          RQS: {req.rqs_score}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  {selectedReq?.id === req.id && req.flags.length > 0 && (
                    <div className="mt-4 pt-4 border-t space-y-3">
                      <h4 className="font-medium text-sm text-gray-700">Detected Issues:</h4>
                      {req.flags.map(flag => (
                        <div 
                          key={flag.id} 
                          className={`p-3 rounded-lg ${
                            flag.status === 'approved' ? 'bg-green-50 border border-green-200' :
                            flag.status === 'dismissed' ? 'bg-gray-50 border border-gray-200 opacity-50' :
                            'bg-amber-50 border border-amber-200'
                          }`}
                        >
                          <div className="flex justify-between items-start">
                            <div>
                              <span className="text-xs font-medium uppercase text-amber-600">
                                {flag.flag_type.replace('_', ' ')}
                              </span>
                              <p className="text-sm mt-1">
                                <span className="font-medium">"{flag.flagged_text}"</span> - {flag.explanation}
                              </p>
                              <p className="text-sm text-gray-600 mt-1">
                                <span className="font-medium">Suggestion:</span> {flag.suggested_rewrite}
                              </p>
                              <p className="text-xs text-gray-500 mt-1">
                                Confidence: {flag.confidence_score}%
                              </p>
                            </div>
                            {flag.status === 'pending' && (
                              <div className="flex gap-2 ml-4">
                                <button 
                                  onClick={(e) => { e.stopPropagation(); handleApproveFlag(req.id, flag.id); }}
                                  className="text-xs px-2 py-1 bg-green-600 text-white rounded hover:bg-green-700"
                                >
                                  Approve
                                </button>
                                <button 
                                  onClick={(e) => { e.stopPropagation(); handleDismissFlag(req.id, flag.id); }}
                                  className="text-xs px-2 py-1 bg-gray-400 text-white rounded hover:bg-gray-500"
                                >
                                  Dismiss
                                </button>
                              </div>
                            )}
                            {flag.status !== 'pending' && (
                              <span className={`text-xs px-2 py-1 rounded ${
                                flag.status === 'approved' ? 'bg-green-200 text-green-800' : 'bg-gray-200 text-gray-600'
                              }`}>
                                {flag.status}
                              </span>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Upload Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 w-full max-w-2xl max-h-[80vh] overflow-auto">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">Upload Requirements</h2>
              <button 
                onClick={() => setShowModal(false)}
                className="text-gray-500 hover:text-gray-700 text-2xl"
              >
                &times;
              </button>
            </div>
            
            <p className="text-gray-600 mb-4">
              Paste your requirements below. Each requirement should be separated by a blank line or numbered.
            </p>
            
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="1. The system should respond quickly to user requests.

2. Users must be able to upload files of appropriate size.

3. The admin can modify user permissions.

4. Data should be processed efficiently and stored securely."
              className="w-full h-64 p-4 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            
            <div className="flex justify-end gap-3 mt-4">
              <button 
                onClick={() => setShowModal(false)}
                className="px-4 py-2 border rounded-lg hover:bg-gray-50"
              >
                Cancel
              </button>
              <button 
                onClick={handleUpload}
                disabled={isAnalyzing || !inputText.trim()}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {isAnalyzing ? (
                  <>
                    <span className="animate-spin">⏳</span>
                    Analyzing...
                  </>
                ) : (
                  'Analyze Requirements'
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
