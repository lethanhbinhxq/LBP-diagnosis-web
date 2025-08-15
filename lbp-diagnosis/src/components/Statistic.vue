<template>
  <div class="space-y-8">
    <h1 class="text-2xl font-bold text-center">Model Statistics</h1>

    <!-- Performance Metrics -->
    <v-row dense>
      <v-col cols="6" md="3" v-for="(value, key) in metrics" :key="key">
        <v-card elevation="2" class="!p-2 text-center !border-2 !border-cyan-300 !rounded-2xl" color="#ffffff">
          <div class="text-lg font-semibold">{{ key }}</div>
          <div class="text-2xl font-bold text-primary">{{ value }}</div>
        </v-card>
      </v-col>
    </v-row>

    <!-- diagnosis history -->
    <v-card class="!p-4 !mt-6 !rounded-2xl !border-2 !border-yellow-400" elevation="2" color="#ffffff">
      <div class="space-y-8">
        <h2 class="text-2xl font-bold text-center">Diagnosis History</h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="aspect-w-1 aspect-h-1">
            <BasePieChart title="Feedback Status" :labels="['Feedback Given', 'No Feedback']"
              :values="feedbackStatus" 
              />
          </div>

          <div class="aspect-w-1 aspect-h-1">
            <BasePieChart title="Correct vs Wrong Diagnoses" :labels="['Correct', 'Wrong']"
              :values="correctWrong" />
          </div>
        </div>


        <h2 class="text-2xl font-bold text-center">Correct/Wrong/No Feedback per Diagnosis Type</h2>
        <div class="w-3/4 min-h-[50dvh] flex items-center justify-center mx-auto">
          <BaseStackedBarChart :labels="['LBP', 'No Finding']"
            :correct-values="[history.correctLbpDiagnoses, history.correctNoFindingDiagnoses]"
            :wrong-values="[history.wrongLbpDiagnoses, history.wrongNoFindingDiagnoses]"
            :no-feedback-values="[noFeedbackLbpDiagnoses, noFeedbackNoFindingDiagnoses]" />
        </div>
      </div>
    </v-card>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import BasePieChart from './BasePieChart.vue'
import BaseStackedBarChart from './BaseStackedBarChart.vue'
import { getDiagnosisHistory } from '../api/statistic_api'

const metrics = ref({
  Accuracy: '95.00%',
  Precision: '94.50%',
  Recall: '98.08%',
  'F1 Score': '94.75%',
})

const history = ref({
  totalDiagnoses: 0,
  feedbackGiven: 0,
  noFeedback: 0,
  correctDiagnoses: 0,
  wrongDiagnoses: 0,
  lbpDiagnoses: 0,
  noFindingDiagnoses: 0,
  correctLbpDiagnoses: 0,
  wrongLbpDiagnoses: 0,
  correctNoFindingDiagnoses: 0,
  wrongNoFindingDiagnoses: 0,
})

const feedbackStatus = computed(() => {
  return [history.value.feedbackGiven, history.value.totalDiagnoses - history.value.feedbackGiven]
})

const correctWrong = computed(() => {
  return [history.value.correctDiagnoses, history.value.wrongDiagnoses]
})

const noFeedbackLbpDiagnoses = computed(() => {
  return history.value.lbpDiagnoses - (history.value.correctLbpDiagnoses + history.value.wrongLbpDiagnoses)
})

const noFeedbackNoFindingDiagnoses = computed(() => {
  return history.value.noFindingDiagnoses - (history.value.correctNoFindingDiagnoses + history.value.wrongNoFindingDiagnoses)
})

onMounted(async () => {
  const data = await getDiagnosisHistory()
  history.value = data
})
</script>
