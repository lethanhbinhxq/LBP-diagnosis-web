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

ChartJS.register(Title, Tooltip, Legend, ArcElement, ChartDataLabels)

const props = defineProps<{
  diagnosisResult: { [key: string]: number }
}>()

const primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim()
const errorColor = getComputedStyle(document.documentElement).getPropertyValue('--color-error').trim()

const chartData = {
  labels: Object.keys(props.diagnosisResult),
  datasets: [
    {
      data: Object.values(props.diagnosisResult),
      backgroundColor: [primaryColor, errorColor],
      borderColor: '#fff',
      borderWidth: 2
    }
  ]
}

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
        const total = context.chart._metasets[0].total
        const percentage = ((value / total) * 100).toFixed(1)
        return `${percentage}%`
      }
    }
  }
}
</script>

<template>
  <div class="max-w-[400px] mx-auto">
    <Pie :data="chartData" :options="chartOptions" />
  </div>
</template>
