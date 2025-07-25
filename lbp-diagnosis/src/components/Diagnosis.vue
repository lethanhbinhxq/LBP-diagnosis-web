<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDiagnosisStore } from '../stores/diagnosisStore'
import submitForDiagnosis from '../api/diagnosis_api'
import DiagnosisChart from '../components/DiagnosisChart.vue'

const router = useRouter()
const diagnosisStore = useDiagnosisStore()

const textContent = ref<string>('')

const imageUrl = computed(() =>
  diagnosisStore.imageFile ? URL.createObjectURL(diagnosisStore.imageFile) : ''
)

function backToHome() {
  router.push({ name: 'Input' })
}

onMounted(async () => {
  if (!diagnosisStore.imageFile || !diagnosisStore.textFile) {
    alert('Missing files, please upload again.')
    router.push({ name: 'Input' })
    return
  }

  diagnosisStore.setLoading(true)

  textContent.value = await diagnosisStore.textFile.text()

  try {
    const result = await submitForDiagnosis(diagnosisStore.imageFile, textContent.value)
    diagnosisStore.setResult(result)
  } catch (err) {
    console.error(err)
    alert('Failed to get diagnosis.')
    router.push({ name: 'Input' })
  } finally {
    diagnosisStore.setLoading(false)
  }
})
</script>

<template>
  <div class="space-y-4">
    <h1 class="text-2xl font-bold text-center">Diagnosis Result</h1>

    <div v-if="diagnosisStore.loading" class="text-center text-lg">
      🔄 Loading diagnosis...
    </div>

    <div v-else>
      <div class="grid md:grid-cols-2 gap-4">
        <div v-if="diagnosisStore.imageFile">
          <div class="bg-surface border p-2 space-y-2 flex flex-col items-center">
            <h2 class="text-xl text-center">Uploaded Image</h2>
            <img :src="imageUrl" class="h-auto border" />
          </div>
        </div>

        <div v-if="textContent" class="bg-surface border p-2 space-y-2">
          <h2 class="text-xl text-center">Uploaded Text</h2>
          <pre class="bg-background border p-2 whitespace-pre-wrap text-justify w-full h-[200px] overflow-auto">
{{ textContent }}
          </pre>
        </div>
      </div>

      <div class="border p-4 mt-4 bg-surface">
        <h2 class="text-xl font-semibold">Diagnosis Result:</h2>
        <DiagnosisChart v-if="diagnosisStore.result" :diagnosis-result="diagnosisStore.result" />
      </div>


      <button class="btn mt-4" @click="backToHome">Back to Home</button>
    </div>
  </div>
</template>
