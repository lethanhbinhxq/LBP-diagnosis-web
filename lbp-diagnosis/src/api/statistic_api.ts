import axios from 'axios'

export async function getDiagnosisHistory() {
  try {
    const response = await axios.get('http://localhost:8000/statistic/diagnosis_history')
    return response.data
  } catch (err) {
    console.error(err)
    throw err
  }
}