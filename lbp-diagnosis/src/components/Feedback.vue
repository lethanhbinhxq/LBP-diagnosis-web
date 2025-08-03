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

const name = ref('')
const email = ref('')
const message = ref('')
const valid = ref(false)
const showSnackbar = ref(false)
const formRef = ref()

const emailRule = (v: string) =>
  !v || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'Enter a valid email'

function submitFeedback() {
  // if (!formRef.value?.validate()) return

  // // Send to backend here
  // console.log('Submitted:', {
  //   name: name.value,
  //   email: email.value,
  //   message: message.value,
  // })

  // // Reset form
  // name.value = ''
  // email.value = ''
  // message.value = ''
  // showSnackbar.value = true
  // formRef.value.resetValidation()
}
</script>

<!-- <style>
.v-field--variant-filled .v-field__overlay {
  background: #cbffe3 !important;
}

.v-btn__overlay {
    background-color: #525252
}

.v-btn:hover > .v-btn__overlay {
  opacity: 0.5 !important;
}

.v-ripple__container {
  color: #ffffff;
  opacity: 0.5;
}

.v-messages__message {
  color: #ff2f00;
  font-weight: bold;
}
</style> -->