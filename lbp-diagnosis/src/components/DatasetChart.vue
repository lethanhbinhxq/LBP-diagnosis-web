<template>
  <div class="max-w-[400px] mx-auto">
    <Pie :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup lang="ts">
import { Pie } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js'
import ChartDataLabels from 'chartjs-plugin-datalabels'
import { computed } from 'vue'

ChartJS.register(Title, Tooltip, Legend, ArcElement, ChartDataLabels)

const props = defineProps<{
  labels: string[]
  values: number[]
}>()

// Get CSS variables
const primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim()
const errorColor = getComputedStyle(document.documentElement).getPropertyValue('--color-error').trim()

// Map labels to colors
const getColorForLabel = (label: string) => {
  if (label.toLowerCase() === 'no finding') return primaryColor
  if (label.toLowerCase() === 'lbp') return errorColor
  return '#ccc' // default color for unknown labels
}

// Chart Data
const chartData = computed(() => ({
  labels: props.labels,
  datasets: [
    {
      data: props.values,
      backgroundColor: props.labels.map(label => getColorForLabel(label)),
      borderColor: '#fff',
      borderWidth: 2
    }
  ]
}))

// Chart Options
const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'right' as const,
      labels: {
        boxHeight: 40
      }
    },
    datalabels: {
      color: '#000',
      textStrokeColor: '#fff',
      textStrokeWidth: 5,
      font: {
        weight: 'bold' as const,
        size: 14
      },
      formatter: (value: number, context: any) => {
        const dataset = context.chart.data.datasets[0]
        const total = dataset.data.reduce((acc: number, val: number) => acc + val, 0)
        const percentage = ((value / total) * 100).toFixed(1)
        return `${percentage}%`
      }
    }
  }
}
</script>
