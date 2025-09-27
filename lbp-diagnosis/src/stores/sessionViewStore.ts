import { defineStore } from 'pinia'

export const useSessionViewStore = defineStore('sessionView', {
  state: () => ({
    showNewDiagnosis: false,
  }),
  actions: {
    toggleNewDiagnosis() {
      this.showNewDiagnosis = !this.showNewDiagnosis
    },

    setNewDiagnosis(value: boolean) {
      this.showNewDiagnosis = value
    },

    getNewDiagnosis() {
      return this.showNewDiagnosis
    }
  },
})
