<template>
  <div class="space-y-8">
    <h1 class="text-2xl font-bold text-center">Diagnosis Sessions</h1>

    <div v-if="route.query.sessionId">
      <SessionDetail />
    </div>

    <div v-else-if="showNewDiagnosis">
      <NewDiagnosis />
    </div>

    <div v-else>
      <div class="flex justify-end mb-5">
        <v-btn @click="onClickAddButton" class="!bg-secondary !text-pink-200" prepend-icon="mdi-plus">
          Add Session
        </v-btn>
      </div>

      <div v-if="loading" class="flex items-center justify-center">
        <v-progress-circular indeterminate size="70" width="7"></v-progress-circular>
      </div>
      <div v-else-if="sessions.length === 0"
        class="flex flex-col items-center justify-center p-10 bg-gray-50 rounded-2xl shadow-sm">
        <v-icon size="80" class="text-gray-400 mb-4">mdi-radiology-box</v-icon>
        <p class="text-lg font-medium text-gray-600">No diagnosis sessions yet</p>
      </div>
      <div v-else>
        <v-data-table v-model:page="page" v-model:items-per-page="itemsPerPage" :headers="headers" :items="sessions"
          class="elevation-1 !bg-white" hide-default-footer>
          <!-- Custom header -->
          <template #headers="{ columns }">
            <tr>
              <th v-for="col in columns" :key="col.key ?? col.title"
                class="px-4 py-2 text-base !font-bold text-black bg-cyan-300">
                {{ col.title }}
              </th>
            </tr>
          </template>

          <!-- Custom rows -->
          <template #item="{ item, columns }">
            <tr class="border-b border-gray-300">
              <td v-for="col in columns" :key="col.key ?? col.title" class="px-4 py-2">
                <template v-if="col.key === 'action'">
                  <v-btn prepend-icon="mdi-eye" class="!bg-primary" @click="viewSession(item.id)">
                    View
                  </v-btn>
                </template>

                <template v-else-if="col.key === 'created_at'">
                  {{ formatDate(item.created_at) }}
                </template>

                <template v-else>
                  {{ item[col.key as keyof typeof item] }}
                </template>
              </td>
            </tr>
          </template>

        </v-data-table>

        <!-- Custom pagination -->
        <div class="flex justify-center mt-4">
          <v-pagination v-model="page" :length="Math.ceil(sessions.length / itemsPerPage)" :total-visible="7"
            show-first-last-page class="bg-white" />
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import NewDiagnosis from './NewDiagnosis.vue'
import SessionDetail from './SessionDetail.vue'
import { useSessionViewStore } from '../stores/sessionViewStore'
import { useDiagnosisSessionStore } from '../stores/diagnosisSessionStore'
import { formatDate } from '../utils/format'

const page = ref(1)
const itemsPerPage = ref(5)

const router = useRouter()
const route = useRoute()
const sessionViewStore = useSessionViewStore()
const diagnosisStore = useDiagnosisSessionStore()

const showNewDiagnosis = computed(() => sessionViewStore.showNewDiagnosis)

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Number of diagnoses', key: 'num_diagnoses' },
  { title: 'Created at', key: 'created_at' },
  { title: 'Action', key: 'action', sortable: false }
]

// Data comes from Pinia store
const sessions = computed(() => diagnosisStore.sessions)
const loading = computed(() => diagnosisStore.loading)

function onClickAddButton() {
  sessionViewStore.setNewDiagnosis(true)
}

function viewSession(sessionId: number) {
  router.push({ name: 'Diagnosis', query: { sessionId } })
}

onMounted(() => {
  sessionViewStore.setNewDiagnosis(false)
  diagnosisStore.fetchSessions()
})
</script>