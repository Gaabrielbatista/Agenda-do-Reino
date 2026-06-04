<template>
  <Teleport to="body">
    <div v-if="visible" class="modal-overlay" @click.self="close">
      <div class="modal-container">
        <div class="modal-header">
          <h3>{{ isEditing ? 'Editar Evento' : 'Novo Evento' }}</h3>
          <button class="close-btn" @click="close"><XMarkIcon class="icon-svg" aria-hidden="true" /></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="form-group">
              <label>Título *</label>
              <input v-model="form.titulo" type="text" required />
            </div>
            <div class="form-group">
              <label>Descrição</label>
              <textarea v-model="form.descricao" rows="3"></textarea>
            </div>
            <div class="form-group">
              <label>Tipo *</label>
              <select v-model="form.tipo" required :disabled="isEditing">
                <option value="normal">Normal</option>
                <option value="recorrente">Recorrente</option>
              </select>
              <small v-if="isEditing" class="tipo-aviso">
                * O tipo de evento não pode ser alterado na edição. Para mudar o tipo, exclua e crie um novo evento.
              </small>
            </div>

            <template v-if="form.tipo === 'normal'">
              <div class="form-group">
                <label>Data/Hora Início *</label>
                <input v-model="form.data_inicio" type="datetime-local" required />
              </div>
              <div class="form-group">
                <label>Data/Hora Fim</label>
                <input v-model="form.data_fim" type="datetime-local" />
              </div>
            </template>

            <template v-else>
              <div class="form-group">
                <label>Dia da semana *</label>
                <select v-model="form.dia_semana">
                  <option :value="0">Segunda</option>
                  <option :value="1">Terça</option>
                  <option :value="2">Quarta</option>
                  <option :value="3">Quinta</option>
                  <option :value="4">Sexta</option>
                  <option :value="5">Sábado</option>
                  <option :value="6">Domingo</option>
                </select>
              </div>
              <div class="form-group">
                <label>Hora Início *</label>
                <input v-model="form.hora_inicio" type="time" required />
              </div>
              <div class="form-group">
                <label>Hora Fim</label>
                <input v-model="form.hora_fim" type="time" />
              </div>
              <div class="form-group checkbox">
                <input v-model="form.ativo" type="checkbox" />
                <label>Ativo</label>
              </div>
            </template>

            <div class="button-group">
              <button type="submit" :disabled="loading">{{ loading ? 'Salvando...' : 'Salvar' }}</button>
              <button type="button" @click="close">Cancelar</button>
            </div>
            <p v-if="error" class="error">{{ error }}</p>
          </form>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'

const props = defineProps<{
  visible: boolean
  eventId?: number | null
  eventType?: 'normal' | 'recorrente' | null
}>()

const emit = defineEmits(['close', 'saved'])

const authStore = useAuthStore()
const { notifySuccess, notifyError } = useToast()
const loading = ref(false)
const error = ref('')
const isEditing = computed(() => !!props.eventId)

const form = ref({
  tipo: 'normal',
  titulo: '',
  descricao: '',
  data_inicio: '',
  data_fim: '',
  dia_semana: 0,
  hora_inicio: '',
  hora_fim: '',
  ativo: true
})

const loadEvent = async () => {
  if (!props.eventId || !props.eventType) return
  try {
    const endpoint = props.eventType === 'normal'
      ? `/eventos/normais/${props.eventId}`
      : `/eventos/recorrentes/${props.eventId}`
    const { data } = await api.get(endpoint)
    form.value.tipo = props.eventType
    form.value.titulo = data.titulo
    form.value.descricao = data.descricao || ''
    if (props.eventType === 'normal') {
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
    error.value = 'Erro ao carregar evento.'
  }
}

const handleSubmit = async () => {
  loading.value = true
  error.value = ''
  try {
    const payload: any = {
      titulo: form.value.titulo,
      descricao: form.value.descricao || null,
      criado_por: authStore.user?.id  // essencial!
    }

    if (form.value.tipo === 'normal') {
      payload.data_inicio = form.value.data_inicio
      payload.data_fim = form.value.data_fim || null
      if (isEditing.value) {
        await api.put(`/eventos/normais/${props.eventId}`, payload)
      } else {
        await api.post('/eventos/normais', payload)
      }
    } else {
      payload.dia_semana = form.value.dia_semana
      payload.hora_inicio = form.value.hora_inicio
      payload.hora_fim = form.value.hora_fim || null
      payload.ativo = form.value.ativo
      if (isEditing.value) {
        await api.put(`/eventos/recorrentes/${props.eventId}`, payload)
      } else {
        await api.post('/eventos/recorrentes', payload)
      }
    }
    notifySuccess(isEditing.value ? 'Evento atualizado com sucesso!' : 'Evento criado com sucesso!')
    emit('saved')
    close()
  } catch (err: any) {
    console.error(err)
    error.value = err.response?.data?.error || 'Erro ao salvar evento.'
    notifyError(error.value)
  } finally {
    loading.value = false
  }
}

const close = () => {
  emit('close')
}

watch(() => props.visible, (newVal) => {
  if (newVal) {
    if (isEditing.value) loadEvent()
    else {
      // resetar formulário
      form.value = {
        tipo: 'normal',
        titulo: '',
        descricao: '',
        data_inicio: '',
        data_fim: '',
        dia_semana: 0,
        hora_inicio: '',
        hora_fim: '',
        ativo: true
      }
    }
    error.value = ''
  }
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-container {
  background: var(--bg-card);
  color: var(--text-primary);
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.close-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 1.5rem;
  cursor: pointer;
}

.close-btn:hover {
  color: var(--text-primary);
}

.modal-body {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.3rem;
  font-weight: 500;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

button[type="submit"] {
  flex: 1;
  padding: 0.75rem;
  background: #3b82f6;
  background: var(--btn-primary, #3b82f6);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}

button[type="submit"]:hover:not(:disabled) {
  background: #2563eb;
  background: var(--btn-primary-hover, #2563eb);
}

button[type="button"] {
  flex: 0.5;
  padding: 0.75rem;
  background: #4b5563;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: opacity 0.2s;
}

button[type="button"]:hover {
  opacity: 0.9;
}

.error {
  color: #f87171;
  margin-top: 1rem;
}

/* --- Substitua o final do seu CSS por isto --- */

input, select, textarea {
  width: 100%;
  padding: 0.6rem;
  border-radius: 6px;
  border: 1px solid var(--btn-primary) !important;  /* <-- FORÇADO com !important */
  background: var(--input-bg);
  color: var(--text-primary);
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: var(--btn-primary) !important;  /* <-- FORÇADO com !important */
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}

/* TEMA ESCURO - Ajuste do Select e Opções */
:root.dark-theme select,
body.dark-theme select {
  background-color: #1e1e2f !important;
  color: #e0e0e0 !important;
}

:root.dark-theme select option,
body.dark-theme select option {
  background-color: #2d2d3a !important;
  color: #e0e0e0 !important;
}

:root.dark-theme select option:checked,
body.dark-theme select option:checked {
  background-color: #3b82f6 !important;
  color: white !important;
}

/* TEMA ESCURO - Fundo azul escuro para TODOS os campos */
:root.dark-theme input,
:root.dark-theme select,
:root.dark-theme textarea,
:root.dark-theme input[type="datetime-local"],
:root.dark-theme input[type="time"] {
  background-color: #1e1e2f !important;  /* Mesmo fundo do campo "Tipo" */
  color: #e0e0e0 !important;             /* Texto claro */
  border-color: var(--btn-primary) !important; /* Borda azul */
}

/* Opcional: Ajuste do placeholder (texto de exemplo) no tema escuro */
:root.dark-theme input::placeholder,
:root.dark-theme textarea::placeholder {
  color: #888888 !important;
}

/* TEMA CLARO */
:root:not(.dark-theme) input,
:root:not(.dark-theme) select,
:root:not(.dark-theme) textarea {
  background-color: var(--input-bg);
  color: var(--text-primary);
}

.tipo-aviso {
  display: block;
  margin-top: 0.3rem;
  color: var(--text-secondary);
  font-size: 0.85rem;
}

select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>