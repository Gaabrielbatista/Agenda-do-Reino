<template>
  <div>
    <h1>Dashboard</h1>
    <p>Bem-vindo, {{ authStore.user?.nome }}!</p>
    
    <button @click="logout">Sair</button>
    <button @click="testAPI">Testar API</button>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import api from '@/services/api' // Centralizado aqui

const authStore = useAuthStore()
const router = useRouter()

function logout() {
  authStore.logout()
  router.push('/login')
}

async function testAPI() {
  try {
    const response = await api.get('/agenda?inicio=2026-05-01&fim=2026-05-31')
    console.log(response.data)
  } catch (error) {
    console.error("Erro ao buscar dados da agenda:", error)
  }
}
</script>