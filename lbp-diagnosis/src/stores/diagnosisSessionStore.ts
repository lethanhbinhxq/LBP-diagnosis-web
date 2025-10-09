import { defineStore } from 'pinia'
import { fetchDiagnosisSessions } from '../api/diagnosis_api'
import { useToastStore } from './toastStore'

export const useDiagnosisSessionStore = defineStore('diagnosisSession', {
  state: () => ({
    sessions: [] as any[],
    loading: false,
    error: null as string | null
  }),

  getters: {
    hasSessions: (state) => state.sessions.length > 0,
    sessionCount: (state) => state.sessions.length
  },

  actions: {
    async fetchSessions() {
      this.loading = true
      this.error = null
      const toast = useToastStore()
      try {
        const res = await fetchDiagnosisSessions()
        this.sessions = Array.isArray(res) ? res : (res.sessions ?? [])
      } catch (err: any) {
        this.error = err.message || 'Failed to load sessions'
        toast.error(this.error ?? 'Failed to load diagnosis sessions')
        this.sessions = []
      } finally {
        this.loading = false
      }
    }
  }
})