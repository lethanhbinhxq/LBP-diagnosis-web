import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    username: '',
    password: '',
    confirmPassword: '',
    loading: false,
    error: ''
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
      this.error = ''
    }
  }
})
