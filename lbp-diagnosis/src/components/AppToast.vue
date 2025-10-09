<template>
    <v-snackbar v-if="toast.message"
    v-model="toast.show" 
    location="top right" 
    timeout="3000" 
    content-class="rounded-lg shadow-lg m-6"
        :style="{ '--toast-bg': toast.type === 'error' ? 'var(--color-error)' : 'var(--color-success)' }">
        <div class="font-semibold text-sm">
            {{ toast.message }}
        </div>
    </v-snackbar>
</template>

<script setup lang="ts">
import { useToastStore } from '../stores/toastStore'
const toast = useToastStore()
</script>

<style>
.v-overlay__content.rounded-lg.shadow-lg.m-6.v-snackbar__wrapper.v-snackbar--variant-elevated {
    background-color: var(--toast-bg) !important;
    color: #ECFFE6 !important;
}
</style>
