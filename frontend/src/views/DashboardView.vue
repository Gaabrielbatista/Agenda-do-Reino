<template>
  <div class="min-h-screen bg-page p-4 md:p-8 flex flex-col gap-6">
    <div class="flex items-center justify-between">
      <h1 class="text-3xl font-bold tracking-tight text-text-main m-0">Dashboard</h1>
      <button 
        @click="logout"
        class="px-4 py-2 bg-red-500/10 hover:bg-red-500 border border-red-500/30 hover:border-red-500 text-red-500 hover:text-white font-medium rounded-lg transition-colors"
      >
        Sair
      </button>
    </div>

    <div class="bg-card p-6 rounded-2xl shadow-lg border border-border">
      <h2 class="text-xl font-semibold text-text-main mb-2">Bem-vindo, {{ authStore.user?.nome }}!</h2>
      <p class="text-text-secondary">Visão geral do sistema em breve.</p>
    </div>

    <div class="bg-card p-6 rounded-2xl shadow-lg border border-border">
      <h3 class="text-lg font-semibold text-text-main mb-4">Ações Rápidas</h3>
      <div class="flex gap-4">
        <button 
          @click="testAPI"
          class="px-5 py-2.5 bg-primary hover:bg-primary-hover text-white font-medium rounded-lg shadow-lg shadow-primary/20 transition-all"
        >
          Testar API (Ver Console)
        </button>
        <button 
          @click="goToCalendar"
          class="px-5 py-2.5 bg-transparent border border-border hover:bg-border/50 text-text-main font-medium rounded-lg transition-all"
        >
          Ir para Calendário
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const authStore = useAuthStore()
const router = useRouter()

function logout() {
  authStore.logout()
  router.push('/login')
}

function goToCalendar() {
  router.push('/')
}

async function testAPI() {
  try {
    const response = await api.get('/agenda?inicio=2026-05-01&fim=2026-05-31')
    console.log("Dados recebidos da API:", response.data)
    alert("API testada com sucesso! Verifique o console para os dados.")
  } catch (error) {
    console.error("Erro ao buscar dados da agenda:", error)
    alert("Erro ao testar a API.")
  }
}
</script>