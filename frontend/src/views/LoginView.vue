<template>
  <div class="min-h-screen flex items-center justify-center bg-page p-4">
    <div class="w-full max-w-md bg-card p-8 rounded-2xl shadow-2xl border border-border">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-text-main mb-2 tracking-tight">AgendaReino</h1>
        <h2 class="text-text-secondary font-medium">Faça login para continuar</h2>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-5">
        <div class="space-y-1.5">
          <label for="email" class="block text-sm font-semibold text-text-main">Email</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            required 
            class="w-full bg-page border border-border text-text-main rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all placeholder:text-text-secondary/50"
            placeholder="seu@email.com"
          />
        </div>

        <div class="space-y-1.5">
          <div class="flex justify-between items-center">
            <label for="senha" class="block text-sm font-semibold text-text-main">Senha</label>
            <a href="#" @click.prevent="forgotPassword" class="text-xs font-medium text-primary hover:text-primary-hover transition-colors">
              Esqueceu a senha?
            </a>
          </div>
          <input 
            type="password" 
            id="senha" 
            v-model="senha" 
            required 
            class="w-full bg-page border border-border text-text-main rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all placeholder:text-text-secondary/50"
            placeholder="••••••••"
          />
        </div>

        <div class="pt-2">
          <button 
            type="submit" 
            :disabled="loading"
            class="w-full flex justify-center items-center gap-2 bg-primary hover:bg-primary-hover text-white font-bold py-3 px-4 rounded-xl transition-all disabled:opacity-70 disabled:cursor-not-allowed shadow-lg shadow-primary/20"
          >
            <svg v-if="loading" class="animate-spin h-5 w-5 text-white" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ loading ? 'Entrando...' : 'Entrar' }}
          </button>
        </div>

        <button 
          type="button" 
          @click="guestLogin" 
          class="w-full bg-transparent border border-border hover:bg-border/50 text-text-secondary hover:text-text-main font-semibold py-3 px-4 rounded-xl transition-all"
        >
          Entrar como visitante
        </button>

        <p v-if="errorMsg" class="text-red-400 text-sm font-medium text-center bg-red-400/10 p-3 rounded-xl border border-red-400/20 m-0 mt-4">{{ errorMsg }}</p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const { notifyError } = useToast()

const email = ref('')
const senha = ref('')
const loading = ref(false)
const errorMsg = ref('')
const redirectPath = computed(() => (typeof route.query.redirect === 'string' ? route.query.redirect : '/'))

async function handleLogin() {
  loading.value = true
  errorMsg.value = ''
  const success = await authStore.login(email.value, senha.value)
  if (success) {
    await router.push(redirectPath.value)
  } else {
    errorMsg.value = 'Email ou senha inválidos'
  }
  loading.value = false
}

function forgotPassword() {
  notifyError('Funcionalidade em breve. Contate o administrador para redefinir sua senha.')
}

async function guestLogin() {
  loading.value = true
  errorMsg.value = ''
  try {
    const response = await api.post('/auth/guest')
    const token = response.data.token
    const user = response.data.usuario
    authStore.setAuth(token, user)
    await router.push(redirectPath.value)
  } catch {
    errorMsg.value = 'Erro ao acessar modo visitante.'
  } finally {
    loading.value = false
  }
}
</script>