<template>
  <div class="profile-container dark-theme">
    <div class="profile-card">
      <div class="card-header">
        <button class="back-btn" @click="goBack" title="Voltar para a Agenda">
          <i class="fas fa-arrow-left"></i>
        </button>
        <h2>Meu Perfil</h2>
      </div>

      <div class="avatar-container">
        <i class="fas fa-user-circle avatar-icon"></i>
        <span class="user-badge" :class="userRoleClass">{{ userRoleLabel }}</span>
      </div>

      <form @submit.prevent="handleUpdate">
        <div class="form-group">
          <label for="nome">Nome</label>
          <div class="input-wrapper">
            <i class="fas fa-user input-icon"></i>
            <input
              id="nome"
              v-model="form.nome"
              type="text"
              required
              :disabled="!isAdmin || loading"
              placeholder="Seu nome completo"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="email">E-mail</label>
          <div class="input-wrapper">
            <i class="fas fa-envelope input-icon"></i>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              :disabled="!isAdmin || loading"
              placeholder="seu.email@exemplo.com"
            />
          </div>
        </div>

        <!-- Só mostra campos de edição se for admin -->
        <template v-if="isAdmin">
          <div class="form-group">
            <label for="senha">Nova Senha (deixe em branco para manter)</label>
            <div class="input-wrapper">
              <i class="fas fa-lock input-icon"></i>
              <input
                id="senha"
                v-model="form.senha"
                type="password"
                :disabled="loading"
                placeholder="Mínimo 6 caracteres"
              />
            </div>
          </div>

          <button type="submit" class="btn-save" :disabled="loading">
            <i class="fas fa-save"></i>
            {{ loading ? 'Salvando...' : 'Salvar Alterações' }}
          </button>
        </template>
        <template v-else>
          <div class="info-alert">
            <i class="fas fa-info-circle"></i>
            Apenas administradores podem atualizar os dados cadastrais.
          </div>
        </template>

        <p v-if="errorMsg" class="message error-msg">
          <i class="fas fa-exclamation-triangle"></i> {{ errorMsg }}
        </p>
        <p v-if="successMsg" class="message success-msg">
          <i class="fas fa-check-circle"></i> {{ successMsg }}
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const errorMsg = ref('')
const successMsg = ref('')

const form = ref({
  nome: '',
  email: '',
  senha: ''
})
// Keep original values to detect unchanged submissions
const original = ref({ nome: '', email: '' })

const isAdmin = computed(() => authStore.user?.tipo === 'admin')

const userRoleLabel = computed(() => {
  return authStore.user?.tipo === 'admin' ? 'Administrador' : 'Membro'
})

const userRoleClass = computed(() => {
  return authStore.user?.tipo === 'admin' ? 'badge-admin' : 'badge-membro'
})

const goBack = () => {
  router.push('/')
}

onMounted(() => {
  if (authStore.user) {
    form.value.nome = authStore.user.nome
    form.value.email = authStore.user.email
    // Guarda os valores originais
    original.value = { nome: authStore.user.nome, email: authStore.user.email }
  } else {
    router.push('/login')
  }
})

const handleUpdate = async () => {
  if (!authStore.user?.id) return
  loading.value = true
  // Prevent submission if nothing changed
  if (form.value.nome === original.value.nome &&
      form.value.email === original.value.email &&
      !form.value.senha.trim()) {
    errorMsg.value = 'Nenhum campo foi alterado.'
    loading.value = false
    return
  }
  errorMsg.value = ''
  successMsg.value = ''

  try {
    const payload: any = {
      nome: form.value.nome,
      email: form.value.email
    }
    
    if (form.value.senha.trim()) {
      if (form.value.senha.length < 6) {
        throw new Error('A nova senha deve conter pelo menos 6 caracteres.')
      }
      payload.senha = form.value.senha
    }

    const response = await api.put(`/usuarios/${authStore.user.id}`, payload)
    
    // Atualiza os dados no store
    authStore.user = {
      ...authStore.user,
      nome: response.data.nome,
      email: response.data.email
    }
    
    // Limpa a senha do form
    form.value.senha = ''
    successMsg.value = 'Perfil atualizado com sucesso!'
    // After updating profile, navigate back to calendar view
    router.push('/')
  } catch (err: any) {
    console.error(err)
    errorMsg.value = err.response?.data?.error || err.message || 'Erro ao atualizar perfil.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.profile-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem 1rem;
  background-color: #1e1e2f;
}

.profile-card {
  background: #2d2d3a;
  border: 1px solid #3a3a4a;
  border-radius: 16px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
  width: 100%;
  max-width: 500px;
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #3a3a4a;
  padding-bottom: 1rem;
}

.card-header h2 {
  margin: 0;
  font-size: 1.8rem;
  color: #ffffff;
  font-weight: 600;
}

.back-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #3a3a4a;
  color: #e0e0e0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  color: #ffffff;
  transform: translateX(-3px);
}

.avatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
  gap: 0.5rem;
}

.avatar-icon {
  font-size: 5rem;
  color: #3b82f6;
  filter: drop-shadow(0 4px 10px rgba(59, 130, 246, 0.3));
}

.user-badge {
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: uppercase;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  letter-spacing: 0.5px;
}

.badge-admin {
  background-color: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.badge-membro {
  background-color: rgba(16, 185, 129, 0.2);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.form-group {
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-size: 0.9rem;
  color: #bbbbcc;
  font-weight: 500;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  color: #666680;
  transition: color 0.2s ease;
}

input {
  width: 100%;
  padding: 0.8rem 1rem 0.8rem 2.8rem;
  border-radius: 8px;
  border: 1px solid #3a3a4a;
  background: #1e1e2f;
  color: #ffffff;
  font-size: 1rem;
  transition: all 0.2s ease;
}

input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

input:focus + .input-icon {
  color: #3b82f6;
}

input:disabled {
  background-color: #1a1a24;
  border-color: #2b2b3a;
  color: #777788;
  cursor: not-allowed;
}

.btn-save {
  width: 100%;
  padding: 0.9rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
  margin-top: 1rem;
}

.btn-save:hover:not(:disabled) {
  background: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.info-alert {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  background-color: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.2);
  color: #93c5fd;
  padding: 0.8rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  margin-top: 1rem;
}

.message {
  padding: 0.8rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  margin-top: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  animation: fadeIn 0.3s ease;
}

.error-msg {
  background-color: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
}

.success-msg {
  background-color: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: #6ee7b7;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
