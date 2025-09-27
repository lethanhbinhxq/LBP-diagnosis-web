import axios from 'axios'

export async function createSession(userId: number) {
  const res = await axios.post('http://localhost:8000/diagnosis/session', { user_id: userId })
  return res.data
}

export async function submitDiagnosis(sessionId: number, imageFile: File, textContent: string) {
  const formData = new FormData()
  formData.append('session_id', sessionId.toString())
  formData.append('image', imageFile)
  formData.append('text', textContent)

  const res = await axios.post('http://localhost:8000/diagnosis/predict', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  return res.data
}

export async function sendFeedback(diagnosisId: number, isCorrect: boolean, comment?: string) {
  await axios.post('http://localhost:8000/diagnosis/feedback', {
    diagnosis_id: diagnosisId,
    is_correct: isCorrect,
    comment: comment || null
  })
}
