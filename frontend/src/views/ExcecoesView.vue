 <template>
  <div class="exceptions-container dark-theme">
    <div class="exceptions-card">
      <div class="card-header">
        <button class="back-btn" @click="goBack" title="Voltar para a Agenda">
          <i class="fas fa-arrow-left"></i>
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
            <i class="fas fa-spinner fa-spin"></i> Carregando exceções...
          </div>
          
          <div v-else-if="excecoes.length === 0" class="empty-state">
            <i class="fas fa-calendar-check"></i>
            <p>Nenhuma exceção configurada para este evento.</p>
          </div>

          <div v-else class="exceptions-grid">
            <div v-for="exc in excecoes" :key="exc.id" class="exc-card">
              <div class="exc-badge-row">
                <span class="exc-badge" :class="exc.tipo === 'CANCELAMENTO' ? 'badge-cancel' : 'badge-resched'">
                  {{ exc.tipo === 'CANCELAMENTO' ? 'Cancelado' : 'Remarcado' }}
                </span>
                <button v-if="isAdmin" class="btn-delete-exc" @click="deleteException(exc.id)" title="Remover Exceção">
                  <i class="fas fa-trash-alt"></i>
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
              <i class="fas fa-plus"></i>
              {{ loading ? 'Adicionando...' : 'Adicionar Exceção' }}
            </button>

            <p v-if="error" class="error-msg"><i class="fas fa-exclamation-triangle"></i> {{ error }}</p>
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

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

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
    alert('Erro ao carregar evento.')
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

    const payload: any = {
      evento_recorrente_id: eventId,
      data_original: dataOriginalStr,
      tipo: form.value.tipo,
      motivo: form.value.motivo.trim() || null,
      criado_por: authStore.user?.id
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
  } catch (err: any) {
    console.error(err)
    error.value = err.response?.data?.error || 'Erro ao salvar exceção.'
  } finally {
    loading.value = false
  }
}

const deleteException = async (id: number) => {
  if (!confirm('Deseja remover esta exceção? O evento voltará ao seu padrão original para essa data.')) return
  try {
    await api.delete(`/eventos/excecoes/${id}`)
    await loadExceptions()
  } catch (err) {
    console.error(err)
    alert('Erro ao excluir exceção.')
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
  padding: 2rem 1rem;
  background-color: #1e1e2f;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.exceptions-card {
  background: #2d2d3a;
  border: 1px solid #3a3a4a;
  border-radius: 16px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
  width: 100%;
  max-width: 1100px;
  padding: 2rem;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #3a3a4a;
  padding-bottom: 1rem;
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

.header-titles h2 {
  margin: 0;
  font-size: 1.6rem;
  color: #ffffff;
}

.header-titles h3 {
  margin: 0.2rem 0 0 0;
  font-size: 1.2rem;
  color: #60a5fa;
  font-weight: 500;
}

.event-details {
  background: rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 2rem;
  font-size: 0.95rem;
  color: #d1d5db;
}

.event-details p {
  margin: 0.3rem 0;
}

.main-layout {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.exceptions-list-section {
  flex: 1;
  min-width: 300px;
}

.form-section {
  width: 400px;
  min-width: 300px;
  background: #242432;
  border: 1px solid #3a3a4a;
  padding: 1.5rem;
  border-radius: 12px;
  height: fit-content;
}

h3 {
  color: #ffffff;
  font-size: 1.2rem;
  margin-top: 0;
  margin-bottom: 1.2rem;
  font-weight: 600;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #9ca3af;
}

.loading-state i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: #3b82f6;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #4b5563;
}

.exceptions-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.exc-card {
  background: #242432;
  border: 1px solid #3a3a4a;
  border-radius: 8px;
  padding: 1rem;
  transition: border-color 0.2s ease;
}

.exc-card:hover {
  border-color: #4b5563;
}

.exc-badge-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
}

.exc-badge {
  font-size: 0.75rem;
  font-weight: bold;
  text-transform: uppercase;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
}

.badge-cancel {
  background-color: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.badge-resched {
  background-color: rgba(245, 158, 11, 0.2);
  color: #fde047;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.btn-delete-exc {
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: 0.2rem;
  font-size: 1rem;
  transition: color 0.2s ease;
}

.btn-delete-exc:hover {
  color: #ef4444;
}

.exc-details {
  font-size: 0.9rem;
  color: #d1d5db;
}

.exc-details p {
  margin: 0.3rem 0;
}

.exc-reason {
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px dashed #3a3a4a;
  color: #9ca3af;
}

.form-group {
  margin-bottom: 1.2rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

label {
  font-size: 0.9rem;
  color: #bbbbcc;
  font-weight: 500;
}

input, select, textarea {
  width: 100%;
  padding: 0.65rem;
  border-radius: 6px;
  border: 1px solid #3a3a4a;
  background: #1e1e2f;
  color: #ffffff;
  font-size: 0.9rem;
  transition: border-color 0.2s ease;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: #3b82f6;
}

input:disabled, select:disabled, textarea:disabled {
  background-color: #1a1a24;
  color: #777788;
  cursor: not-allowed;
}

.form-row {
  display: flex;
  gap: 1rem;
}

.half {
  flex: 1;
}

.helper-text {
  font-size: 0.75rem;
  color: #888899;
  line-height: 1.3;
}

.btn-submit {
  width: 100%;
  padding: 0.75rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: background 0.2s ease;
  margin-top: 1rem;
}

.btn-submit:hover:not(:disabled) {
  background: #2563eb;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-msg {
  background-color: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
  padding: 0.6rem;
  border-radius: 6px;
  font-size: 0.85rem;
  margin-top: 1rem;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}
</style>
