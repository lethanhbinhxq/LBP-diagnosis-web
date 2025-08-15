<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { signup, login } from '../api/auth_api'

const activeTab = ref(0)

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const errorMessage = ref('')
const loading = ref(false)

const router = useRouter()

async function handleLogin() {
    errorMessage.value = ''
    loading.value = true

    try {
        await login(username.value, password.value)
        router.push('/dashboard')  // Redirect on successful login
    } catch (err) {
        errorMessage.value = 'Invalid username or password'
    } finally {
        loading.value = false
    }
}

async function handleSignup() {
    if (password.value !== confirmPassword.value) {
        errorMessage.value = 'Passwords do not match!'
        return
    }

    errorMessage.value = ''
    loading.value = true

    try {
        await signup(username.value, password.value)
        router.push('/dashboard')  // Redirect on success
    } catch (err) {
        errorMessage.value = 'Signup failed. Username may already exist.'
    } finally {
        loading.value = false
    }
}

function signInWithGoogle() {
    console.log('Sign in with Google clicked')
    // Implement Google sign-in logic here
}

function togglePasswordVisibility() {
    showPassword.value = !showPassword.value
}

watch(activeTab, (_newVal) => {
    errorMessage.value = ''
})

</script>

<template>
    <div class="w-full min-h-screen bg-linear-45 from-primary to-surface flex items-center justify-center">
        <div class="flex flex-col items-center space-y-6 w-full max-w-lg">
            <!-- Heading -->
            <div>
                <h1 class="text-center font-bold text-on-surface">Welcome to</h1>
                <h1 class="text-teal-500 font-bold !text-5xl border-2 p-2">LBP Diagnosis</h1>
            </div>

            <div class="w-full h-px max-w-6xl mx-auto py-1"
                style="background-image: linear-gradient(90deg, rgba(255, 255, 255, 0) 1.46%, rgba(255, 255, 255, 0.8) 40.83%, rgba(255, 255, 255, 0.5) 65.57%, rgba(255, 255, 255, 0) 107.92%);">
            </div>



            <v-card class="!bg-white !p-10 !rounded-2xl w-full" elevation="6">
                <!-- Tabs -->
                <v-tabs v-model="activeTab" background-color="transparent" grow>
                    <v-tab color="#47b5ae">Login</v-tab>
                    <v-tab color="#47b5ae">Signup</v-tab>
                </v-tabs>

                <v-window v-model="activeTab" class="mt-4">
                    <!-- Login Tab -->
                    <v-window-item :value="0">
                        <form @submit.prevent="handleLogin" class="space-y-4">
                            <v-text-field v-model="username" label="Username" outlined dense required color="primary"
                                prepend-inner-icon="mdi-account"></v-text-field>

                            <v-text-field v-model="password" :type="showPassword ? 'text' : 'password'" label="Password"
                                outlined dense required color="primary" prepend-inner-icon="mdi-lock"
                                :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                                @click:append-inner="togglePasswordVisibility"></v-text-field>

                            <div v-if="errorMessage" class="text-red-500 text-sm text-center font-bold">
                                {{ errorMessage }}
                            </div>


                            <v-btn type="submit" color="#64ccc5" block class="py-2 !text-on-secondary" variant="flat">
                                Login
                            </v-btn>
                        </form>

                        <div class="my-4 text-center text-gray-500">or</div>

                        <v-btn @click="signInWithGoogle" block variant="outlined"
                            class="flex items-center justify-center gap-2 !text-teal-900">
                            <img src="https://www.svgrepo.com/show/475656/google-color.svg" alt="Google"
                                class="w-5 h-5" />
                            Sign in with Google
                        </v-btn>
                    </v-window-item>

                    <!-- Signup Tab -->
                    <v-window-item :value="1">
                        <form @submit.prevent="handleSignup" class="space-y-4">
                            <v-text-field v-model="username" label="Username" outlined dense required color="primary"
                                prepend-inner-icon="mdi-account"></v-text-field>

                            <v-text-field v-model="password" :type="showPassword ? 'text' : 'password'" label="Password"
                                outlined dense required color="primary" prepend-inner-icon="mdi-lock"
                                :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                                @click:append-inner="togglePasswordVisibility"></v-text-field>

                            <v-text-field v-model="confirmPassword" :type="showPassword ? 'text' : 'password'"
                                label="Confirm Password" outlined dense required color="primary"
                                prepend-inner-icon="mdi-lock-check"
                                :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                                @click:append-inner="togglePasswordVisibility"></v-text-field>

                            <!-- Error Message Display -->
                            <div v-if="errorMessage" class="text-red-500 text-sm text-center font-bold">
                                {{ errorMessage }}
                            </div>

                            <v-btn type="submit" :loading="loading" color="#64ccc5" block
                                class="py-2 !text-on-secondary" variant="flat">
                                Sign Up
                            </v-btn>
                        </form>
                    </v-window-item>

                </v-window>
            </v-card>
        </div>
    </div>
</template>
