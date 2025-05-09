// diagnosisStore.ts
import { defineStore } from 'pinia'

export const useDiagnosisStore = defineStore('diagnosis', {
  state: () => ({
    imageFile: null as File | null,
    textFile: null as File | null,
    result: null as string | null,
    loading: false
  }),
  actions: {
    setFiles(image: File, text: File) {
      this.imageFile = image
      this.textFile = text
    },
    setResult(result: string) {
      this.result = result
    },
    setLoading(state: boolean) {
      this.loading = state
    }
  }
})
