<template>
  <div class="login-container dark-theme">
    <div class="login-card">
      <h1 class="title">AgendaReino</h1>
      <h2 class="subtitle">Login</h2>

      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" required />
        </div>

        <div class="input-group">
          <label for="senha">Senha</label>
          <input type="password" id="senha" v-model="senha" required />
        </div>

        <button type="submit" :disabled="loading">Entrar com o sistema</button>
        <button type="button" @click="guestLogin" class="guest-btn">Entrar como visitante</button>
        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
        <div class="links">
          <a href="#" @click.prevent="forgotPassword">Esqueceu a senha?</a>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
console.log('LoginView carregado')

import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const email = ref('')
const senha = ref('')
const loading = ref(false)
const errorMsg = ref('')
const router = useRouter()
const authStore = useAuthStore()

async function handleLogin() {
  loading.value = true
  errorMsg.value = ''
  const success = await authStore.login(email.value, senha.value)
  if (success) {
    router.push('/')  // redireciona para a página principal (calendário)
  } else {
    errorMsg.value = 'Email ou senha inválidos'
  }
  loading.value = false
}

function forgotPassword() {
  alert('Funcionalidade em breve. Contate o administrador para redefinir sua senha.')
}

import api from '@/services/api'

async function guestLogin() {
  loading.value = true
  errorMsg.value = ''
  try {
    const response = await api.post('/auth/guest')
    const token = response.data.token
    const user = response.data.usuario
    authStore.token = token
    authStore.user = user
    localStorage.setItem('token', token)
    // Força o axios a usar o token
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
    router.push('/')
  } catch (err) {
    errorMsg.value = 'Erro ao acessar modo visitante.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  min-height: 100vh;
  width: 100vw;
  justify-content: center;
  align-items: center;
  background-color: var(--bg-page);
  transition: background-color 0.3s;
}

.login-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 400px;
  text-align: center;
  transition: background-color 0.3s, border-color 0.3s;
}

.title {
  font-size: 2rem;
  color: var(--btn-primary);
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.subtitle {
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
  font-weight: 500;
}

label {
  display: block;
  margin-bottom: 0.3rem;
  font-weight: 500;
  color: var(--text-primary);
}

input {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid var(--input-border);
  background-color: var(--input-bg);
  color: var(--text-primary);
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s;
}

input:focus {
  outline: none;
  border-color: var(--btn-primary);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

button {
  width: 100%;
  padding: 0.75rem;
  background: var(--btn-primary);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}

button:hover:not(:disabled) {
  background: var(--btn-primary-hover);
}

.links a {
  color: var(--btn-primary);
  text-decoration: none;
  font-size: 0.9rem;
}
</style>