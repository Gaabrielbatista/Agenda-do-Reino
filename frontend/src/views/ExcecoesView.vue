 <template>
  <div class="exceptions-container">
    <div class="exceptions-card">
      <div class="card-header">
        <button class="back-btn" @click="goBack" title="Voltar para a Agenda">
          <ArrowLeftIcon class="icon-svg" aria-hidden="true" />
        </button>
        <div class="header-titles">
          <h2>Gerenciar Exceções</h2>
          <h3 v-if="evento">{{ evento.titulo }}</h3>
        </div>
      </div>

      <!-- Informações do Evento Recorrente -->
      <div class="event-details" v-if="evento">
        <p><strong>Recorrência:</strong> {{ diasSemana[evento.dia_semana] }} às {{ evento.hora_inicio }} <span v-if="evento.hora_fim">até {{ evento.hora_fim }}</span></p>
        <p v-if="evento.descricao"><strong>Descrição:</strong> {{ evento.descricao }}</p>
      </div>

      <div class="main-layout">
        <!-- Listagem de Exceções Existentes -->
        <div class="exceptions-list-section">
          <h3>Exceções Configuradas</h3>
          
          <div v-if="loadingList" class="loading-state">
            <ArrowPathIcon class="loading-icon animate-spin" aria-hidden="true" /> Carregando exceções...
          </div>
          
          <div v-else-if="excecoes.length === 0" class="empty-state">
            <CalendarDaysIcon class="icon-svg" aria-hidden="true" />
            <p>Nenhuma exceção configurada para este evento.</p>
          </div>

          <div v-else class="exceptions-grid">
            <div v-for="exc in excecoes" :key="exc.id" class="exc-card">
              <div class="exc-badge-row">
                <span class="exc-badge" :class="exc.tipo === 'CANCELAMENTO' ? 'badge-cancel' : 'badge-resched'">
                  {{ exc.tipo === 'CANCELAMENTO' ? 'Cancelado' : 'Remarcado' }}
                </span>
                <button v-if="isAdmin" class="btn-delete-exc" @click="deleteException(exc.id)" title="Remover Exceção">
                  <TrashIcon class="btn-icon" aria-hidden="true" />
                </button>
              </div>

              <div class="exc-details">
                <p><strong>Ocorrência Original:</strong> {{ formatDateTimeStr(exc.data_original) }}</p>
                
                <template v-if="exc.tipo === 'REMARCACAO'">
                  <p><strong>Nova Data/Hora:</strong> {{ formatNewDateTime(exc) }}</p>
                </template>

                <p v-if="exc.motivo" class="exc-reason">
                  <strong>Motivo:</strong> <em>"{{ exc.motivo }}"</em>
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Formulário para Criar Nova Exceção (Apenas Admin) -->
        <div class="form-section" v-if="isAdmin && evento">
          <h3>Nova Exceção</h3>
          
          <form @submit.prevent="handleSubmit">
            <div class="form-group">
              <label for="data_original">Data da Ocorrência Original *</label>
              <input
                id="data_original"
                v-model="form.data_original_date"
                type="date"
                required
                :disabled="loading"
              />
              <span class="helper-text">
                Selecione o dia da ocorrência que deseja alterar (deve ser um(a) <strong>{{ diasSemana[evento.dia_semana] }}</strong>).
              </span>
            </div>

            <div class="form-group">
              <label for="tipo_excecao">Tipo de Exceção *</label>
              <select id="tipo_excecao" v-model="form.tipo" required :disabled="loading">
                <option value="cancelamento">Cancelamento (Remover ocorrência)</option>
                <option value="remarcacao">Remarcação (Mudar data/horários)</option>
              </select>
            </div>

            <template v-if="form.tipo === 'remarcacao'">
              <div class="form-group">
                <label for="data_nova">Nova Data</label>
                <input
                  id="data_nova"
                  v-model="form.data_nova_date"
                  type="date"
                  :disabled="loading"
                />
                <span class="helper-text">Deixe em branco para manter o mesmo dia e alterar apenas horários.</span>
              </div>

              <div class="form-row">
                <div class="form-group half">
                  <label for="hora_nova_inicio">Nova Hora Início *</label>
                  <input
                    id="hora_nova_inicio"
                    v-model="form.hora_nova_inicio"
                    type="time"
                    required
                    :disabled="loading"
                  />
                </div>
                <div class="form-group half">
                  <label for="hora_nova_fim">Nova Hora Fim</label>
                  <input
                    id="hora_nova_fim"
                    v-model="form.hora_nova_fim"
                    type="time"
                    :disabled="loading"
                  />
                </div>
              </div>
            </template>

            <div class="form-group">
              <label for="motivo">Motivo / Justificativa</label>
              <textarea
                id="motivo"
                v-model="form.motivo"
                rows="2"
                placeholder="Ex: Feriado nacional, manutenção do templo, etc."
                :disabled="loading"
              ></textarea>
            </div>

            <button type="submit" class="btn-submit" :disabled="loading">
              <PlusIcon class="btn-icon" aria-hidden="true" />
              {{ loading ? 'Adicionando...' : 'Adicionar Exceção' }}
            </button>

            <p v-if="error" class="error-msg"><ExclamationTriangleIcon class="btn-icon" aria-hidden="true" /> {{ error }}</p>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import { useToast } from '@/composables/useToast'
import {
  ArrowLeftIcon,
  ArrowPathIcon,
  CalendarDaysIcon,
  TrashIcon,
  PlusIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const { notifySuccess, notifyError } = useToast()

const eventId = Number(route.params.id)
const isAdmin = computed(() => authStore.user?.tipo === 'admin')

const evento = ref<any>(null)
const excecoes = ref<any[]>([])
const loading = ref(false)
const loadingList = ref(false)
const error = ref('')

const diasSemana = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']

const form = ref({
  data_original_date: '',
  tipo: 'cancelamento',
  data_nova_date: '',
  hora_nova_inicio: '',
  hora_nova_fim: '',
  motivo: ''
})

const goBack = () => {
  router.push('/')
}

const loadEvent = async () => {
  try {
    const { data } = await api.get(`/eventos/recorrentes/${eventId}`)
    evento.value = data
    // Inicializa a hora padrão de início para conveniência
    form.value.hora_nova_inicio = data.hora_inicio
    form.value.hora_nova_fim = data.hora_fim || ''
  } catch (err) {
    console.error(err)
    notifyError('Erro ao carregar evento.')
    router.push('/')
  }
}

const loadExceptions = async () => {
  loadingList.value = true
  try {
    const { data } = await api.get(`/eventos/recorrentes/${eventId}/excecoes`)
    excecoes.value = data
  } catch (err) {
    console.error(err)
  } finally {
    loadingList.value = false
  }
}

const formatDateTimeStr = (iso: string) => {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleString('pt-BR')
}

const formatNewDateTime = (exc: any) => {
  let output = ''
  if (exc.data_nova) {
    const d = new Date(exc.data_nova)
    output += d.toLocaleDateString('pt-BR')
  } else {
    // Mesma data do original
    const d = new Date(exc.data_original)
    output += d.toLocaleDateString('pt-BR')
  }
  output += ` às ${exc.hora_nova_inicio}`
  if (exc.hora_nova_fim) {
    output += ` – ${exc.hora_nova_fim}`
  }
  return output
}

const validateOriginalDateWeekday = () => {
  if (!form.value.data_original_date || !evento.value) return true
  
  // Date input está em YYYY-MM-DD local, criamos um objeto data correspondente
  const parts = form.value.data_original_date.split('-')
  const year = parseInt(parts[0])
  const month = parseInt(parts[1]) - 1
  const day = parseInt(parts[2])
  const d = new Date(year, month, day)
  
  // JS weekday: 0=Domingo, 1=Segunda, ..., 6=Sábado
  // Backend weekday: 0=Segunda, 1=Terça, ..., 6=Domingo
  let jsDay = d.getDay()
  let backendDay = jsDay === 0 ? 6 : jsDay - 1
  
  return backendDay === evento.value.dia_semana
}

const handleSubmit = async () => {
  loading.value = true
  error.value = ''

  if (!validateOriginalDateWeekday()) {
    error.value = `A data original selecionada não cai em um(a) ${diasSemana[evento.value.dia_semana]}.`
    loading.value = false
    return
  }

  try {
    // Monta a data_original adicionando o horário de início original do evento
    const dataOriginalStr = `${form.value.data_original_date}T${evento.value.hora_inicio}:00`
    const tipoPayload = form.value.tipo === 'cancelamento' ? 'CANCELAMENTO' : 'REMARCACAO'
    const payload: any = {
      evento_recorrente_id: eventId,
      data_original: dataOriginalStr,
      tipo: tipoPayload,
      motivo: form.value.motivo.trim() || null,
      criado_por: authStore.user?.id,
    }

    if (form.value.tipo === 'remarcacao') {
      if (form.value.data_nova_date) {
        payload.data_nova = `${form.value.data_nova_date}T${form.value.hora_nova_inicio}:00`
      } else {
        payload.data_nova = null
      }
      payload.hora_nova_inicio = form.value.hora_nova_inicio
      payload.hora_nova_fim = form.value.hora_nova_fim || null
    }

    await api.post('/eventos/excecoes', payload)

    // Sucesso, recarrega exceções e reseta form
    await loadExceptions()
    form.value.data_original_date = ''
    form.value.data_nova_date = ''
    form.value.motivo = ''
    form.value.tipo = 'cancelamento'
    notifySuccess(tipoPayload === 'CANCELAMENTO'
      ? 'Exceção de cancelamento adicionada com sucesso.'
      : 'Exceção de remarcação adicionada com sucesso.')
  } catch (err: any) {
    console.error(err)
    error.value = err.response?.data?.error || 'Erro ao salvar exceção.'
    notifyError(error.value)
  } finally {
    loading.value = false
  }
}

const deleteException = async (id: number) => {
  if (!confirm('Deseja remover esta exceção? O evento voltará ao seu padrão original para essa data.')) return
  try {
    await api.delete(`/eventos/excecoes/${id}`)
    await loadExceptions()
    notifySuccess('Exceção removida com sucesso.')
  } catch (err) {
    console.error(err)
    notifyError('Erro ao excluir exceção.')
  }
}

onMounted(() => {
  loadEvent()
  loadExceptions()
})
</script>

<style scoped>
.exceptions-container {
  min-height: 100vh;
  background-color: var(--bg-page);
  padding: 2rem;
  color: var(--text-primary);
  display: flex;
  justify-content: center;
  transition: background-color 0.3s;
}

.exceptions-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  width: 100%;
  max-width: 1000px;
}

input, select, textarea {
  width: 100%;
  padding: 0.65rem;
  border-radius: 6px;
  border: 1px solid var(--input-border);
  background: var(--input-bg);
  color: var(--text-primary);
  font-size: 0.9rem;
  transition: border-color 0.2s ease;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: var(--btn-primary);
}

/* Estilos Estruturais das Exceções */
.card-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 1rem; }
.back-btn { background: none; border: none; color: var(--text-primary); cursor: pointer; }
.back-btn svg { width: 1.2rem; height: 1.2rem; }
.event-details { margin-bottom: 2rem; padding: 1rem; background: rgba(0,0,0,0.1); border-radius: 8px; }
.main-layout { display: flex; flex-direction: column; gap: 2rem; }
.form-group { margin-bottom: 1.2rem; }
.helper-text { font-size: 0.8rem; color: var(--text-secondary); display: block; margin-top: 0.3rem; }
.btn-submit { width: 100%; padding: 0.8rem; background: var(--btn-primary); color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 1rem; transition: background 0.2s;}
.btn-submit:hover { background: var(--btn-primary-hover); }
.btn-icon { width: 1rem; height: 1rem; margin-right: 0.4rem; }
.success-msg { margin-top: 0.75rem; color: #10b981; font-weight: 600; display: flex; align-items: center; gap: 0.4rem; }
.exc-card { border: 1px solid var(--border-color); padding: 1rem; border-radius: 8px; margin-bottom: 1rem; background: var(--bg-page); }
.exc-badge-row { display: flex; justify-content: space-between; margin-bottom: 0.8rem; }
.exc-badge { padding: 0.3rem 0.6rem; border-radius: 4px; font-size: 0.8rem; font-weight: bold; }
.badge-cancel { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
.badge-resched { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }
.btn-delete-exc { background: none; border: none; color: #ef4444; cursor: pointer; }
.empty-state { text-align: center; padding: 2rem; color: var(--text-secondary); }
.empty-state svg { width: 2rem; height: 2rem; margin-bottom: 0.5rem; }
.loading-icon { width: 1rem; height: 1rem; margin-right: 0.5rem; }
.animate-spin { animation: spin 1s linear infinite; }
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
