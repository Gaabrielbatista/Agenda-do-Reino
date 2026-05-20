<template>
  <div class="login-container">
    <form @submit.prevent="handleLogin">
      <h2>Login</h2>
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input type="email" class="form-control" id="email" v-model="email" required />
      </div>
      <div class="mb-3">
        <label for="senha" class="form-label">Senha</label>
        <input type="password" class="form-control" id="senha" v-model="senha" required />
      </div>
      <button type="submit" class="btn btn-primary w-100">Entrar</button>
      <p v-if="errorMessage" class="text-danger mt-2">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const email = ref('')
const senha = ref('')
const errorMessage = ref('')
const router = useRouter()
const authStore = useAuthStore()

async function handleLogin() {
  errorMessage.value = ''
  const success = await authStore.login(email.value, senha.value)
  if (success) {
    router.push('/')
  } else {
    errorMessage.value = 'Email ou senha inválidos'
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 100px auto;
  padding: 2rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
}
</style>