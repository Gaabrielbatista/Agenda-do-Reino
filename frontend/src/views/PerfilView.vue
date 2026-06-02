<template>
  <div class="profile-container">
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
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import { useToast } from '@/composables/useToast'

const router = useRouter()
const authStore = useAuthStore()
const { notifySuccess, notifyError } = useToast()

const loading = ref(false)
const errorMsg = ref('')

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
    notifySuccess('Perfil atualizado com sucesso!')
    // After updating profile, navigate back to calendar view
    router.push('/')
  } catch (err: any) {
    console.error(err)
    errorMsg.value = err.response?.data?.error || err.message || 'Erro ao atualizar perfil.'
    notifyError(errorMsg.value)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
}

.back-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  color: var(--text-primary);
  font-size: 1.2rem;
}

.back-btn i {
  pointer-events: none;
}

.profile-card {
  background: var(--bg-card);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.15);
  max-width: 500px;
  width: 100%;
  border: 1px solid var(--border-color);
}

.avatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
}

.avatar-icon {
  font-size: 5rem; /* Ícone maior */
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  color: var(--text-secondary);
}

.input-wrapper input {
  width: 100%;
  padding-left: 2.8rem;
  background-color: var(--input-bg);
  color: var(--text-primary);
  border: 1px solid var(--input-border);
  border-radius: 8px;
}

.input-wrapper input::placeholder {
  color: var(--text-secondary);
}
.btn-save {
  width: 100%;
  padding: 0.8rem;
  margin-top: 1rem;
  background: var(--btn-primary);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s ease;
}

.btn-save:hover {
  background: var(--btn-primary-hover);
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.info-alert {
  margin-top: 1rem;
  padding: 0.8rem;
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>
