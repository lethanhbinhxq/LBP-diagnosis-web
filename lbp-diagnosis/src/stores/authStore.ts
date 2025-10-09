import { defineStore } from 'pinia'
import { login as loginApi, signup as signupApi } from '../api/auth_api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    email: '',
    password: '',
    confirmPassword: '',
    loading: false,
    error: '',
    fullname: localStorage.getItem('fullname') || '',
    token: localStorage.getItem('token') || '' 
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    setEmail(email: string) {
      this.email = email
    },
    setPassword(password: string) {
      this.password = password
    },
    setConfirmPassword(confirmPassword: string) {
      this.confirmPassword = confirmPassword
    },
    setLoading(state: boolean) {
      this.loading = state
    },
    setError(message: string) {
      this.error = message
    },

    setAuth(token: string, fullname: string) {
      this.token = token
      this.fullname = fullname
      localStorage.setItem('token', token)
      localStorage.setItem('fullname', fullname)
    },

    clearAuth() {
      this.token = ''
      this.fullname = ''
      localStorage.removeItem('token')
      localStorage.removeItem('fullname')
    },

    clear() {
      this.email = ''
      this.password = ''
      this.confirmPassword = ''
      this.loading = false
      this.error = ''
      this.clearAuth()
    },

    async login(email: string, password: string) {
      this.loading = true
      this.error = ''
      try {
        const res = await loginApi(email, password)
        this.setAuth(res.access_token, res.fullname) 
        return res
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Login failed'
        throw err
      } finally {
        this.loading = false
      }
    },

    async signup(fullname: string, email: string, password: string) {
      this.loading = true
      this.error = ''
      try {
        const res = await signupApi(fullname, email, password)
        this.setAuth(res.access_token, fullname)
        return res
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Signup failed'
        throw err
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.clear()
    }
  }
})
