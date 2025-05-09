import axios from 'axios'

async function submitForDiagnosis(imageFile: File | null, textContent: string) {
    const formData = new FormData()

    if (imageFile) {
        formData.append('image', imageFile)
    } else {
        alert('No image selected!')
        return
    }

    formData.append('text', textContent)

    try {
        const response = await axios.post('http://localhost:8000/predict', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })
        return response.data.diagnosis
    } catch (err) {
        console.error(err)
        alert('Failed to diagnose')
    }
}

export default submitForDiagnosis