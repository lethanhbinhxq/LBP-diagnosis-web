// diagnosisStore.ts
import { defineStore } from 'pinia'
import { useToastStore } from './toastStore'

import { fetchDiagnosisSessionDetail } from '../api/diagnosis_api'
import { sendFeedback } from '../api/diagnosis_api'

export const useDiagnosisStore = defineStore('diagnosis', {
  state: () => ({
    sessions: [] as any[],
    sessionDetail: null as any | null,
    loading: false,
    error: null as string | null,
  }),

  actions: {
    async loadSessionDetail(sessionId: number) {
      this.loading = true
      this.error = null
      const toast = useToastStore()
      try {
        this.sessionDetail = await fetchDiagnosisSessionDetail(sessionId)
      } catch (e: any) {
        this.error = e.message
        toast.error(this.error ?? 'Failed to load diagnosis detail')
      } finally {
        this.loading = false
      }
    },

    async giveFeedback(diagnosisId: number, is_correct: boolean | null, comment: string) {
      const updated = await sendFeedback(diagnosisId, is_correct, comment)
      const idx = this.sessionDetail?.diagnoses.findIndex((d: any) => d.id === diagnosisId)
      if (idx !== -1 && this.sessionDetail) {
        this.sessionDetail.diagnoses[idx] = updated
      }
    },
  },
})
