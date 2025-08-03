// diagnosisStore.ts
import { defineStore } from 'pinia'

export const useDiagnosisStore = defineStore('diagnosis', {
  state: () => ({
    imageFile: null as File | null,
    textFile: null as File | null,
    result: null as { [key: string]: number } | null,
    loading: false
  }),
  actions: {
    setFiles(image: File, text: File) {
      this.imageFile = image
      this.textFile = text
    },
    setResult(result: { [key: string]: number }) {
      this.result = result
    },
    setLoading(state: boolean) {
      this.loading = state
    },
    clear() {
      this.imageFile = null
      this.textFile = null
      this.result = null
      this.loading = false
    },
  }
})
