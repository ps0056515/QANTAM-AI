const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface FetchOptions extends RequestInit {
  token?: string
}

async function fetchAPI<T>(endpoint: string, options: FetchOptions = {}): Promise<T> {
  const { token, ...fetchOptions } = options

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...fetchOptions,
    headers,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }))
    throw new Error(error.detail || `HTTP ${response.status}`)
  }

  return response.json()
}

export const api = {
  clarity: {
    analyse: (data: { project_id: string; source: string; content?: string }) =>
      fetchAPI<{ task_id: string }>('/api/v1/clarity/analyse', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    getResults: (resultId: string) =>
      fetchAPI(`/api/v1/clarity/results/${resultId}`),
    approveFlag: (flagId: string) =>
      fetchAPI(`/api/v1/clarity/flags/${flagId}/approve`, { method: 'POST' }),
    dismissFlag: (flagId: string) =>
      fetchAPI(`/api/v1/clarity/flags/${flagId}/dismiss`, { method: 'POST' }),
  },

  pulse: {
    generate: (data: { requirement_ids: string[]; test_types?: string[] }) =>
      fetchAPI<{ task_id: string }>('/api/v1/pulse/generate', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    getResults: (resultId: string) =>
      fetchAPI(`/api/v1/pulse/results/${resultId}`),
    reviewTestCase: (testId: string, action: string, editedContent?: string) =>
      fetchAPI(`/api/v1/pulse/test-cases/${testId}/review`, {
        method: 'POST',
        body: JSON.stringify({ action, edited_content: editedContent }),
      }),
    export: (testIds: string[], format: string) =>
      fetchAPI('/api/v1/pulse/export', {
        method: 'POST',
        body: JSON.stringify({ test_ids: testIds, format }),
      }),
  },

  signal: {
    calculateRQS: (releaseId: string) =>
      fetchAPI('/api/v1/signal/rqs', {
        method: 'POST',
        body: JSON.stringify({ release_id: releaseId }),
      }),
    getDecision: (releaseId: string) =>
      fetchAPI(`/api/v1/signal/releases/${releaseId}/decision`),
    generateDocuments: (releaseId: string, docTypes: string[]) =>
      fetchAPI(`/api/v1/signal/releases/${releaseId}/documents`, {
        method: 'POST',
        body: JSON.stringify({ doc_types: docTypes }),
      }),
  },

  tasks: {
    getStatus: (taskId: string) =>
      fetchAPI<{ status: string; progress: number; result_id?: string }>(
        `/api/v1/tasks/${taskId}/status`
      ),
    cancel: (taskId: string) =>
      fetchAPI(`/api/v1/tasks/${taskId}/cancel`, { method: 'POST' }),
  },
}
