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


      <v-data-table v-model:page="page" v-model:items-per-page="itemsPerPage" :headers="headers" :items="data"
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
                <v-btn prepend-icon="mdi-eye" class="!bg-primary" @click="viewSession(item.id)">View</v-btn>
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
        <v-pagination v-model="page" :length="Math.ceil(data.length / itemsPerPage)" :total-visible="7"
          show-first-last-page class="bg-white" />
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

const page = ref(1)
const itemsPerPage = ref(5)

const showNewDiagnosis = computed(() => sessionViewStore.showNewDiagnosis)

const router = useRouter()
const route = useRoute()
const sessionViewStore = useSessionViewStore()

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Number of diagnoses', key: 'num_diagnoses' },
  { title: 'Created at', key: 'created_at' },
  { title: 'Action', key: 'action', sortable: false }
]

const data = Array.from({ length: 30 }, (_, i) => ({
  id: i + 1,
  num_diagnoses: Math.floor(Math.random() * 10) + 1,
  created_at: `2025-09-${String(Math.floor(i / 4) + 1).padStart(2, '0')} ${String(
    8 + (i % 4) * 3
  ).padStart(2, '0')}:15:00`
}))

function onClickAddButton() {
  sessionViewStore.setNewDiagnosis(true)
}

function viewSession(sessionId: number) {
  router.push({ path: '/dashboard/diagnosis', query: { sessionId } })

  // (For now, just log or store in Pinia)
  console.log("Viewing session:", sessionId)
}

onMounted(() => {
  sessionViewStore.setNewDiagnosis(false)
})
</script>
