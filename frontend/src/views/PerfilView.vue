<template>
  <div class="min-h-screen bg-page p-4 flex justify-center items-center">
    <div class="w-full max-w-lg bg-card rounded-2xl shadow-2xl border border-border overflow-hidden">
      <div class="px-6 py-5 border-b border-border flex items-center gap-4">
        <button 
          class="p-2 -ml-2 text-text-secondary hover:text-text-main hover:bg-border/50 rounded-lg transition-colors" 
          @click="goBack" 
          title="Voltar para a Agenda"
        >
          <ArrowLeftIcon class="w-6 h-6" aria-hidden="true" />
        </button>
        <h2 class="m-0 text-xl font-semibold tracking-wide text-text-main">Meu Perfil</h2>
      </div>

      <div class="p-8">
        <div class="flex flex-col items-center mb-8">
          <UserCircleIcon class="w-24 h-24 text-text-secondary mb-3" aria-hidden="true" />
          <span 
            :class="['px-3 py-1 rounded-full text-xs font-bold tracking-wider', authStore.user?.tipo === 'admin' ? 'bg-primary/20 text-primary' : 'bg-emerald-500/20 text-emerald-400']"
          >
            {{ userRoleLabel }}
          </span>
        </div>

        <form @submit.prevent="handleUpdate" class="space-y-5">
          <div class="space-y-1.5">
            <label for="nome" class="block text-sm font-medium text-text-main">Nome</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <UserIcon class="h-5 w-5 text-text-secondary" aria-hidden="true" />
              </div>
              <input
                id="nome"
                v-model="form.nome"
                type="text"
                required
                :disabled="!isAdmin || loading"
                placeholder="Seu nome completo"
                class="w-full bg-page border border-border text-text-main rounded-xl pl-11 pr-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all disabled:opacity-50 disabled:cursor-not-allowed placeholder:text-text-secondary/50"
              />
            </div>
          </div>

          <div class="space-y-1.5">
            <label for="email" class="block text-sm font-medium text-text-main">E-mail</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <EnvelopeIcon class="h-5 w-5 text-text-secondary" aria-hidden="true" />
              </div>
              <input
                id="email"
                v-model="form.email"
                type="email"
                required
                :disabled="!isAdmin || loading"
                placeholder="seu.email@exemplo.com"
                class="w-full bg-page border border-border text-text-main rounded-xl pl-11 pr-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all disabled:opacity-50 disabled:cursor-not-allowed placeholder:text-text-secondary/50"
              />
            </div>
          </div>

          <template v-if="isAdmin">
            <div class="space-y-1.5">
              <label for="senha" class="block text-sm font-medium text-text-main">Nova Senha (deixe em branco para manter)</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <LockClosedIcon class="h-5 w-5 text-text-secondary" aria-hidden="true" />
                </div>
                <input
                  id="senha"
                  v-model="form.senha"
                  type="password"
                  :disabled="loading"
                  placeholder="Mínimo 6 caracteres"
                  class="w-full bg-page border border-border text-text-main rounded-xl pl-11 pr-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all disabled:opacity-50 disabled:cursor-not-allowed placeholder:text-text-secondary/50"
                />
              </div>
            </div>

            <div class="pt-4">
              <button 
                type="submit" 
                :disabled="loading"
                class="w-full flex justify-center items-center gap-2 bg-primary hover:bg-primary-hover text-white font-bold py-3 px-4 rounded-xl transition-all disabled:opacity-70 disabled:cursor-not-allowed shadow-lg shadow-primary/20"
              >
                <svg v-if="loading" class="animate-spin h-5 w-5 text-white" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <ArrowDownTrayIcon v-else class="w-5 h-5" aria-hidden="true" />
                {{ loading ? 'Salvando...' : 'Salvar Alterações' }}
              </button>
            </div>
          </template>
          
          <template v-else>
            <div class="mt-6 p-4 bg-primary/10 border border-primary/20 rounded-xl flex items-start gap-3">
              <InformationCircleIcon class="w-5 h-5 text-primary shrink-0 mt-0.5" aria-hidden="true" />
              <p class="m-0 text-sm text-text-main">Apenas administradores podem atualizar os dados cadastrais.</p>
            </div>
          </template>

          <p v-if="errorMsg" class="mt-4 p-3 bg-red-400/10 border border-red-400/20 rounded-xl flex items-center gap-2 text-sm text-red-400 m-0">
            <ExclamationTriangleIcon class="w-5 h-5 shrink-0" aria-hidden="true" /> 
            {{ errorMsg }}
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import { useToast } from '@/composables/useToast'
import {
  ArrowLeftIcon,
  UserCircleIcon,
  UserIcon,
  EnvelopeIcon,
  LockClosedIcon,
  ArrowDownTrayIcon,
  InformationCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'

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
const original = ref({ nome: '', email: '' })

const isAdmin = computed(() => authStore.user?.tipo === 'admin')

const userRoleLabel = computed(() => {
  return authStore.user?.tipo === 'admin' ? 'Administrador' : 'Membro'
})

const goBack = () => {
  router.push('/')
}

onMounted(() => {
  if (authStore.user) {
    form.value.nome = authStore.user.nome
    form.value.email = authStore.user.email
    original.value = { nome: authStore.user.nome, email: authStore.user.email }
  } else {
    router.push('/login')
  }
})

const handleUpdate = async () => {
  if (!authStore.user?.id) return
  loading.value = true
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
    
    authStore.user = {
      ...authStore.user,
      nome: response.data.nome,
      email: response.data.email
    }
    
    form.value.senha = ''
    notifySuccess('Perfil atualizado com sucesso!')
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
