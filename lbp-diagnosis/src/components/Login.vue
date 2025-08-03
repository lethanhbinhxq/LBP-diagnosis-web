<script setup lang="ts">
import { ref } from 'vue'
import router from '../router'

const email = ref('')
const password = ref('')

function handleLogin() {
    router.push('/dashboard')
}

function signInWithGoogle() {
    console.log('Sign in with Google clicked')
    // Implement Google sign-in (e.g., Firebase, OAuth2)
}
</script>


<template>
    <div class="w-full min-h-screen bg-primary flex items-center justify-center">
        <div class="bg-background rounded-2xl p-8">
            <h1 class="text-center">Welcome to LBP Diagnosis!</h1>

            <form @submit.prevent="handleLogin">
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-1" for="email">Email</label>
                    <input id="email" type="email" v-model="email" required
                        class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                        placeholder="Enter your email" />
                </div>

                <div class="mb-6">
                    <label class="block text-sm font-medium text-gray-700 mb-1" for="password">Password</label>
                    <input id="password" type="password" v-model="password" required
                        class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                        placeholder="Enter your password" />
                </div>

                <button type="submit"
                    class="w-full bg-primary text-white font-semibold py-2 px-4 rounded-md hover:bg-primary-dark transition">
                    Login
                </button>
            </form>

            <div class="my-4 text-center text-gray-500">or</div>

            <button @click="signInWithGoogle"
                class="w-full flex items-center justify-center gap-2 bg-white text-gray-700 border border-gray-300 py-2 px-4 rounded-md hover:bg-gray-100 transition">
                <img src="https://www.svgrepo.com/show/475656/google-color.svg" alt="Google" class="w-5 h-5" />
                Sign in with Google
            </button>

        </div>
    </div>
</template>