<!-- components/Input.vue -->

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useDiagnosisStore } from '../stores/diagnosisStore'

const fileInputImage = ref<HTMLInputElement | null>(null)
const fileNameImage = ref<string | null>(null)

const fileInputText = ref<HTMLInputElement | null>(null)
const fileNameText = ref<string | null>(null)

const router = useRouter()
const diagnosisStore = useDiagnosisStore()

function onFileUploadImage() {
  fileInputImage.value?.click()
}

function onFileSelectedImage(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    fileNameImage.value = target.files[0].name
  }
}

function onFileUploadText() {
  fileInputText.value?.click()
}

function onFileSelectedText(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    fileNameText.value = target.files[0].name
  }
}

function runDiagnosis() {
  const imageFile = fileInputImage.value?.files?.[0]
  const textFile = fileInputText.value?.files?.[0]

  if (imageFile && textFile) {
    diagnosisStore.setFiles(imageFile, textFile)
    router.push({ name: 'Diagnosis' })
  } else {
    alert('Please upload both files!')
  }
}
</script>

<template>
  <div class="max-w-xl mx-auto p-4 space-y-6">
    <h1 class="text-2xl font-bold">LBP Diagnosis</h1>

    <div class="grid grid-cols-2 gap-10">
      <!-- Image Upload -->
      <div class="flex flex-col items-center">
        <div class="w-64 bg-surface py-2">
          <h2 class="text-xl">Image</h2>
        </div>
        <div class="border-2 border-dashed h-64 w-64 flex flex-col items-center justify-center space-y-2">
          <button @click="onFileUploadImage" class="btn">Upload file</button>
          <input type="file" ref="fileInputImage" hidden @change="onFileSelectedImage" accept="image/*">
          <div v-if="fileNameImage" class="text-sm text-on-surface">{{ fileNameImage }}</div>
        </div>
      </div>

      <!-- Text Upload -->
      <div class="flex flex-col items-center">
        <div class="w-64 bg-surface py-2">
          <h2 class="text-xl">Text</h2>
        </div>
        <div class="border-2 border-dashed h-64 w-64 flex flex-col items-center justify-center space-y-2">
          <button @click="onFileUploadText" class="btn">Upload file</button>
          <input type="file" ref="fileInputText" hidden @change="onFileSelectedText" accept=".txt">
          <div v-if="fileNameText" class="text-sm text-on-surface">{{ fileNameText }}</div>
        </div>
      </div>
    </div>

    <button class="btn" @click="runDiagnosis">Run diagnosis</button>

  </div>
</template>