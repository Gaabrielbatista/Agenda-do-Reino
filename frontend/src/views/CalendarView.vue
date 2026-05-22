<template>
  <div class="app-layout dark-theme">
    <aside :class="['sidebar', { collapsed: isCollapsed }]">
      <div class="sidebar-header">
        <button class="toggle-btn" @click="toggleSidebar">
          <i :class="isCollapsed ? 'fas fa-bars' : 'fas fa-chevron-left'"></i>
        </button>
      </div>
      <nav class="sidebar-nav">
        <button v-if="isAdmin" class="nav-item" @click="openCreateModal">
          <i class="fas fa-plus-circle"></i>
          <span v-if="!isCollapsed">Novo Evento</span>
        </button>
        <div class="nav-divider" v-if="!isCollapsed">Visualização</div>
        <button class="nav-item" @click="changeView('dayGridMonth')" :class="{ active: currentView === 'dayGridMonth' }">
          <i class="fas fa-calendar-alt"></i>
          <span v-if="!isCollapsed">Mês</span>
        </button>
        <button class="nav-item" @click="changeView('timeGridWeek')" :class="{ active: currentView === 'timeGridWeek' }">
          <i class="fas fa-calendar-week"></i>
          <span v-if="!isCollapsed">Semana</span>
        </button>
        <button class="nav-item" @click="changeView('timeGridDay')" :class="{ active: currentView === 'timeGridDay' }">
          <i class="fas fa-calendar-day"></i>
          <span v-if="!isCollapsed">Dia</span>
        </button>
        <div class="nav-divider" v-if="!isCollapsed">Conta</div>
        <button class="nav-item" @click="goToProfile">
          <i class="fas fa-user-circle"></i>
          <span v-if="!isCollapsed">Perfil</span>
        </button>
        <button class="nav-item" @click="logout">
          <i class="fas fa-sign-out-alt"></i>
          <span v-if="!isCollapsed">Sair</span>
        </button>
      </nav>
    </aside>

    <main class="main-content">
      <div class="top-bar">
        <h2>AgendaReino</h2>
        <div class="user-info" v-if="authStore.token">
          <span>{{ authStore.user?.nome || 'Usuário' }}</span>
        </div>
        <div v-else>
          <router-link to="/login" class="login-link">Entrar</router-link>
        </div>
      </div>
      <div class="calendar-container">
        <FullCalendar
          ref="fullCalendar"
          :options="calendarOptions"
        />
      </div>
    </main>

    <EventModal
      :visible="modalVisible"
      :eventId="selectedEventId"
      :eventType="selectedEventType"
      @close="modalVisible = false"
      @deleted="refreshEvents"
      @edit="openEditModal"
    />

    <EventFormModal
      :visible="formModalVisible"
      :eventId="editingEventId"
      :eventType="editingEventType"
      @close="formModalVisible = false"
      @saved="refreshEvents"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'

import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import EventModal from '@/components/EventModal.vue'
import EventFormModal from '@/components/EventFormModal.vue'

const router = useRouter()
const authStore = useAuthStore()
const fullCalendar = ref<any>(null)
const isCollapsed = ref(false)
const currentView = ref('dayGridMonth')
const isAdmin = computed(() => authStore.user?.tipo === 'admin')

// Estados para modais
const modalVisible = ref(false)
const selectedEventId = ref<number | null>(null)
const selectedEventType = ref<'normal' | 'recorrente' | null>(null)

const formModalVisible = ref(false)
const editingEventId = ref<number | null>(null)
const editingEventType = ref<'normal' | 'recorrente' | null>(null)

// Abrir modal de criação (novo evento)
const openCreateModal = () => {
  editingEventId.value = null
  editingEventType.value = null
  formModalVisible.value = true
}

// Abrir modal de edição (a partir do EventModal)
const openEditModal = (id: number, type: 'normal' | 'recorrente') => {
  editingEventId.value = id
  editingEventType.value = type
  formModalVisible.value = true
}

// Buscar eventos para o calendário
const fetchEvents = async (info: any) => {
  try {
    const startStr = info.start.toISOString().slice(0, 10)
    const endStr = info.end.toISOString().slice(0, 10)
    const response = await api.get(`/agenda?inicio=${startStr}&fim=${endStr}`)
    return response.data.map((ev: any) => ({
      title: ev.titulo,
      start: ev.data_inicio,
      end: ev.data_fim || ev.data_inicio,
      extendedProps: { id: ev.source_id, type: ev.source_type }
    }))
  } catch (error) {
    console.error(error)
    return []
  }
}

const calendarOptions = {
  plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
  locale: 'pt-br',
  headerToolbar: { left: '', center: '', right: '' },
  initialView: currentView.value,
  weekends: true,
  height: '100%',
  events: fetchEvents,
  eventClick: (info: any) => {
    const { id, type } = info.event.extendedProps
    selectedEventId.value = id
    selectedEventType.value = type
    modalVisible.value = true
  }
}

const changeView = (view: string) => {
  currentView.value = view
  const calendarApi = fullCalendar.value?.getApi()
  if (calendarApi) calendarApi.changeView(view)
}

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value

  setTimeout(() => {
    const calendarApi = fullCalendar.value?.getApi()
    if (calendarApi) {
      calendarApi.updateSize()
    }
  }, 300)
}

const refreshEvents = () => {
  const calendarApi = fullCalendar.value?.getApi()
  if (calendarApi) calendarApi.refetchEvents()
}

const goToProfile = () => {
  router.push('/perfil')
}

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
/* Layout geral estrutural */
.app-layout {
  display: flex;
  height: 100vh;
  width: 100%; /* Garante que ocupe a largura da janela inteira */
  overflow: hidden;
}

/* Sidebar - Responsável apenas pelo layout, as cores vêm do dark-theme.css */
.sidebar {
  transition: width 0.3s ease;
  width: 250px;
  flex-shrink: 0; /* Impede que a barra lateral seja espremida */
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
  z-index: 10;
  border-right: 1px solid #3a3a4a; /* Separação visual com a área principal */
}

.sidebar.collapsed {
  width: 70px;
}

.sidebar-header {
  display: flex;
  justify-content: flex-end;
  padding: 1rem;
}

.toggle-btn {
  background: none;
  border: none;
  color: inherit;
  font-size: 1.2rem;
  cursor: pointer;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem 0.5rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  background: none;
  border: none;
  color: inherit;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  width: 100%;
  text-align: left;
  transition: background 0.2s;
  white-space: nowrap; /* Evita que o texto quebre ao recolher a barra */
}

.nav-item i {
  width: 24px;
  text-align: center;
}

.nav-item:hover, .nav-item.active {
  background-color: rgba(255, 255, 255, 0.1); /* Efeito hover genérico */
}

.nav-divider {
  font-size: 0.7rem;
  text-transform: uppercase;
  color: #aaa;
  margin: 0.5rem 0 0.2rem 1rem;
  white-space: nowrap;
}

/* Área principal */
.main-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* O scroll deve ficar no calendário, não no main */
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem 1.5rem;
}

.top-bar h2 {
  margin: 0;
  font-size: 1.5rem;
}

.user-info {
  font-weight: bold;
}

.calendar-container {
  flex: 1;
  padding: 1rem;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* Nota: As customizações de cor do FullCalendar foram removidas daqui. 
   Certifique-se de que o arquivo dark-theme.css está sendo importado no seu projeto. */
</style>