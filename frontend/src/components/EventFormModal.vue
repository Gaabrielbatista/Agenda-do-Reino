<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible" key="modal" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-[10000] p-4" @click.self="close">
        <div class="bg-card text-text-main rounded-xl w-full max-w-lg max-h-[90vh] overflow-y-auto shadow-2xl border border-border modal-card">
        
        <div class="flex justify-between items-center px-6 py-5 border-b border-border">
          <h3 class="m-0 text-xl font-semibold tracking-wide">{{ isEditing ? 'Editar Evento' : 'Novo Evento' }}</h3>
          <button class="text-text-secondary hover:text-text-main transition-colors" @click="close">
            <XMarkIcon class="w-6 h-6" aria-hidden="true" />
          </button>
        </div>

        <div class="p-6">
          <form @submit.prevent="handleSubmit" class="space-y-4">
            
            <div class="space-y-1.5">
              <label class="block text-sm font-medium text-text-main">Título *</label>
              <input 
                v-model="form.titulo" 
                type="text" 
                required 
                class="w-full bg-page border border-border text-text-main rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all placeholder:text-text-secondary/50"
                placeholder="Ex: Festividade dos Jovens"
              />
            </div>
            
            <div class="space-y-1.5">
              <label class="block text-sm font-medium text-text-main">Descrição</label>
              <textarea 
                v-model="form.descricao" 
                rows="3"
                class="w-full bg-page border border-border text-text-main rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all resize-y placeholder:text-text-secondary/50"
                placeholder="Detalhes opcionais..."
              ></textarea>
            </div>
            
            <div class="space-y-1.5">
              <label class="block text-sm font-medium text-text-main">Tipo *</label>
              <select 
                v-model="form.tipo" 
                required 
                :disabled="isEditing"
                class="w-full bg-page border border-border text-text-main rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <option value="normal">Evento Único (Normal)</option>
                <option value="recorrente">Evento Recorrente</option>
              </select>
              <p v-if="isEditing" class="text-xs text-text-secondary mt-1">
                * O tipo de evento não pode ser alterado na edição. Para mudar o tipo, exclua e crie um novo evento.
              </p>
            </div>

            <div class="space-y-1.5">
              <label class="block text-sm font-medium text-text-main">Cor</label>
              <div class="flex flex-wrap gap-2">
                <div
                  v-for="c in cores"
                  :key="c"
                  class="w-8 h-8 rounded-full cursor-pointer ring-2 ring-offset-2 ring-offset-card transition-all hover:scale-110"
                  :class="form.cor === c ? 'ring-primary' : 'ring-transparent'"
                  :style="{ backgroundColor: c }"
                  @click="form.cor = c"
                ></div>
              </div>
            </div>

            <template v-if="form.tipo === 'normal'">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div class="space-y-1.5">
                  <label class="block text-sm font-medium text-text-main">Início *</label>
                  <input 
                    v-model="form.data_inicio" 
                    type="datetime-local" 
                    required 
                    class="w-full bg-page border border-border text-text-main rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all color-scheme-dark"
                  />
                </div>
                <div class="space-y-1.5">
                  <label class="block text-sm font-medium text-text-main">Fim</label>
                  <input 
                    v-model="form.data_fim" 
                    type="datetime-local" 
                    class="w-full bg-page border border-border text-text-main rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all color-scheme-dark"
                  />
                </div>
              </div>
            </template>

            <template v-else>
              <div class="space-y-1.5">
                <label class="block text-sm font-medium text-text-main">Dia da semana *</label>
                <select 
                  v-model="form.dia_semana"
                  class="w-full bg-page border border-border text-text-main rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all"
                >
                  <option :value="0">Segunda</option>
                  <option :value="1">Terça</option>
                  <option :value="2">Quarta</option>
                  <option :value="3">Quinta</option>
                  <option :value="4">Sexta</option>
                  <option :value="5">Sábado</option>
                  <option :value="6">Domingo</option>
                </select>
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div class="space-y-1.5">
                  <label class="block text-sm font-medium text-text-main">Hora Início *</label>
                  <input 
                    v-model="form.hora_inicio" 
                    type="time" 
                    required 
                    class="w-full bg-page border border-border text-text-main rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all color-scheme-dark"
                  />
                </div>
                <div class="space-y-1.5">
                  <label class="block text-sm font-medium text-text-main">Hora Fim</label>
                  <input 
                    v-model="form.hora_fim" 
                    type="time" 
                    class="w-full bg-page border border-border text-text-main rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all color-scheme-dark"
                  />
                </div>
              </div>
              <div class="flex items-center gap-3 pt-2">
                <input 
                  id="ativoCheckbox"
                  v-model="form.ativo" 
                  type="checkbox" 
                  class="w-5 h-5 rounded border-border bg-page text-primary focus:ring-primary focus:ring-offset-card"
                />
                <label for="ativoCheckbox" class="text-sm font-medium text-text-main cursor-pointer select-none">Evento Ativo</label>
              </div>
            </template>

            <div class="flex flex-col sm:flex-row gap-3 pt-6 mt-4 border-t border-border">
              <button 
                type="button" 
                @click="close"
                class="flex-1 sm:flex-none px-6 py-2.5 rounded-lg font-medium text-text-main bg-page border border-border hover:bg-border transition-colors order-2 sm:order-1"
              >
                Cancelar
              </button>
              <button 
                type="submit" 
                :disabled="loading"
                class="flex-1 px-6 py-2.5 rounded-lg font-medium text-white bg-primary hover:bg-primary-hover border border-transparent disabled:opacity-70 disabled:cursor-not-allowed transition-colors order-1 sm:order-2 flex items-center justify-center gap-2"
              >
                <svg v-if="loading" class="animate-spin h-5 w-5 text-white" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ loading ? 'Salvando...' : 'Salvar Evento' }}
              </button>
            </div>
            <p v-if="error" class="text-red-400 bg-red-400/10 p-3 rounded-lg border border-red-400/20 text-sm m-0">{{ error }}</p>
          </form>
        </div>
      </div>
    </div>
  </Transition>
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

const cores = [
  '#3B82F6', '#10B981', '#F59E0B', '#EF4444',
  '#8B5CF6', '#EC4899', '#06B6D4', '#F97316',
  '#6366F1', '#14B8A6', '#84CC16', '#E11D48',
]

const form = ref({
  tipo: 'normal',
  titulo: '',
  descricao: '',
  cor: '#3B82F6',
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
    form.value.cor = data.cor || '#3B82F6'
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
      cor: form.value.cor,
      criado_por: authStore.user?.id
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
      form.value = {
        tipo: 'normal',
        titulo: '',
        descricao: '',
        cor: '#3B82F6',
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
/* Herda color-scheme do :root (dark) / [data-theme="light"] (light) */
.color-scheme-dark {
  color-scheme: inherit;
}
.modal-enter-active {
  transition: opacity 0.3s ease-out;
}
.modal-leave-active {
  transition: opacity 0.2s ease-in;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-active .modal-card {
  animation: modal-pop 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.modal-leave-active .modal-card {
  animation: modal-pop 0.2s ease-in reverse;
}
@keyframes modal-pop {
  from {
    opacity: 0;
    transform: scale(0.92) translateY(-12px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
</style>