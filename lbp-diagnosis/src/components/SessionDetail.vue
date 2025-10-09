<template>
  <div class="p-6 bg-white rounded shadow space-y-4">
    <!-- Back button -->
    <v-btn prepend-icon="mdi-arrow-left" class="!bg-secondary !text-pink-200 mt-4" @click="goBack">
      Back
    </v-btn>

    <h2 class="text-xl font-bold">Session {{ sessionId }} Details</h2>

    <!-- Loading / Error states -->
    <div v-if="diagnosisStore.loading" class="flex justify-center my-4">
      <v-progress-circular indeterminate size="70" width="7"></v-progress-circular>
    </div>

    <!-- Session summary -->
    <div v-else-if="diagnosisStore.sessionDetail" class="space-y-1">
      <p><strong>ID:</strong> {{ diagnosisStore.sessionDetail.id }}</p>
      <p><strong>Number of diagnoses:</strong> {{ diagnosisStore.sessionDetail.num_diagnoses }}</p>
      <p><strong>Created at:</strong> {{ formatDate(diagnosisStore.sessionDetail.created_at) }}</p>
    </div>

    <!-- Diagnoses table -->
    <div v-if="diagnosisStore.sessionDetail" class="mt-6">
      <h3 class="font-semibold mb-2">Diagnoses in this session:</h3>
      <table class="w-full border border-gray-300 text-sm">
        <thead class="bg-cyan-200">
          <tr>
            <th class="border px-2 py-1">Image</th>
            <th class="border px-2 py-1">Text Report</th>
            <th class="border px-2 py-1">Predicted Label</th>
            <th class="border px-2 py-1">Confidence</th>
            <th class="border px-2 py-1">Correct?</th>
            <th class="border px-2 py-1">Comment</th>
            <th class="border px-2 py-1">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(diag, i) in paginatedDiagnoses" :key="diag.id">
            <td class="border px-2 py-1 text-center">
              <img :src="getImageUrl(diag.image_path)" alt="MRI" class="h-24 object-cover mx-auto" />
            </td>
            <td class="border px-2 py-1 max-w-[250px] truncate" :title="diag.report_text">
              {{ truncateText(diag.report_text, 100) }}
            </td>
            <td class="border px-2 py-1 text-center font-semibold">
              {{ getPredictedLabel(diag.predicted_result) }}
            </td>
            <td class="border px-2 py-1 text-center">
              {{ (diag.confidence_score * 100).toFixed(1) }}%
            </td>
            <td class="border px-2 py-1 text-center">
              <span v-if="diag.is_correct" class="text-green-600 font-semibold">✔ Correct</span>
              <span v-else-if="diag.is_correct === false" class="text-red-600 font-semibold">✘ Incorrect</span>
              <span v-else>
              </span>
            </td>
            <td class="border px-2 py-1 max-w-[250px] truncate">{{ diag.comment }}</td>
            <td class="border px-2 py-1 text-center">
              <v-btn size="small" class="!bg-primary !text-white" @click="openFeedbackDialog(diag)">
                Feedback
              </v-btn>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Custom pagination -->
      <div class="flex justify-center mt-4">
        <v-pagination v-model="page"
          :length="Math.ceil((diagnosisStore.sessionDetail?.diagnoses.length || 0) / itemsPerPage)" :total-visible="7"
          show-first-last-page class="bg-white" />
      </div>
    </div>

    <v-dialog v-model="feedbackDialog" persistent max-width="500px">
      <v-card class="!bg-white">
        <v-card-title>Give Feedback</v-card-title>
        <v-card-text>
          <v-radio-group v-model="feedbackData.is_correct">
            <v-radio label="✔ Correct" :value="true"></v-radio>
            <v-radio label="✘ Incorrect" :value="false"></v-radio>
          </v-radio-group>
          <v-textarea v-model="feedbackData.comment" label="Comment" rows="3"></v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="feedbackDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="submitFeedback">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { computed, ref, onMounted } from 'vue'
import { useDiagnosisStore } from '../stores/diagnosisStore'
import { formatDate } from '../utils/format'

const route = useRoute()
const router = useRouter()
const diagnosisStore = useDiagnosisStore()

const sessionId = computed(() => Number(route.query.sessionId))

const page = ref(1)
const itemsPerPage = ref(5)
const feedbackDialog = ref(false)
const feedbackData = ref({ id: 0, is_correct: null as boolean | null, comment: '' })

const paginatedDiagnoses = computed(() => {
  const diagnoses = diagnosisStore.sessionDetail?.diagnoses || []
  const start = (page.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return diagnoses.slice(start, end)
})

function openFeedbackDialog(diag: any) {
  feedbackData.value = {
    id: diag.id,
    is_correct: diag.is_correct,
    comment: diag.comment || '',
  }
  feedbackDialog.value = true
}

function getPredictedLabel(result: string) {
  if (!result) return ''
  if (result.toLowerCase() === 'no finding') return 'No Finding'

  // Random LBP-related reasons
  const reasons = [
    'Herniation & Bulging',
    'Degeneration & Narrowing',
    'Bony Abnormalities',
  ]

  // Randomly pick one reason for LBP
  const randomReason = reasons[Math.floor(Math.random() * reasons.length)]
  return randomReason
}

async function submitFeedback() {
  await diagnosisStore.giveFeedback(feedbackData.value.id, feedbackData.value.is_correct, feedbackData.value.comment)
  feedbackDialog.value = false
}

onMounted(() => {
  if (sessionId.value) {
    diagnosisStore.loadSessionDetail(sessionId.value)
  }
})

function goBack() {
  router.push({ name: 'Diagnosis' })
}

function truncateText(text: string, length: number) {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

function getImageUrl(path: string | null) {
  return path ? `http://localhost:8000/uploads/${path}` : ''
}
</script>