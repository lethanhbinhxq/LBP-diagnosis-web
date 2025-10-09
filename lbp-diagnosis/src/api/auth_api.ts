import api from './axios_instance'
import { AxiosError } from 'axios'

export async function signup(fullname: string, email: string, password: string) {
  try {
    const response = await api.post('/auth/signup', { fullname, email, password })
    const data = response.data

    if (data.access_token) {
      localStorage.setItem('token', data.access_token)
    }

    return data
  } catch (err) {
    const axiosErr = err as AxiosError<{ detail?: string; message?: string }>
    const msg = axiosErr.response?.data?.detail || axiosErr.response?.data?.message || 'Signup failed'
    throw new Error(msg)
  }
}

export async function login(email: string, password: string) {
  try {
    const response = await api.post('/auth/login', { email, password })
    const data = response.data

    if (data.access_token) {
      localStorage.setItem('token', data.access_token)
    }

    return data
  } catch (err) {
    const axiosErr = err as AxiosError<{ detail?: string; message?: string }>
    const msg = axiosErr.response?.data?.detail || axiosErr.response?.data?.message || 'Login failed'
    throw new Error(msg) 
  }
}

export function logout() {
  localStorage.removeItem('token')
}