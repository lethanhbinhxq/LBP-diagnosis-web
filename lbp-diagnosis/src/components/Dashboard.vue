<template>
  <v-app>
    <v-app-bar app class="!bg-primary !text-on-secondary !pe-5">
      <v-app-bar-nav-icon class="ms-3" @click="rail = !rail" />
      <router-link to="/" class="flex items-center">
      </router-link>
      <v-toolbar-title>LBP Diagnosis</v-toolbar-title>

      <v-menu offset-y>
        <template #activator="{ props }">
          <v-btn icon v-bind="props">
            <v-icon size="x-large">mdi-account-circle</v-icon>
          </v-btn>
        </template>

        <v-list class="!bg-white" @click.stop>
          <v-list-item>
            <v-list-item-title class="font-semibold">Hello, {{ username }}</v-list-item-title>
          </v-list-item>

          <v-divider></v-divider>

          <v-list-item @click="logout">
            <template #prepend>
              <v-icon class="me-2 text-black">mdi-logout</v-icon>
            </template>
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

    </v-app-bar>

    <v-navigation-drawer app color="#011" :rail="rail" @click="rail = false">
      <v-list>
        <v-list-item v-for="(item, index) in menuItems" :key="index" :to="item.to" :exact="item.exact" color="#019">
          <template #prepend>
            <v-icon size="x-large" class="pe-2">{{ item.icon }}</v-icon>
          </template>

          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main class="bg-surface">
      <router-view class="p-5" />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const rail = ref(false)
const username = ref('Thanh Binh')
const menuItems = [
  { title: 'Dashboard', icon: 'mdi-view-dashboard', to: '/dashboard', exact: true },
  { title: 'Diagnosis', icon: 'mdi-radiology-box', to: '/dashboard/diagnosis' },
  { title: 'Statistic', icon: 'mdi-chart-bar', to: '/dashboard/statistic' },
  { title: 'Feedback', icon: 'mdi-text-box-edit', to: '/dashboard/feedback' },
]

function logout() {
  router.push('/')
}
</script>

<style>
.v-list-item__overlay {
  background-color: #c1fff9 !important;
  color: #EEEEEE !important;
}

.v-list-item:hover>.v-list-item__overlay {
  opacity: 0.5 !important;
}

.v-list-item .v-ripple__animation {
  background: rgba(1, 1, 1, 0.3) !important;
}

.v-list-item--active {
  color: #176b87 !important;
}
</style>