<template>
  <Teleport to="body">
    <div v-if="visible" class="modal-overlay" @click.self="close">
      <div class="modal-container">
        <div class="modal-header">
          <h3>{{ evento?.titulo || 'Carregando...' }}</h3>
          <button class="close-btn" @click="close">✕</button>
        </div>

        <div v-if="loading" class="modal-body">
          <p>Carregando detalhes...</p>
        </div>

        <div v-else-if="error" class="modal-body">
          <p class="error">{{ error }}</p>
        </div>

        <div v-else-if="evento" class="modal-body">
          <!-- Informações comuns -->
          <div class="info-row">
            <strong>📅 Data/Hora:</strong>
            {{ formatDateTime(evento.data_inicio) }}
            <span v-if="evento.data_fim"> – {{ formatDateTime(evento.data_fim) }}</span>
          </div>
          <div class="info-row" v-if="evento.descricao">
            <strong>📝 Descrição:</strong> {{ evento.descricao }}
          </div>

          <!-- Se for evento normal -->
          <template v-if="tipo === 'normal'">
            <div class="info-row">
              <strong>🖌️ Status:</strong> {{ evento.status === 'ativo' ? 'Ativo' : 'Cancelado' }}
            </div>
          </template>

          <!-- Se for evento recorrente -->
          <template v-if="tipo === 'recorrente'">
            <div class="info-row">
              <strong>🔁 Recorrência:</strong>
              {{ diasSemana[evento.dia_semana] }} às {{ evento.hora_inicio }}
              <span v-if="evento.hora_fim"> – {{ evento.hora_fim }}</span>
            </div>
            <div class="info-row">
              <strong>✅ Ativo:</strong> {{ evento.ativo ? 'Sim' : 'Não' }}
            </div>

            <!-- Próximas ocorrências -->
            <div class="info-section">
              <strong>📅 Próximas ocorrências (30 dias):</strong>
              <ul v-if="proximasOcorrencias.length">
                <li v-for="occ in proximasOcorrencias" :key="occ">
                  {{ formatDateTime(occ) }}
                </li>
              </ul>
              <p v-else>Nenhuma ocorrência futura encontrada.</p>
            </div>

            <!-- Exceções -->
            <div class="info-section">
              <strong>⚠️ Exceções:</strong>
              <ul v-if="excecoes.length">
                <li v-for="exc in excecoes" :key="exc.id">
                  {{ formatDate(exc.data_original) }} – {{ exc.tipo === 'CANCELAMENTO' ? 'Cancelado' : 'Remarcado' }}
                  <span v-if="exc.tipo === 'REMARCACAO' && exc.data_nova">
                    para {{ formatDateTime(exc.data_nova) }}
                  </span>
                  <span v-if="exc.motivo"> ({{ exc.motivo }})</span>
                </li>
              </ul>
              <p v-else>Nenhuma exceção cadastrada.</p>
            </div>
          </template>

          <div class="info-row">
            <strong>👤 Criado por:</strong> ID {{ evento.criado_por }}
          </div>

          <!-- Botões de ação (apenas admin) -->
          <div class="action-buttons" v-if="isAdmin">
            <button class="btn-edit" @click="$emit('edit', evento.id, tipo)">✏️ Editar</button>
            <button class="btn-delete" @click="deleteEvent">🗑️ Excluir</button>
            <button v-if="tipo === 'recorrente'" class="btn-exceptions" @click="manageExceptions">
              ⚙️ Gerenciar Exceções
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const props = defineProps<{
  visible: boolean
  eventId: number | null
  eventType: 'normal' | 'recorrente' | null
}>()

const emit = defineEmits(['close', 'deleted', "edit"])

const router = useRouter()
const authStore = useAuthStore()
const isAdmin = authStore.user?.tipo === 'admin'

const loading = ref(false)
const error = ref('')
const evento = ref<any>(null)
const excecoes = ref<any[]>([])
const proximasOcorrencias = ref<string[]>([])
const tipo = ref<'normal' | 'recorrente' | null>(null)

const diasSemana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']

const close = () => {
  emit('close')
}

const fetchEvent = async () => {
  if (!props.eventId || !props.eventType) return
  loading.value = true
  error.value = ''
  evento.value = null
  excecoes.value = []
  proximasOcorrencias.value = []
  tipo.value = props.eventType

  try {
    // Busca dados do evento
    const endpoint = props.eventType === 'normal'
      ? `/eventos/normais/${props.eventId}`
      : `/eventos/recorrentes/${props.eventId}`
    const response = await api.get(endpoint)
    evento.value = response.data

    // Se for recorrente, busca exceções e próximas ocorrências
    if (props.eventType === 'recorrente') {
      // Exceções
      const excResponse = await api.get(`/eventos/recorrentes/${props.eventId}/excecoes`)
      excecoes.value = excResponse.data

      // Próximas ocorrências (próximos 30 dias)
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
  } catch (err) {
    console.error(err)
    error.value = 'Erro ao carregar detalhes do evento.'
  } finally {
    loading.value = false
  }
}

// Formatação de data/hora local
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

// Ações
const deleteEvent = async () => {
  if (!confirm('Tem certeza que deseja excluir este evento?')) return
  try {
    const endpoint = tipo.value === 'normal'
      ? `/eventos/normais/${props.eventId}`
      : `/eventos/recorrentes/${props.eventId}`
    await api.delete(endpoint)
    emit('deleted')
    close()
  } catch (err) {
    console.error(err)
    alert('Erro ao excluir evento.')
  }
}

const manageExceptions = () => {
  router.push(`/evento/recorrente/${props.eventId}/excecoes`)
  close()
}

// Observa a visibilidade e o ID para carregar dados ao abrir
watch(() => props.visible, (newVal) => {
  if (newVal && props.eventId && props.eventType) {
    fetchEvent()
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
  z-index: 10000;
}
.modal-container {
  background: #2d2d3a;
  color: #e0e0e0;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0,0,0,0.3);
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #3a3a4a;
}
.modal-header h3 {
  margin: 0;
  font-size: 1.3rem;
}
.close-btn {
  background: none;
  border: none;
  color: #aaa;
  font-size: 1.5rem;
  cursor: pointer;
}
.close-btn:hover {
  color: white;
}
.modal-body {
  padding: 1.5rem;
}
.info-row {
  margin-bottom: 0.8rem;
}
.info-section {
  margin-top: 1rem;
  border-top: 1px solid #3a3a4a;
  padding-top: 1rem;
}
.info-section ul {
  margin: 0.5rem 0 0 1.2rem;
  padding-left: 0;
}
.info-section li {
  margin: 0.2rem 0;
}
.error {
  color: #f87171;
}
.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  justify-content: flex-end;
}
.btn-edit, .btn-delete, .btn-exceptions {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}
.btn-edit {
  background: #3b82f6;
  color: white;
}
.btn-delete {
  background: #ef4444;
  color: white;
}
.btn-exceptions {
  background: #10b981;
  color: white;
}
</style>