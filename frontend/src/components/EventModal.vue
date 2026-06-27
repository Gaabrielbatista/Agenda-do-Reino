<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible" key="modal" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-[10000] p-4" @click.self="close">
        <div class="bg-card text-text-main rounded-xl w-full max-w-lg max-h-[85vh] overflow-y-auto shadow-2xl border border-border modal-card">
        
        <div class="flex justify-between items-center px-6 py-5 border-b border-border">
          <div class="flex items-center gap-3 min-w-0">
            <div v-if="evento?.cor" class="w-4 h-4 rounded-full flex-shrink-0" :style="{ backgroundColor: evento.cor }"></div>
            <h3 class="m-0 text-xl font-semibold tracking-wide truncate">{{ evento?.titulo || 'Carregando...' }}</h3>
          </div>
          <button class="text-text-secondary hover:text-text-main transition-colors flex-shrink-0" @click="close">
            <XMarkIcon class="w-6 h-6" aria-hidden="true" />
          </button>
        </div>

        <div v-if="error && !evento" class="p-6">
          <p class="text-red-400 bg-red-400/10 p-3 rounded-lg border border-red-400/20">{{ error }}</p>
        </div>

        <div v-else-if="loading && !evento" class="p-6">
            <div class="flex items-center justify-center gap-2 text-text-secondary">
              <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Carregando detalhes...
            </div>
        </div>

        <div v-else-if="evento" ref="expandRef" class="expand-wrapper" :class="{ 'expand-done': contentVisible }">
          <div class="p-6 space-y-5" :class="{ 'content-hidden': !contentVisible, 'content-stagger': contentVisible }">
          <div v-if="evento.descricao" class="space-y-1.5">
              <strong class="flex items-center gap-2 text-[1.05rem] font-semibold text-text-main">
                <DocumentTextIcon class="w-5 h-5 text-primary" aria-hidden="true" />Descrição
              </strong>
              <p class="pl-7 m-0 text-text-secondary leading-relaxed">{{ evento.descricao }}</p>
            </div>

          <template v-if="tipo === 'normal'">
            <div class="space-y-1">
              <strong class="flex items-center gap-2 text-[1.05rem] font-semibold text-text-main">
                <CalendarDaysIcon class="w-5 h-5 text-emerald-500" aria-hidden="true" />Data e Hora
              </strong>
              <div class="pl-7 text-text-secondary">
                {{ formatDateTime(evento.data_inicio) }}
                <span v-if="evento.data_fim"> – {{ formatDateTime(evento.data_fim) }}</span>
              </div>
            </div>
            <div class="space-y-1">
              <strong class="flex items-center gap-2 text-[1.05rem] font-semibold text-text-main">
                <InformationCircleIcon class="w-5 h-5 text-blue-400" aria-hidden="true" />Status:
              </strong> 
              <div class="pl-7 text-text-secondary">
                {{ evento.status === 'ativo' ? 'Ativo' : 'Cancelado' }}
              </div>
            </div>
          </template>

          <template v-if="tipo === 'recorrente'">
            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-1">
                <strong class="flex items-center gap-2 text-[1.05rem] font-semibold text-text-main">
                  <ArrowPathIcon class="w-5 h-5 text-primary" aria-hidden="true" />Recorrência
                </strong>
                <div class="pl-7 text-text-secondary">{{ diasSemana[evento.dia_semana] }}</div>
              </div>
              <div class="space-y-1">
                <strong class="flex items-center gap-2 text-[1.05rem] font-semibold text-text-main">
                  <ClockIcon class="w-5 h-5 text-primary" aria-hidden="true" />Horário
                </strong>
                <div class="pl-7 text-text-secondary">
                  {{ evento.hora_inicio }}
                  <span v-if="evento.hora_fim"> – {{ evento.hora_fim }}</span>
                </div>
              </div>
            </div>

            <div class="space-y-1">
              <strong class="flex items-center gap-2 text-[1.05rem] font-semibold text-text-main">
                <CheckCircleIcon class="w-5 h-5 text-emerald-400" aria-hidden="true" />Ativo
              </strong>
              <div class="pl-7 text-text-secondary">{{ evento.ativo ? 'Sim' : 'Não' }}</div>
            </div>

            <div class="pt-4 border-t border-border space-y-2">
              <strong class="flex items-center gap-2 text-[1.05rem] font-semibold text-text-main">
                <CalendarDaysIcon class="w-5 h-5 text-purple-400" aria-hidden="true" />Próximos Eventos (30 dias)
              </strong>
              <ul v-if="proximasOcorrencias.length" class="pl-7 m-0 space-y-1 text-text-secondary list-disc list-inside">
                <li v-for="occ in proximasOcorrencias" :key="occ">
                  {{ formatDateTime(occ) }}
                </li>
              </ul>
              <p v-else class="pl-7 m-0 text-text-secondary italic">Nenhuma ocorrência futura encontrada.</p>
            </div>

            <div class="pt-4 border-t border-border space-y-2">
              <strong class="flex items-center gap-2 text-[1.05rem] font-semibold text-text-main">
                <ExclamationTriangleIcon class="w-5 h-5 text-amber-400" aria-hidden="true" />Exceções
              </strong>
              <ul v-if="excecoes.length" class="pl-7 m-0 space-y-1 text-text-secondary list-disc list-inside">
                <li v-for="exc in excecoes" :key="exc.id">
                  {{ formatDate(exc.data_original) }} – <span :class="exc.tipo === 'CANCELAMENTO' ? 'text-red-400' : 'text-blue-400'">{{ exc.tipo === 'CANCELAMENTO' ? 'Cancelado' : 'Remarcado' }}</span>
                  <span v-if="exc.tipo === 'REMARCACAO' && exc.data_nova">
                    para {{ formatDateTime(exc.data_nova) }}
                  </span>
                  <span v-if="exc.motivo" class="text-sm opacity-70"> ({{ exc.motivo }})</span>
                </li>
              </ul>
              <p v-else class="pl-7 m-0 text-text-secondary italic">Nenhuma exceção cadastrada.</p>
            </div>
          </template>

          <div class="pt-4 border-t border-border space-y-1">
            <strong class="flex items-center gap-2 text-[1.05rem] font-semibold text-text-main">
              <UserIcon class="w-5 h-5 text-gray-400" aria-hidden="true" />Criado por
            </strong>
            <div class="pl-7 text-text-secondary">{{ creatorName || 'Carregando...' }}</div>
          </div>

          <div class="flex flex-wrap gap-3 mt-8 pt-4 justify-end" v-if="isAdmin">
            <button 
              v-if="tipo === 'recorrente'" 
              class="flex items-center gap-2 px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white font-medium rounded-lg transition-colors" 
              @click="manageExceptions"
            >
              <Cog6ToothIcon class="w-5 h-5" aria-hidden="true" />Exceções
            </button>
            <button 
              class="flex items-center gap-2 px-4 py-2 bg-primary hover:bg-primary-hover text-white font-medium rounded-lg transition-colors" 
              @click="close(); $emit('edit', evento.id, tipo)"
            >
              <PencilSquareIcon class="w-5 h-5" aria-hidden="true" />Editar
            </button>
            <button 
              class="flex items-center gap-2 px-4 py-2 bg-red-500/10 hover:bg-red-500 border border-red-500/30 hover:border-red-500 text-red-500 hover:text-white font-medium rounded-lg transition-colors" 
              @click="deleteEvent"
            >
              <TrashIcon class="w-5 h-5" aria-hidden="true" />Excluir
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import { useToast } from '@/composables/useToast'
import {
  XMarkIcon,
  CalendarDaysIcon,
  DocumentTextIcon,
  InformationCircleIcon,
  ArrowPathIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  UserIcon,
  PencilSquareIcon,
  TrashIcon,
  Cog6ToothIcon,
  ClockIcon
} from '@heroicons/vue/24/outline'

const props = defineProps<{
  visible: boolean
  eventId: number | null
  eventType: 'normal' | 'recorrente' | null
}>()

const emit = defineEmits(['close', 'deleted', "edit"])

const router = useRouter()
const authStore = useAuthStore()
const { notifySuccess, notifyError } = useToast()
const isAdmin = authStore.user?.tipo === 'admin'

const loading = ref(false)
const error = ref('')
const evento = ref<any>(null)
const excecoes = ref<any[]>([])
const proximasOcorrencias = ref<string[]>([])
const tipo = ref<'normal' | 'recorrente' | null>(null)
const creatorName = ref('')
const expandRef = ref<HTMLElement | null>(null)
const contentVisible = ref(false)

const diasSemana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']

const close = () => {
  emit('close')
}

const fetchEvent = async () => {
  if (!props.eventId || !props.eventType) return
  loading.value = true
  error.value = ''
  evento.value = null
  creatorName.value = ''
  excecoes.value = []
  proximasOcorrencias.value = []
  tipo.value = props.eventType
  contentVisible.value = false

  try {
    const endpoint = props.eventType === 'normal'
      ? `/eventos/normais/${props.eventId}`
      : `/eventos/recorrentes/${props.eventId}`
    const response = await api.get(endpoint)
    evento.value = response.data

    if (props.eventType === 'recorrente') {
      const excResponse = await api.get(`/eventos/recorrentes/${props.eventId}/excecoes`)
      excecoes.value = excResponse.data

      const hoje = new Date()
      const fim = new Date()
      fim.setDate(hoje.getDate() + 30)
      const inicioStr = hoje.toISOString().slice(0, 10)
      const fimStr = fim.toISOString().slice(0, 10)
      const agendaResponse = await api.get(`/agenda?inicio=${inicioStr}&fim=${fimStr}`)
      const ocorrencias = agendaResponse.data.filter(
        (ev: any) => ev.source_id === props.eventId && ev.source_type === 'recorrente'
      )
      proximasOcorrencias.value = ocorrencias.map((occ: any) => occ.data_inicio)
    }

    if (evento.value.criado_por) {
      try {
        const userResp = await api.get(`/usuarios/${evento.value.criado_por}`)
        creatorName.value = userResp.data.nome
      } catch {
        creatorName.value = 'Desconhecido'
      }
    }

    loading.value = false
    await nextTick()
    if (expandRef.value) {
      const height = expandRef.value.scrollHeight
      expandRef.value.style.maxHeight = height + 'px'
      await new Promise(r => setTimeout(r, 580))
      contentVisible.value = true
      expandRef.value.style.maxHeight = ''
    } else {
      contentVisible.value = true
    }
  } catch (err) {
    console.error(err)
    error.value = 'Erro ao carregar detalhes do evento.'
    notifyError(error.value)
    loading.value = false
  }
}

const formatDateTime = (iso: string) => {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleString('pt-BR')
}
const formatDate = (iso: string) => {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleDateString('pt-BR')
}

const deleteEvent = async () => {
  if (!confirm('Tem certeza que deseja excluir este evento?')) return
  try {
    const endpoint = tipo.value === 'normal'
      ? `/eventos/normais/${props.eventId}`
      : `/eventos/recorrentes/${props.eventId}`
    await api.delete(endpoint)
    notifySuccess('Evento excluído com sucesso.')
    emit('deleted')
    close()
  } catch (err) {
    console.error(err)
    notifyError('Erro ao excluir evento.')
  }
}

const manageExceptions = () => {
  router.push(`/evento/recorrente/${props.eventId}/excecoes`)
  close()
}

watch(() => props.visible, (newVal) => {
  if (newVal && props.eventId && props.eventType) {
    fetchEvent()
  }
})
</script>

<style scoped>
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

.expand-wrapper {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.55s cubic-bezier(0.16, 1, 0.3, 1);
}
.expand-done {
  max-height: none !important;
  overflow: visible;
}
.content-hidden {
  opacity: 0;
  pointer-events: none;
}

.content-stagger > * {
  animation: section-in 0.35s ease-out both;
}
.content-stagger > *:nth-child(1) { animation-delay: 0.03s; }
.content-stagger > *:nth-child(2) { animation-delay: 0.07s; }
.content-stagger > *:nth-child(3) { animation-delay: 0.11s; }
.content-stagger > *:nth-child(4) { animation-delay: 0.15s; }
.content-stagger > *:nth-child(5) { animation-delay: 0.19s; }
.content-stagger > *:nth-child(6) { animation-delay: 0.23s; }
.content-stagger > *:nth-child(7) { animation-delay: 0.27s; }
.content-stagger > *:nth-child(8) { animation-delay: 0.31s; }
.content-stagger > *:nth-child(9) { animation-delay: 0.35s; }
@keyframes section-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-card::-webkit-scrollbar {
  width: 6px;
}
.modal-card::-webkit-scrollbar-track {
  background: transparent;
}
.modal-card::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: 6px;
}
.modal-card::-webkit-scrollbar-thumb:hover {
  background: var(--text-secondary);
}
</style>