import axios from 'axios'

export async function signup(fullname:string, username: string, password: string) {
  try {
    const response = await axios.post('http://localhost:8000/auth/signup', {
      fullname,
      username,
      password
    })
    return response.data
  } catch (err) {
    console.error(err)
    throw err
  }
}

export async function login(username: string, password: string) {
  try {
    const response = await axios.post('http://localhost:8000/auth/login', {
      username,
      password
    })
    return response.data
  } catch (err) {
    console.error(err)
    throw err
  }
}
