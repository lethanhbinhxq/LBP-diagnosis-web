<script setup lang="ts">
import { ref } from 'vue'
import { useDiagnosisStore } from '../stores/diagnosisStore'
import DiagnosisChart from './DiagnosisChart.vue'
import submitForDiagnosis from '../api/diagnosis_api'

const diagnosisStore = useDiagnosisStore()

const fileInputImage = ref<HTMLInputElement | null>(null)
const fileInputText = ref<HTMLInputElement | null>(null)

const fileNameImage = ref<string | null>(null)
const fileNameText = ref<string | null>(null)
const textContent = ref<string>('') // store text preview
const imageUrl = ref<string>('')     // image preview

const diagnosisResult = ref<Record<string, number> | null>(null)
const loading = ref(false)

function onFileUploadImage() {
  fileInputImage.value?.click()
}

function onFileUploadText() {
  fileInputText.value?.click()
}

function onFileSelectedImage(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files?.length) {
    const file = target.files[0]
    diagnosisStore.imageFile = file
    fileNameImage.value = file.name
    imageUrl.value = URL.createObjectURL(file)
  }
}

async function onFileSelectedText(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files?.length) {
    const file = target.files[0]
    diagnosisStore.textFile = file
    fileNameText.value = file.name
    textContent.value = await file.text()
  }
}

async function runDiagnosis() {
  const imageFile = diagnosisStore.imageFile
  const textFile = diagnosisStore.textFile

  if (!imageFile || !textFile) {
    alert('Please upload both files!')
    return
  }

  diagnosisStore.setFiles(imageFile, textFile)
  loading.value = true

  try {
    const result = await submitForDiagnosis(imageFile, textContent.value)
    diagnosisStore.setResult(result)
    diagnosisResult.value = result
  } catch (err) {
    console.error(err)
    alert('Diagnosis failed.')
  } finally {
    loading.value = false
  }
}

function resetPage() {
  diagnosisStore.clear()
  fileNameImage.value = null
  fileNameText.value = null
  imageUrl.value = ''
  textContent.value = ''
  diagnosisResult.value = null
  loading.value = false

  // Reset input elements so the same file can be uploaded again
  if (fileInputImage.value) fileInputImage.value.value = ''
  if (fileInputText.value) fileInputText.value.value = ''
}

</script>

<template>
  <div class="max-w-7xl mx-auto p-6 space-y-6">
    <h1 class="text-3xl font-bold text-center">LBP Diagnosis</h1>

    <!-- 3-column layout -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 items-stretch">
      <!-- 📁 Image Upload -->
      <div class="space-y-4 bg-white border-3 border-cyan-300 p-4 rounded-xl flex flex-col">
        <h2 class="text-xl font-semibold text-center">Image Upload</h2>

        <div
          class="border-2 border-gray-400 border-dashed rounded-2xl m-2 p-4 flex-1 flex flex-col max-h-[360px] overflow-auto">
          <input type="file" ref="fileInputImage" hidden @change="onFileSelectedImage" accept="image/*" />
          <div v-if="fileNameImage" class="text-sm font-medium">📁 {{ fileNameImage }}</div>
          <div class="flex-1 overflow-auto flex justify-center items-center w-full">
            <img v-if="imageUrl" :src="imageUrl" class="w-full h-auto border" />
          </div>
        </div>

        <div class="flex justify-center">
          <v-btn class="m-2" color="#64ccc5" @click="onFileUploadImage" variant="flat" :disabled="loading">
            Upload Image
          </v-btn>
        </div>
      </div>

      <!-- 📄 Text Upload -->
      <div class="space-y-4 bg-white border-3 border-cyan-300 p-4 rounded-xl flex flex-col">
        <h2 class="text-xl font-semibold text-center">Text Upload</h2>

        <div
          class="border-2 border-gray-400 border-dashed rounded-2xl m-2 p-4 flex-1 flex flex-col max-h-[360px] overflow-auto">
          <input type="file" ref="fileInputText" hidden @change="onFileSelectedText" accept=".txt" />
          <div v-if="fileNameText" class="text-sm font-medium">📁 {{ fileNameText }}</div>
          <div class="flex-1 overflow-auto flex justify-center items-center w-full">
            <pre v-if="textContent" class="bg-background border p-2 whitespace-pre-wrap text-sm max-h-60 overflow-auto">
{{ textContent }}
          </pre>
          </div>
        </div>

        <div class="flex justify-center">
          <v-btn class="m-2" color="#64ccc5" @click="onFileUploadText" variant="flat" :disabled="loading">
            Upload Text
          </v-btn>
        </div>
      </div>

      <!-- 🧠 Diagnosis Result -->
      <div class="space-y-4 bg-white border-3 border-cyan-300 p-4 rounded-xl flex flex-col">
        <h2 class="text-xl font-semibold text-center">Diagnosis Result</h2>

        <div class="flex-1 flex flex-col items-center justify-center max-h-[360px] overflow-auto">
          <div v-if="loading" class="text-center text-lg w-full">🔄 Running diagnosis...</div>

          <div v-else-if="diagnosisResult">
            <DiagnosisChart :diagnosis-result="diagnosisResult" />
          </div>

          <div v-else class="text-center text-gray-500 italic w-full">No result yet.</div>
        </div>

        <!-- Buttons -->
        <div class="m-2 flex">
          <v-btn class="m-2 flex-1" color="#64ccc5" @click="runDiagnosis" variant="flat" :disabled="loading">
            Run
          </v-btn>
          <v-btn class="m-2 flex-1" color="#f73213" @click="resetPage" variant="flat" :disabled="loading">
            Reset
          </v-btn>
        </div>
      </div>
    </div>
  </div>
</template>
