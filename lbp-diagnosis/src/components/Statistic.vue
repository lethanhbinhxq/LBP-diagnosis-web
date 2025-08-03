<template>
  <div class="space-y-8">
    <h1 class="text-2xl font-bold text-center">Model Statistics</h1>

    <!-- Performance Metrics -->
    <v-row dense>
      <v-col cols="6" md="3" v-for="(value, key) in metrics" :key="key">
        <v-card 
        elevation="2" 
        class="!p-2 text-center !border-2 !border-cyan-300 !rounded-2xl"
        color="#ffffff">
          <div class="text-lg font-semibold">{{ key }}</div>
          <div class="text-2xl font-bold text-primary">{{ value }}</div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Dataset Summary -->
    <v-card 
    class="!p-4 !mt-6 !rounded-2xl !border-2 !border-yellow-400" 
    elevation="2"
    color="#ffffff">
      <h2 class="text-xl font-semibold mb-4">Dataset Summary</h2>
      <v-row>
        <v-col cols="12" md="6">
          <v-list>
            <v-list-item>
              <v-list-item-title>Total MRIs</v-list-item-title>
              <v-list-item-subtitle>{{ dataset.total }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>LBP Cases</v-list-item-title>
              <v-list-item-subtitle>{{ dataset.lbp }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>No Finding Cases</v-list-item-title>
              <v-list-item-subtitle>{{ dataset.noFinding }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-col>

        <v-col cols="12" md="6">
          <DatasetChart :labels="['LBP', 'No Finding']" :values="[dataset.lbp, dataset.noFinding]" />
        </v-col>
      </v-row>
    </v-card>

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import DatasetChart from './DatasetChart.vue'

const metrics = ref({
  Accuracy: '95.00%',
  Precision: '94.50%',
  Recall: '98.08%',
  'F1 Score': '94.75%',
})

const dataset = ref({
  total: 1000,
  lbp: 600,
  noFinding: 400,
})
</script>
