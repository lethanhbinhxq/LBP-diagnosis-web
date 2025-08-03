<template>
  <div class="space-y-10">
    <!-- Greeting -->
    <div class="text-4xl font-bold">Welcome back, {{ username }}! 🎉</div>

    <!-- Short Introduction -->
    <div class="text-lg text-gray-600">
      This is the <span class="font-semibold text-primary">LBP Diagnosis System</span> — an AI-powered tool to assist diagnosis based on MRI images and radiology reports.
      Quickly navigate below to get started!
    </div>

    <!-- Shortcut Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Diagnosis Shortcut -->
      <v-card
        class="hover:shadow-2xl transition cursor-pointer"
        elevation="4"
        color="#ffffff"
        dark
        @click="goTo('Diagnosis')"
      >
        <v-card-title class="text-2xl">
          <v-icon class="mr-3" size="36">mdi-radiology-box</v-icon>
          Diagnosis
        </v-card-title>
        <v-card-text>
          Upload MRI and report files to get AI-assisted diagnosis.
        </v-card-text>
      </v-card>

      <!-- Statistic Shortcut -->
      <v-card
        class="hover:shadow-2xl transition cursor-pointer"
        elevation="4"
        color="#ffffff"
        dark
        @click="goTo('Statistic')"
      >
        <v-card-title class="text-2xl">
          <v-icon class="mr-3" size="36">mdi-chart-bar</v-icon>
          Statistics
        </v-card-title>
        <v-card-text>
          View model performance, usage insights, and reports.
        </v-card-text>
      </v-card>

      <!-- Feedback Shortcut -->
      <v-card
        class="hover:shadow-2xl transition cursor-pointer"
        elevation="4"
        color="#ffffff"
        @click="goTo('Feedback')"
      >
        <v-card-title class="text-2xl">
          <v-icon class="mr-3" size="36">mdi-text-box-edit</v-icon>
          Feedback
        </v-card-title>
        <v-card-text>
          Share your feedback to help us improve the system.
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const router = useRouter()
const username = ref('Thanh Binh')

function goTo(page: string) {
  router.push({ name: page })
}
</script>
