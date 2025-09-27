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

        <!-- All 3 charts in one row -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
          <div class="aspect-w-1 aspect-h-1">
            <BasePieChart
              title="Feedback Status"
              :labels="['Feedback Given', 'No Feedback']"
              :values="feedbackStatus"
            />
          </div>

          <div class="aspect-w-1 aspect-h-1">
            <BasePieChart
              title="Correct vs Wrong Diagnoses"
              :labels="['Correct', 'Wrong']"
              :values="correctWrong"
            />
          </div>

          <div class="min-h-[50dvh] flex items-center justify-center">
            <BaseStackedBarChart
              title="Correct/Wrong/No Feedback per Diagnosis Type"
              :labels="['LBP', 'No Finding']"
              :correct-values="[history.correctLbpDiagnoses, history.correctNoFindingDiagnoses]"
              :wrong-values="[history.wrongLbpDiagnoses, history.wrongNoFindingDiagnoses]"
              :no-feedback-values="[noFeedbackLbpDiagnoses, noFeedbackNoFindingDiagnoses]"
            />
          </div>
        </div>
      </div>
    </v-card>
  </div>
</template>


<script setup lang="ts">
import { ref, computed } from 'vue'
import BasePieChart from './BasePieChart.vue'
import BaseStackedBarChart from './BaseStackedBarChart.vue'

// Fake metrics
const metrics = ref({
  Accuracy: '95.00%',
  Precision: '94.50%',
  Recall: '98.08%',
  'F1 Score': '94.75%',
})

// Fake history data
const history = ref({
  totalDiagnoses: 50,
  feedbackGiven: 35,
  noFeedback: 15,
  correctDiagnoses: 40,
  wrongDiagnoses: 10,
  lbpDiagnoses: 30,
  noFindingDiagnoses: 20,
  correctLbpDiagnoses: 25,
  wrongLbpDiagnoses: 3,
  correctNoFindingDiagnoses: 15,
  wrongNoFindingDiagnoses: 7,
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
</script>
