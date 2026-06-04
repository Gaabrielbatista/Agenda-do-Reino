<template>
  <div class="form-container">
    <h1>{{ isEditing ? 'Editar Evento' : 'Novo Evento' }}</h1>

    <form @submit.prevent="handleSubmit">
      <!-- Campos comuns -->
      <div class="form-group">
        <label for="titulo">Título *</label>
        <input id="titulo" v-model="form.titulo" type="text" required />
      </div>

      <div class="form-group">
        <label for="descricao">Descrição</label>
        <textarea id="descricao" v-model="form.descricao" rows="3"></textarea>
      </div>

      <div class="form-group">
        <label for="tipo">Tipo *</label>
        <select id="tipo" v-model="form.tipo" required>
          <option value="normal">Normal</option>
          <option value="recorrente">Recorrente</option>
        </select>
      </div>

      <!-- Campos para evento normal -->
      <template v-if="form.tipo === 'normal'">
        <div class="form-group">
          <label for="data_inicio">Data e Hora de Início *</label>
          <input id="data_inicio" v-model="form.data_inicio" type="datetime-local" required />
        </div>
        <div class="form-group">
          <label for="data_fim">Data e Hora de Fim</label>
          <input id="data_fim" v-model="form.data_fim" type="datetime-local" />
        </div>
      </template>

      <!-- Campos para evento recorrente -->
      <template v-if="form.tipo === 'recorrente'">
        <div class="form-group">
          <label for="dia_semana">Dia da semana *</label>
          <select id="dia_semana" v-model="form.dia_semana" required>
            <option :value="0">Segunda-feira</option>
            <option :value="1">Terça-feira</option>
            <option :value="2">Quarta-feira</option>
            <option :value="3">Quinta-feira</option>
            <option :value="4">Sexta-feira</option>
            <option :value="5">Sábado</option>
            <option :value="6">Domingo</option>
          </select>
        </div>
        <div class="form-group">
          <label for="hora_inicio">Hora de Início *</label>
          <input id="hora_inicio" v-model="form.hora_inicio" type="time" required />
        </div>
        <div class="form-group">
          <label for="hora_fim">Hora de Fim</label>
          <input id="hora_fim" v-model="form.hora_fim" type="time" />
        </div>
        <div class="form-group checkbox">
          <input id="ativo" v-model="form.ativo" type="checkbox" />
          <label for="ativo">Ativo</label>
        </div>
      </template>

      <div class="button-group">
        <button type="submit" :disabled="loading">{{ loading ? 'Salvando...' : 'Salvar' }}</button>
        <button type="button" @click="cancel">Cancelar</button>
      </div>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const isEditing = computed(() => !!route.params.id)
const eventType = computed(() => route.params.type as 'normal' | 'recorrente' | undefined)
const eventId = computed(() => route.params.id ? Number(route.params.id) : null)

const loading = ref(false)
const error = ref('')

const form = ref({
  tipo: 'normal',
  titulo: '',
  descricao: '',
  // normal
  data_inicio: '',
  data_fim: '',
  // recorrente
  dia_semana: 0,
  hora_inicio: '',
  hora_fim: '',
  ativo: true
})

// Carrega dados se for edição
const loadEvent = async () => {
  if (!isEditing.value || !eventType.value || !eventId.value) return
  try {
    const endpoint = eventType.value === 'normal'
      ? `/eventos/normais/${eventId.value}`
      : `/eventos/recorrentes/${eventId.value}`
    const { data } = await api.get(endpoint)
    form.value.tipo = eventType.value
    form.value.titulo = data.titulo
    form.value.descricao = data.descricao || ''
    if (eventType.value === 'normal') {
      form.value.data_inicio = data.data_inicio?.slice(0, 16) || ''
      form.value.data_fim = data.data_fim?.slice(0, 16) || ''
    } else {
      form.value.dia_semana = data.dia_semana
      form.value.hora_inicio = data.hora_inicio
      form.value.hora_fim = data.hora_fim || ''
      form.value.ativo = data.ativo
    }
  } catch (err) {
    console.error(err)
    error.value = 'Erro ao carregar evento para edição.'
  }
}

const handleSubmit = async () => {
  loading.value = true
  error.value = ''

  try {
    let payload: any = {
      titulo: form.value.titulo,
      descricao: form.value.descricao || null,
      criado_por: authStore.user?.id
    }

    if (form.value.tipo === 'normal') {
      if (!form.value.data_inicio) throw new Error('Data/hora de início é obrigatória')
      payload.data_inicio = form.value.data_inicio
      payload.data_fim = form.value.data_fim || null
      // criado_por será obtido do token pelo backend

      if (isEditing.value && eventType.value === 'normal') {
        await api.put(`/eventos/normais/${eventId.value}`, payload)
      } else {
        await api.post('/eventos/normais', payload)
      }
    } else {
      if (form.value.dia_semana === undefined) throw new Error('Dia da semana é obrigatório')
      if (!form.value.hora_inicio) throw new Error('Hora de início é obrigatória')
      payload.dia_semana = form.value.dia_semana
      payload.hora_inicio = form.value.hora_inicio
      payload.hora_fim = form.value.hora_fim || null
      payload.ativo = form.value.ativo

      if (isEditing.value && eventType.value === 'recorrente') {
        await api.put(`/eventos/recorrentes/${eventId.value}`, payload)
      } else {
        await api.post('/eventos/recorrentes', payload)
      }
    }

    router.push('/')
  } catch (err: any) {
    console.error(err)
    error.value = err.response?.data?.error || err.message || 'Erro ao salvar evento.'
  } finally {
    loading.value = false
  }
}

const cancel = () => {
  router.push('/')
}

onMounted(() => {
  loadEvent()
})
</script>

<style scoped>
.form-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  color: var(--text-primary);
  transition: all 0.3s;
}

h1 {
  margin-top: 0;
  color: var(--text-primary);
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.3rem;
  font-weight: 500;
}

input, select, textarea {
  width: 100%;
  padding: 0.6rem;
  border-radius: 6px;
  border: 1px solid var(--input-border);
  background: var(--input-bg);
  color: var(--text-primary);
  transition: border-color 0.2s;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: var(--btn-primary);
}
</style>