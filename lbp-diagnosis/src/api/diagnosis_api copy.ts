// diagnosis_api.ts

import axios from 'axios'

export async function submitForDiagnosis(imageFile: File | null, textContent: string) {
    const formData = new FormData()

    if (imageFile) {
        formData.append('image', imageFile)
    } else {
        alert('No image selected!')
        return
    }

    formData.append('text', textContent)

    try {
        const response = await axios.post('http://localhost:8000/diagnosis/predict', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })
        return response.data.diagnosis
    } catch (err) {
        console.error(err)
        alert('Failed to diagnose')
    }
}

export async function sendFeedback(diagnosisId: number, isCorrect: boolean) {
    try {
        await axios.post('http://localhost:8000/diagnosis/feedback', {
            diagnosis_id: diagnosisId,
            is_correct: isCorrect
        })
    } catch (err) {
        console.error(err)
        alert('Failed to submit feedback')
    }
}