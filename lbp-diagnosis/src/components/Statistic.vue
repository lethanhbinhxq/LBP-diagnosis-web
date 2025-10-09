<template>
  <div class="space-y-8">
    <h1 class="text-2xl font-bold text-center">Model & Diagnosis Statistics</h1>

    <!-- Loading -->
    <div v-if="statisticsStore.loading" class="flex justify-center items-center min-h-[40vh]">
      <v-progress-circular indeterminate size="70" width="7"></v-progress-circular>
    </div>

    <div v-else>
      <v-row dense>
        <v-col cols="6" md="3" v-for="(value, key) in statisticsStore.modelMetrics" :key="key">
          <v-card elevation="2" class="!p-2 text-center !border-2 !border-cyan-300 !rounded-2xl" color="#ffffff">
            <div class="text-lg font-semibold">{{ key }}</div>
            <div class="text-2xl font-bold text-primary">{{ (value * 100).toFixed(2) }}%</div>
          </v-card>
        </v-col>
      </v-row>

      <!-- Diagnosis History -->
      <v-card class="!p-4 !mt-6 !rounded-2xl !border-2 !border-yellow-400" elevation="2" color="#ffffff">
        <h2 class="text-2xl font-bold text-center mb-4">Diagnosis History</h2>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
          <div class="aspect-w-1 aspect-h-1">
            <BasePieChart
              v-if="statisticsStore.feedbackStatus[0] + statisticsStore.feedbackStatus[1] > 0"
              title="Feedback Status"
              :labels="['Feedback Given', 'No Feedback']"
              :values="statisticsStore.feedbackStatus"
            />
          </div>

          <div class="aspect-w-1 aspect-h-1">
            <BasePieChart
              v-if="statisticsStore.correctWrong[0] + statisticsStore.correctWrong[1] > 0"
              title="Correct vs Wrong Diagnoses"
              :labels="['Correct', 'Wrong']"
              :values="statisticsStore.correctWrong"
            />
          </div>

          <div class="min-h-[50dvh] flex items-center justify-center">
            <BaseStackedBarChart
              v-if="statisticsStore.history.totalDiagnoses > 0"
              title="Correct/Wrong/No Feedback per Diagnosis Type"
              :labels="['LBP', 'No Finding']"
              :correct-values="[statisticsStore.history.correctLbpDiagnoses, statisticsStore.history.correctNoFindingDiagnoses]"
              :wrong-values="[statisticsStore.history.wrongLbpDiagnoses, statisticsStore.history.wrongNoFindingDiagnoses]"
              :no-feedback-values="[statisticsStore.noFeedbackLbpDiagnoses, statisticsStore.noFeedbackNoFindingDiagnoses]"
            />
          </div>
        </div>
      </v-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useStatisticsStore } from '../stores/statisticStore'
import BasePieChart from './BasePieChart.vue'
import BaseStackedBarChart from './BaseStackedBarChart.vue'

const statisticsStore = useStatisticsStore()

onMounted(() => {
  statisticsStore.fetchStatistics()
})
</script>
