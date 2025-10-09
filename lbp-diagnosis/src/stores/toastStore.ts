import { defineStore } from 'pinia'

export const useToastStore = defineStore('toast', {
  state: () => ({
    show: true,
    message: '',
    type: 'success' as 'success' | 'error',
  }),
  actions: {
    success(msg: string) {
      this.message = msg
      this.type = 'success'
      this.show = true
    },
    error(msg: string) {
      this.message = msg
      this.type = 'error'
      this.show = true
    },
    close() {
      this.show = false
      this.message = ''
    },
  },
})
