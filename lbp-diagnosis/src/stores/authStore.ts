import { defineStore } from 'pinia'
import { login as loginApi } from '../api/auth_api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    username: '',
    password: '',
    confirmPassword: '',
    loading: false,
    error: '',
    fullname: ''
  }),
  actions: {
    setUsername(username: string) {
      this.username = username
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
    clear() {
      this.username = ''
      this.password = ''
      this.confirmPassword = ''
      this.loading = false
      this.error = '',
      this.fullname = ''
    },

    async login() {
      this.loading = true
      this.error = ''
      try {
        const res = await loginApi(this.username, this.password)

        this.fullname = res.fullname

        return true
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Login failed'
        return false
      } finally {
        this.loading = false
      }
    },
  }
})
