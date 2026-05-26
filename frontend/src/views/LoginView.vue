<template>
  <div class="login-container">
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
  min-height: 100vh;
  background-color: var(--color-bg-page);
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-card {
  background: var(--bg-card);
  padding: 2.5rem; /* Mais espaçamento interno */
  border-radius: 16px; /* Bordas mais arredondadas */
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2); /* Sombra suave */
  border: 1px solid var(--border-color);
}

.title {
  color: var(--text-primary); /* Ou uma cor de destaque sutil */
  font-size: 1.8rem;
  margin-bottom: 0.25rem;
  font-weight: 700;
}

.subtitle {
  color: var(--text-secondary);
  margin-bottom: 2rem;
}

.input-group {
  margin-bottom: 1.25rem;
}

.input-group label {
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.4rem;
  display: block;
}

.input-group input {
  width: 100%;
  padding: 0.75rem;
  background-color: var(--input-bg);
  border: 1px solid var(--input-border);
  border-radius: 8px;
  color: var(--text-primary);
  transition: border-color 0.3s;
}

.input-group input:focus {
  border-color: var(--btn-primary);
  outline: none;
}

/* Botões com espaçamento visual */
button[type="submit"] {
  width: 100%;
  padding: 0.8rem;
  margin-top: 0.5rem;
  border: none;
  border-radius: 8px;
  background: var(--btn-primary);
  color: white;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s, transform 0.1s;
}

button[type="submit"]:hover {
  background: var(--btn-primary-hover);
}

button[type="submit"]:active {
  transform: scale(0.98);
}

.guest-btn {
  width: 100%;
  padding: 0.8rem;
  margin-top: 1rem;
  border: 1px solid var(--border-color); /* Estilo outline */
  border-radius: 8px;
  background: transparent;
  color: var(--text-secondary);
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
}

.guest-btn:hover {
  background: var(--hover-bg);
  color: var(--text-primary);
}
</style>