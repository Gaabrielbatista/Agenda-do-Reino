<template>
  <div class="app-layout">
    <aside :class="['sidebar', { collapsed: isCollapsed }]">
      <div class="sidebar-header">
        <button class="toggle-btn" @click="toggleSidebar">
          <i :class="isCollapsed ? 'fas fa-bars' : 'fas fa-chevron-left'"></i>
        </button>
      </div>
      <nav class="sidebar-nav">
        <button v-if="isAdmin" class="nav-item" @click="openCreateModal">
          <i class="fas fa-calendar-plus"></i>
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
      </nav>

      <div class="sidebar-footer">
        <button class="nav-item" @click="goToProfile">
          <i class="fas fa-user-circle"></i>
          <span v-if="!isCollapsed">Perfil</span>
        </button>
        <button class="nav-item" @click="logout">
          <i class="fas fa-arrow-right-from-bracket"></i>
          <span v-if="!isCollapsed">Sair</span>
        </button>
      </div>
    </aside>

    <main class="main-content">
      <div class="top-bar">
        <div class="top-bar-left">
          <button @click="toggleTheme" class="theme-toggle-btn">
            <i :class="isDark ? 'fas fa-moon' : 'fas fa-sun'"></i>
          </button>
        </div>
        <div class="top-bar-center">
          <h2>AgendaReino</h2>
        </div>
        <div class="top-bar-right">
          <div v-if="authStore.token" class="user-info-top">
            <i class="fas fa-user-circle"></i>
            <span>{{ authStore.user?.nome || 'Usuário' }}</span>
            <span class="user-role-badge" :class="authStore.user?.tipo === 'admin' ? 'admin' : 'membro'">
              {{ authStore.user?.tipo === 'admin' ? 'Admin' : 'Membro' }}
            </span>
          </div>
          <div v-else>
            <router-link to="/login" class="login-link">Entrar</router-link>
          </div>
        </div>
      </div>
      <div class="calendar-container">
        <FullCalendar ref="fullCalendar" :options="calendarOptions" />
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import type { CalendarOptions } from '@fullcalendar/core'

import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import EventModal from '@/components/EventModal.vue'
import EventFormModal from '@/components/EventFormModal.vue'

import { isDark, toggleTheme } from '@/composables/useTheme'

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

// Funções de apoio
const openCreateModal = () => {
  editingEventId.value = null
  editingEventType.value = null
  formModalVisible.value = true
}

const openEditModal = (id: number, type: 'normal' | 'recorrente') => {
  editingEventId.value = id
  editingEventType.value = type
  formModalVisible.value = true
}

const fetchEvents = async (info: any) => {
  try {
    const startStr = info.start.toISOString().slice(0, 10)
    const endStr = info.end.toISOString().slice(0, 10)
    const response = await api.get(`/agenda?inicio=${startStr}&fim=${endStr}`)
    return response.data.map((ev: any) => ({
      title: ev.titulo,
      start: ev.data_inicio,
      end: ev.data_fim || ev.data_inicio,
      classNames: [ev.source_type === 'normal' ? 'fc-event-normal' : 'fc-event-recurring'],
      extendedProps: { id: ev.source_id, type: ev.source_type }
    }))
  } catch (error) {
    console.error(error)
    return []
  }
}

const calendarOptions: CalendarOptions = {
  plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
  locale: 'pt-br',
  headerToolbar: { left: '', center: '', right: '' },
  initialView: currentView.value,
  weekends: true,
  height: '100%',
  eventTimeFormat: {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
    omitZeroMinute: false
  } as const,
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
/* Layout Estrutural Principal */
.app-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background-color: var(--bg-page);
  color: var(--text-primary);
  transition: background-color 0.3s, color 0.3s;
}

/* Sidebar */
.sidebar {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: width 0.3s ease, background-color 0.3s;
  width: 250px;
  flex-shrink: 0;
  background-color: var(--bg-sidebar);
  border-right: 1px solid var(--border-color);
  z-index: 10;
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
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem 0.5rem;
  overflow-x: hidden;
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
  white-space: nowrap;
}

.nav-item i {
  width: 24px;
  text-align: center;
}

.nav-item:hover, .nav-item.active {
  background-color: var(--hover-bg);
}

.nav-divider {
  font-size: 0.7rem;
  text-transform: uppercase;
  color: var(--text-secondary);
  margin: 0.5rem 0 0.2rem 1rem;
  white-space: nowrap;
}

.sidebar-footer {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem 0.5rem;
  border-top: 1px solid var(--border-color);
}

/* Área Principal e Top Bar */
.main-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem 1.5rem;
  background-color: var(--bg-topbar);
  border-bottom: 1px solid var(--border-color);
  transition: background-color 0.3s;
}

.top-bar-left {
  width: 100px;
  display: flex;
  justify-content: flex-start;
}

.top-bar-center {
  flex: 1;
  text-align: center;
}

.top-bar-center h2 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  color: var(--text-primary);
}

.top-bar-right {
  width: auto;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info-top {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: rgba(128, 128, 128, 0.1);
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
}

.user-info-top i {
  font-size: 1.2rem;
  color: var(--btn-primary);
}

.user-role-badge {
  font-size: 0.7rem;
  font-weight: bold;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
}

.user-role-badge.admin {
  background-color: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
}

.user-role-badge.membro {
  background-color: rgba(16, 185, 129, 0.2);
  color: #34d399;
}

/* Melhorando o botão de alternar tema */
.theme-toggle-btn {
  background: var(--bg-sidebar);
  border: 1px solid var(--border-color);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  cursor: pointer;
  color: var(--text-primary);
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s, transform 0.2s;
}

.theme-toggle-btn:hover {
  background: var(--hover-bg);
}

/* Container do Calendário */
.calendar-container {
  flex: 1;
  padding: 1rem;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* FullCalendar — estilo de cartões para eventos dayGrid */
:deep(.fc-daygrid-event) {
  display: block;
  width: calc(100% - 0.25rem);
  padding: 4px 8px;
  margin: 0.12rem 0;
  border-radius: 0.75rem;
  color: #ffffff;
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: transform 0.18s ease, filter 0.18s ease, box-shadow 0.18s ease;
  overflow: hidden;
}

:deep(.fc-daygrid-event.fc-event-recurring) {
  background-color: var(--btn-primary);
}

:deep(.fc-daygrid-event.fc-event-normal) {
  background-color: #10b981;
}

:deep(.fc-daygrid-event:hover),
:deep(.fc-daygrid-event:focus) {
  transform: translateY(-1px) scale(1.01);
  filter: brightness(1.08);
  box-shadow: 0 14px 30px rgba(0, 0, 0, 0.18);
}

:deep(.fc-daygrid-event .fc-event-title),
:deep(.fc-daygrid-event .fc-event-title-container) {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  line-height: 1.25;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #ffffff;
}

:deep(.fc-daygrid-event .fc-event-time) {
  display: block;
  margin-top: 0.12rem;
  font-size: 0.75rem;
  opacity: 0.92;
  color: rgba(255, 255, 255, 0.94);
}

:deep(.fc-daygrid-event-dot),
:deep(.fc-event-dot) {
  display: none;
}

:deep(.fc-daygrid-event-harness) {
  width: 100%;
}

.nav-item .fa-right-from-bracket {
  color: var(--text-primary);
}
</style>