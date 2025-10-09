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
import type { ChartOptions } from 'chart.js'
import { reactive, watch } from 'vue'

ChartJS.register(Title, Tooltip, Legend, ArcElement, ChartDataLabels)

const props = defineProps<{
  title?: string
  labels: string[]
  values: number[]
  colors?: string[]
}>()

const defaultColors = ['#4bc0c0', '#ff6384', '#ffcd56', '#36a2eb', '#9966ff']

const chartData = reactive({
  labels: props.labels,
  datasets: [
    {
      data: [...props.values],
      backgroundColor: props.colors?.length ? props.colors : defaultColors,
      borderColor: '#fff',
      borderWidth: 2
    }
  ]
})

// Watch for changes in props.values and update chartData
watch(() => props.values, (newValues) => {
  chartData.datasets[0].data = [...newValues]
}, { deep: true })

const chartOptions: ChartOptions<'pie'> = {
  responsive: true,
  plugins: {
    legend: {
      position: 'right',
      labels: {
        boxHeight: 40
      }
    },
    title: {
      display: true,
      text: props.title,
      font: { size: 18 }
    },
    datalabels: {
      color: '#000',
      textStrokeColor: '#fff',
      textStrokeWidth: 5,
      font: {
        weight: 'bold',
        size: 14
      },
      formatter: (value: number, context: any) => {
        const dataset = context.chart.data.datasets[0];
        const total = dataset.data.reduce((sum: number, val: number) => sum + val, 0);
        if (total === 0) return '';
        const percentage = ((value / total) * 100).toFixed(1);
        return value === 0 ? '' : `${percentage}%`;
      }
    }
  }
}
</script>

<template>
  <div class="max-w-[400px] mx-auto space-y-2">
    <Pie :data="chartData" :options="chartOptions" :key="chartData.datasets[0].data.join('-')" />
  </div>
</template>
