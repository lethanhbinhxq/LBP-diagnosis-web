import axios from 'axios'

export async function sendFeedbackForm(name: string, email: string, message: string) {
  const response = await axios.post('http://localhost:8000/feedback', {
    name,
    email,
    message
  })
  return response.data
}
