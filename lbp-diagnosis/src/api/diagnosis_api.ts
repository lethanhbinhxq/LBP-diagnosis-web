import api from './axios_instance'

export async function fetchDiagnosisSessions() {
  const response = await api.get('/diagnosis/sessions')
  return response.data  // should be an array
}

// Run a new diagnosis session
export async function runDiagnosisSession(formData: FormData) {
  const res = await api.post('/diagnosis/run', formData, {
    headers: {
      'Content-Type': 'multipart/form-data', // ✅ override default JSON
    },
  })
  return res.data
}

export async function fetchDiagnosisSessionDetail(sessionId: number) {
  try {
    const res = await api.get(`/diagnosis/sessions/${sessionId}`)
    return res.data
  } catch (err: any) {
    throw new Error(err.response?.data?.detail || 'Failed to fetch session detail')
  }
}

export async function sendFeedback(diagnosisId: number, is_correct: boolean | null, comment: string) {
  try {
    const response = await api.put(`/diagnosis/${diagnosisId}/feedback`, {
      is_correct,
      comment,
    })
    return response.data
  } catch (err: any) {
    throw new Error(err.response?.data?.detail || 'Failed to give feedback')
  }
}