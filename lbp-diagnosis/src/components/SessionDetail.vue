<template>
  <div class="p-6 bg-white rounded shadow space-y-4">
    <!-- Back button -->
    <v-btn prepend-icon="mdi-arrow-left" class="!bg-secondary !text-pink-200 mt-4" @click="goBack">
      Back
    </v-btn>

    <h2 class="text-xl font-bold">Session {{ sessionId }} Details</h2>

    <!-- Session summary -->
    <div v-if="session" class="space-y-1">
      <p><strong>ID:</strong> {{ session.id }}</p>
      <p><strong>Number of diagnoses:</strong> {{ session.num_diagnoses }}</p>
      <p><strong>Created at:</strong> {{ session.created_at }}</p>
    </div>

    <!-- Diagnoses table -->
    <div class="mt-6">
      <h3 class="font-semibold mb-2">Diagnoses in this session:</h3>
      <table class="w-full border border-gray-300 text-sm">
        <thead class="bg-cyan-200">
          <tr>
            <th class="border px-2 py-1">Image</th>
            <th class="border px-2 py-1">Text Report</th>
            <th class="border px-2 py-1">Result</th>
            <th class="border px-2 py-1">Correct?</th>
            <th class="border px-2 py-1">Feedback</th>
            <th class="border px-2 py-1">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(diag, i) in diagnoses" :key="i">
            <td class="border px-2 py-1 text-center">
              <img :src="diag.image" alt="MRI" class="h-24 object-cover mx-auto" />
            </td>
            <td class="border px-2 py-1" :title="diag.report">
              {{ truncateText(diag.report, 100) }}
            </td>
            <td class="border px-2 py-1">
              <div>LBP: {{ diag.result.lbp }}%</div>
              <div>No Finding: {{ diag.result.noFinding }}%</div>
            </td>
            <td class="border px-2 py-1 text-center">
              <span v-if="diag.isCorrect" class="text-green-600 font-semibold">✔ Correct</span>
              <span v-else class="text-red-600 font-semibold">✘ Incorrect</span>
            </td>
            <td class="border px-2 py-1">{{ diag.feedback }}</td>
            <td class="border px-2 py-1 text-center">
              <v-btn size="small" class="!bg-primary !text-white" @click="updateFeedback(i)">
                Update
              </v-btn>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { computed, ref, onMounted } from 'vue'

const route = useRoute()
const router = useRouter()

const sessionId = computed(() => route.query.sessionId as string | undefined)

// session and diagnoses data
const session = ref<any>(null)
const diagnoses = ref<any[]>([])

onMounted(() => {
  if (sessionId.value) {
    // mock fetching from backend
    session.value = {
      id: sessionId.value,
      num_diagnoses: 3,
      created_at: '2025-09-18 10:15:00',
    }

    diagnoses.value = [
      {
        image: '../../public/case_1.png',
        report:
          'A T2-weighted MRI of a male patient with 8 vertebrae and 8 discs. Discs 8 show Pfirrmann grade 3. Discs 1-7 show Pfirrmann grade 4. Narrowing in discs 2, 4. Bulging in discs 2-7. Low endplate in discs 2-7. Up endplate in discs 2-7. Herniation in discs 2. Spondylolisthesis in discs 2. Modic type 2 in discs 2, 5-6. Modic type 1 in discs 4.',
        result: { lbp: 85, noFinding: 15 },
        isCorrect: true,
        feedback: '',
      },
      {
        image: '../../public/case_2.JPEG',
        report:
          'T2-weighted MRI of a female patient showing six vertebrae and six intervertebral discs. All discs are graded as Pfirrmann grade 1. There is no evidence of disc herniation, narrowing, or bulging. Endplates appear normal at every level, and no abnormalities are detected.',
        result: { lbp: 60, noFinding: 40 },
        isCorrect: false,
        feedback: 'False positive — report indicates normal MRI; model incorrectly predicted LBP.',
      },
      {
        image: '../../public/P13-3.JPEG',
        report:
          'A T2-weighted MRI of a female patient with 6 vertebrae and 6 discs. All discs show Pfirrmann grade 1. No disc herniation, disc narrowing or disc bulging is observed. Endplates are normal across all levels. No abnormalities are noted.',
        result: { lbp: 10, noFinding: 90 },
        isCorrect: true,
        feedback: 'Correctly identified no finding.',
      },
    ]
  }
})

function goBack() {
  router.push({ path: '/dashboard/diagnosis' })
}

function updateFeedback(index: number) {
  // TODO: open dialog or navigate to feedback update page
  alert(`Update feedback for diagnosis #${index + 1}`)
}

function truncateText(text: string, length: number) {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}
</script>
