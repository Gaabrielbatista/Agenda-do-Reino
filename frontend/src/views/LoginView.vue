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
</script>

<style scoped>
.login-container {
  min-height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0;
  padding: 0;
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
  text-align: center;
  border: none; /* remove qualquer borda */
}

.title {
  font-size: 2rem;
  color: #1e3c72;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.subtitle {
  color: #4a627a;
  margin-bottom: 1.5rem;
  font-weight: 500;
}

.input-group {
  text-align: left;
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.3rem;
  font-weight: 500;
  color: #1e3c72;
}

input {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  transition: border 0.2s;
  background: white;
}

input:focus {
  outline: none;
  border-color: #2a5298;
  box-shadow: 0 0 0 2px rgba(42, 82, 152, 0.2);
}

button {
  width: 100%;
  padding: 0.75rem;
  background: #2a5298;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
}

button:hover:not(:disabled) {
  background: #1e3c72;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  color: #e74c3c;
  margin-top: 0.8rem;
  font-size: 0.9rem;
}

.links {
  margin-top: 1rem;
}

.links a {
  color: #2a5298;
  text-decoration: none;
  font-size: 0.9rem;
}

.links a:hover {
  text-decoration: underline;
}

/* Adicione este bloco no final do seu <style scoped> */

/* Sobrescritas para o Tema Escuro */
.dark-theme {
  background-color: #1e1e2f; /* Fundo de toda a página de login */
}

.dark-theme .login-card {
  background: #2d2d3a;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5); /* Sombra mais intensa para contraste no escuro */
}

.dark-theme .title {
  color: #ffffff;
}

.dark-theme .subtitle,
.dark-theme label {
  color: #e0e0e0;
}

.dark-theme input {
  background-color: #1e1e2f;
  border: 1px solid #3a3a4a;
  color: #e0e0e0;
}

.dark-theme input:focus {
  border-color: #3b82f6; /* Azul de foco do seu tema escuro */
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

.dark-theme button {
  background-color: #3b82f6; /* Botão segue o padrão do botão primário do calendário */
}

.dark-theme button:hover:not(:disabled) {
  background-color: #2563eb;
}

.dark-theme .links a {
  color: #60a5fa; /* Tom de azul mais claro para links no modo escuro */
}
</style>