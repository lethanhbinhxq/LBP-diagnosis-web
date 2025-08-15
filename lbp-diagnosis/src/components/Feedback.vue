<template>
  <div class="max-w-2xl mx-auto p-4 space-y-6">
    <h1 class="text-2xl font-bold text-center">Feedback</h1>

    <v-card elevation="2" color="#ffffff">
      <v-form v-model="valid" ref="formRef" class="p-7">
        <v-text-field
          v-model="name"
          label="Your Name"
          prepend-icon="mdi-account"
          clearable
        />

        <v-text-field
          v-model="email"
          label="Email (optional)"
          prepend-icon="mdi-email"
          clearable
          :rules="[emailRule]"
        />

        <v-textarea
          v-model="message"
          label="* Your Feedback"
          prepend-icon="mdi-message"
          auto-grow
          :rules="[v => !!v || 'Feedback is required']"
          required
        />

        <v-btn class="mt-4" color="#64ccc5" @click="submitFeedback" :disabled="!valid" variant="flat">
          Submit
        </v-btn>
      </v-form>
    </v-card>

    <v-snackbar v-model="showSnackbar" timeout="4000" color="success">
      Feedback sent successfully!
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import {sendFeedbackForm} from "../api/feedback_api.ts"

const name = ref('')
const email = ref('')
const message = ref('')
const valid = ref(false)
const showSnackbar = ref(false)
const formRef = ref()

const emailRule = (v: string) =>
  !v || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'Enter a valid email'

async function submitFeedback() {
  if (!formRef.value?.validate()) return

  try {
    await sendFeedbackForm(name.value, email.value, message.value)

    // Reset form
    name.value = ''
    email.value = ''
    message.value = ''
    showSnackbar.value = true
    formRef.value.resetValidation()
    valid.value = true
  } catch (error) {
    console.error('Failed to send feedback:', error)
    throw error
  }
}
</script>