// src/stores/statisticsStore.ts
import { defineStore } from 'pinia'
import { useToastStore } from './toastStore'
import { getStatistics } from '../api/statistic_api'

export const useStatisticsStore = defineStore('statistics', {
  state: () => ({
    modelMetrics: {} as Record<string, number>,
    history: {} as any,
    loading: false,
  }),

  getters: {
    feedbackStatus: (state) => [
      state.history.feedbackGiven ?? 0,
      (state.history.totalDiagnoses ?? 0) - (state.history.feedbackGiven ?? 0),
    ],

    correctWrong: (state) => [
      state.history.correctDiagnoses ?? 0,
      state.history.wrongDiagnoses ?? 0,
    ],

    noFeedbackLbpDiagnoses: (state) =>
      (state.history.lbpDiagnoses ?? 0) -
      ((state.history.correctLbpDiagnoses ?? 0) + (state.history.wrongLbpDiagnoses ?? 0)),

    noFeedbackNoFindingDiagnoses: (state) =>
      (state.history.noFindingDiagnoses ?? 0) -
      ((state.history.correctNoFindingDiagnoses ?? 0) + (state.history.wrongNoFindingDiagnoses ?? 0)),
  },

  actions: {
    async fetchStatistics() {
      const toast = useToastStore()
      this.loading = true
      try {
        const data = await getStatistics()
        this.modelMetrics = data.modelMetrics ?? {}
        this.history = data.history ?? {}
      } catch (err: any) {
        toast.error(err.message ?? 'Failed to load statistics')
      } finally {
        this.loading = false
      }
    },
  },
})
