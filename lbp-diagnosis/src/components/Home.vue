<template>
  <div class="space-y-10 px-4 md:px-10">

    <h2 class="font-bold text-center my-2">Welcome to LBP-Diagnosis</h2>
    <!-- Brief Introduction -->
    <div class="text-lg text-gray-700 max-w-3xl mx-auto text-center">
      Explore the <span class="font-semibold text-primary">LBP Diagnosis System</span> — 
      an AI-powered tool for quick and accurate lumbar spine diagnosis using MRI scans and radiology reports. 
      Navigate below to access the system's core features.
    </div>

    <!-- Shortcut Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
      <!-- Diagnosis Card -->
      <v-card
        class="hover:scale-105 transition-transform cursor-pointer shadow-md hover:shadow-2xl rounded-xl"
        elevation="4"
        color="#ffffff"
        @click="goTo('Diagnosis')"
      >
        <v-card-title class="text-2xl items-center">
          <v-icon class="mr-3" size="36" color="#06D6A0">mdi-radiology-box</v-icon>
          Diagnosis
        </v-card-title>
        <v-card-text class="text-gray-600">
          Upload MRI scans and radiology reports to receive AI-assisted diagnosis instantly.
        </v-card-text>
      </v-card>

      <!-- Statistics Card -->
      <v-card
        class="hover:scale-105 transition-transform cursor-pointer shadow-md hover:shadow-2xl rounded-xl"
        elevation="4"
        color="#ffffff"
        @click="goTo('Statistic')"
      >
        <v-card-title class="text-2xl items-center">
          <v-icon class="mr-3" size="36" color="#EF476F">mdi-chart-bar</v-icon>
          Statistics
        </v-card-title>
        <v-card-text class="text-gray-600">
          View model performance, diagnosis history, and insights on system usage.
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goTo(page: string) {
  router.push({ name: page })
}
</script>

<style scoped>
/* Add smooth hover effects for cards */
.v-card {
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
</style>
