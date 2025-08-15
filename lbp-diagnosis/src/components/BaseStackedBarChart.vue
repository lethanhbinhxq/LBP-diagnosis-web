<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { computed } from 'vue'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps<{
  title?: string
  labels: string[]
  correctValues: number[]
  wrongValues: number[]
  noFeedbackValues: number[]
  colors?: string[]
}>()

const defaultColors = ['#06D6A0', '#EF476F', '#FFD166'] // Correct, Wrong, No Feedback

const chartData = computed(() => ({
  labels: props.labels,
  datasets: [
    {
      label: 'Correct',
      data: props.correctValues,
      backgroundColor: props.colors?.[0] ?? defaultColors[0]
    },
    {
      label: 'Wrong',
      data: props.wrongValues,
      backgroundColor: props.colors?.[1] ?? defaultColors[1]
    },
    {
      label: 'No Feedback',
      data: props.noFeedbackValues,
      backgroundColor: props.colors?.[2] ?? defaultColors[2]
    }
  ]
}))

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false, // Important!
  plugins: {
    legend: {
      position: 'top' as const,
      labels: {
        boxHeight: 20
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
      formatter: (value: number) => {
        return value === 0 ? '' : value;
      }
    },
    title: {
      display: true,
      text: props.title,
      font: { size: 18 }
    },
  },
  scales: {
    x: {
      stacked: true,
      ticks: { color: '#000' }
    },
    y: {
      stacked: true,
      beginAtZero: true,
      ticks: { precision: 0, color: '#000' }
    }
  }
}))
</script>

<template>
  <!-- Outer div controls height -->
  <Bar :data="chartData" :options="chartOptions" />
</template>
