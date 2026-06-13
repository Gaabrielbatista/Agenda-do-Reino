<template>
  <div class="flex h-screen w-screen overflow-hidden bg-page text-text-main">
    
    <!-- Mobile Overlay for Sidebar -->
    <div 
      v-if="!isCollapsedMobile" 
      class="fixed inset-0 bg-black/50 z-30 md:hidden" 
      @click="toggleSidebarMobile"
    ></div>

    <!-- Sidebar -->
    <aside 
      :class="[
        'absolute md:static top-0 left-0 h-full bg-sidebar border-r border-border z-40 transition-all duration-300 ease-in-out',
        'w-64 flex flex-col',
        isCollapsedMobile ? '-translate-x-full md:translate-x-0' : 'translate-x-0',
        { 'md:w-[80px]': isCollapsedDesktop }
      ]"
    >
      <div class="flex justify-end p-4">
        <!-- Desktop Toggle -->
        <button class="hidden md:block text-text-secondary hover:text-text-main" @click="toggleSidebarDesktop">
          <Bars3Icon v-if="isCollapsedDesktop" class="w-6 h-6" aria-hidden="true" />
          <ChevronLeftIcon v-else class="w-6 h-6" aria-hidden="true" />
        </button>
        <!-- Mobile Close -->
        <button class="md:hidden text-text-secondary hover:text-text-main" @click="toggleSidebarMobile">
          <ChevronLeftIcon class="w-6 h-6" aria-hidden="true" />
        </button>
      </div>

      <nav class="flex-1 px-3 py-4 space-y-1.5 overflow-x-hidden">
        <button 
          v-if="isAdmin" 
          class="flex items-center gap-3 w-full px-3 py-2.5 text-primary hover:bg-primary/10 rounded-lg transition-colors whitespace-nowrap"
          @click="openCreateModal"
        >
          <PlusCircleIcon class="w-6 h-6 shrink-0" aria-hidden="true" />
          <span v-if="!isCollapsedDesktop || !isDesktop" class="font-medium">Novo Evento</span>
        </button>

      </nav>

      <div class="p-3 border-t border-border flex flex-col gap-1.5">
        <button class="flex items-center gap-3 w-full px-3 py-2.5 text-text-main hover:bg-card rounded-lg transition-colors whitespace-nowrap" @click="goToProfile">
          <UserCircleIcon class="w-6 h-6 shrink-0" aria-hidden="true" />
          <span v-if="!isCollapsedDesktop || !isDesktop">Perfil</span>
        </button>
        <button class="flex items-center gap-3 w-full px-3 py-2.5 text-text-secondary hover:text-text-main hover:bg-card rounded-lg transition-colors whitespace-nowrap" @click="toggleTheme">
          <SunIcon v-if="isDark" class="w-6 h-6 shrink-0" aria-hidden="true" />
          <MoonIcon v-else class="w-6 h-6 shrink-0" aria-hidden="true" />
          <span v-if="!isCollapsedDesktop || !isDesktop">{{ isDark ? 'Tema Claro' : 'Tema Escuro' }}</span>
        </button>
        <button class="flex items-center gap-3 w-full px-3 py-2.5 text-text-main hover:bg-card rounded-lg transition-colors whitespace-nowrap" @click="logout">
          <ArrowRightOnRectangleIcon class="w-6 h-6 shrink-0" aria-hidden="true" />
          <span v-if="!isCollapsedDesktop || !isDesktop">Sair</span>
        </button>
      </div>
    </aside>

    <main class="flex-1 flex flex-col min-w-0">
      <!-- Top Bar -->
      <header class="flex items-center justify-between px-4 sm:px-8 py-4 bg-page border-b border-border">
        <div class="flex items-center gap-4">
          <button class="md:hidden text-text-secondary hover:text-text-main" @click="toggleSidebarMobile">
            <Bars3Icon class="w-6 h-6" aria-hidden="true" />
          </button>
        </div>

        <div class="flex-1 text-center sm:text-left">
          <h2 class="text-xl font-semibold tracking-wide text-text-main">AgendaReino</h2>
        </div>

        <div class="flex items-center">
          <div v-if="authStore.token" class="flex items-center gap-3 bg-card px-3 py-1.5 rounded-full border border-border shadow-sm">
            <UserCircleIcon class="w-5 h-5 text-primary" aria-hidden="true" />
            <span class="text-sm font-medium hidden sm:block text-text-main">{{ authStore.user?.nome || 'Usuário' }}</span>
            <span :class="['text-xs font-bold px-2.5 py-0.5 rounded-full', authStore.user?.tipo === 'admin' ? 'bg-primary/20 text-primary' : 'bg-emerald-500/20 text-emerald-400']">
              {{ authStore.user?.tipo === 'admin' ? 'Admin' : 'Membro' }}
            </span>
          </div>
          <div v-else>
            <router-link to="/login" class="text-primary hover:text-primary-hover font-medium">Entrar</router-link>
          </div>
        </div>
      </header>

      <!-- Calendar -->
      <div class="flex-1 px-0 sm:px-2 pb-0 sm:pb-2 overflow-hidden flex flex-col">
        <div class="bg-card flex-1 rounded-xl shadow-lg border border-border overflow-hidden flex flex-col">
          <div class="flex items-center justify-between px-3 sm:px-5 py-2.5 border-b border-border min-h-[52px]">
            <div class="flex items-center gap-1.5">
              <button class="calendar-nav-btn" @click="calendarPrev" title="Mês anterior">
                <ChevronLeftIcon class="w-5 h-5" />
              </button>
              <button class="calendar-nav-btn" @click="calendarNext" title="Próximo mês">
                <ChevronRightIcon class="w-5 h-5" />
              </button>
              <button class="calendar-today-btn" @click="calendarToday">Hoje</button>
              <h2 class="text-base sm:text-lg font-semibold text-text-main capitalize ml-2 whitespace-nowrap">{{ currentTitle }}</h2>
            </div>
            <div class="flex items-center gap-1">
              <button
                @click="changeView('dayGridMonth')"
                :class="['calendar-view-btn', currentView === 'dayGridMonth' ? 'active' : '']"
              >Mês</button>
              <button
                @click="changeView('timeGridWeek')"
                :class="['calendar-view-btn', currentView === 'timeGridWeek' ? 'active' : '']"
              >Semana</button>
              <button
                @click="changeView('timeGridDay')"
                :class="['calendar-view-btn', currentView === 'timeGridDay' ? 'active' : '']"
              >Dia</button>
            </div>
          </div>
          <div ref="calendarContainerRef" class="flex-1 p-1 sm:p-3">
            <FullCalendar ref="fullCalendar" :options="calendarOptions" class="h-full custom-calendar" />
          </div>
        </div>
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import type { CalendarOptions, EventInput } from '@fullcalendar/core'

import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import { isDark, toggleTheme } from '@/composables/useTheme'
import EventModal from '@/components/EventModal.vue'
import EventFormModal from '@/components/EventFormModal.vue'

import {
  Bars3Icon,
  ChevronLeftIcon,
  ChevronRightIcon,
  PlusCircleIcon,
  UserCircleIcon,
  ArrowRightOnRectangleIcon,
  SunIcon,
  MoonIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()
const fullCalendar = ref<any>(null)
const calendarContainerRef = ref<HTMLElement | null>(null)

// Sidebar state
const isCollapsedDesktop = ref(true)
const isCollapsedMobile = ref(true)
const isDesktop = ref(true)

const checkScreenSize = () => {
  isDesktop.value = window.innerWidth >= 768
  if (isDesktop.value) {
    isCollapsedMobile.value = true
  }
}

onMounted(() => {
  checkScreenSize()
  window.addEventListener('resize', checkScreenSize)
  calendarContainerRef.value?.addEventListener('wheel', handleCalendarWheel, { passive: false })
})

onUnmounted(() => {
  window.removeEventListener('resize', checkScreenSize)
  calendarContainerRef.value?.removeEventListener('wheel', handleCalendarWheel)
})

const currentView = ref('dayGridMonth')
const isAdmin = computed(() => authStore.user?.tipo === 'admin')

// Modals
const modalVisible = ref(false)
const selectedEventId = ref<number | null>(null)
const selectedEventType = ref<'normal' | 'recorrente' | null>(null)

const formModalVisible = ref(false)
const editingEventId = ref<number | null>(null)
const editingEventType = ref<'normal' | 'recorrente' | null>(null)

// Actions
const openCreateModal = () => {
  editingEventId.value = null
  editingEventType.value = null
  formModalVisible.value = true
  if (!isDesktop.value) isCollapsedMobile.value = true
}

const openEditModal = (id: number, type: 'normal' | 'recorrente') => {
  editingEventId.value = id
  editingEventType.value = type
  formModalVisible.value = true
}

const sourceTypeFallbackColors: Record<string, string> = {
  normal: '#3B82F6',
  recorrente: '#10B981'
}

const defaultEventColor = '#3B82F6'

const normalizeHexColor = (color: string): string | null => {
  const trimmed = color.trim()

  if (/^#[0-9A-Fa-f]{3}$/.test(trimmed)) {
    return `#${trimmed[1]}${trimmed[1]}${trimmed[2]}${trimmed[2]}${trimmed[3]}${trimmed[3]}`.toLowerCase()
  }

  if (/^#[0-9A-Fa-f]{6}$/.test(trimmed)) {
    return trimmed.toLowerCase()
  }

  return null
}

const hexToRgb = (hex: string): { r: number; g: number; b: number } | null => {
  const normalized = normalizeHexColor(hex)
  if (!normalized) return null

  const value = parseInt(normalized.slice(1), 16)
  return {
    r: (value >> 16) & 255,
    g: (value >> 8) & 255,
    b: value & 255
  }
}

const getContrastingTextColor = (): string => {
  return '#ffffff'
}

const resolveEventColor = (event: AgendaEvent): string => {
  const backendColor = normalizeHexColor(event.cor ?? event.cor_evento ?? '')
  if (backendColor) return backendColor

  return sourceTypeFallbackColors[event.source_type] ?? defaultEventColor
}

const isDarkTheme = () => document.documentElement.getAttribute('data-theme') !== 'light'

const lightenHex = (hex: string, amount: number): string => {
  const rgb = hexToRgb(hex)
  if (!rgb) return hex

  const toChannel = (channel: number) => Math.round(channel + (255 - channel) * amount)
  const toHex = (channel: number) => channel.toString(16).padStart(2, '0')

  return `#${toHex(toChannel(rgb.r))}${toHex(toChannel(rgb.g))}${toHex(toChannel(rgb.b))}`
}

const getEventThemeColor = (event: AgendaEvent): string => {
  const color = resolveEventColor(event)
  const rgb = hexToRgb(color)
  const isDark = isDarkTheme()

  if (!rgb) return isDark ? lightenHex(color, 0.18) : lightenHex(color, 0.40)

  const luminance = (0.299 * rgb.r + 0.587 * rgb.g + 0.114 * rgb.b) / 255

  if (luminance < 0.5) {
    return lightenHex(color, 0.30)
  }

  return isDark ? lightenHex(color, 0.18) : lightenHex(color, 0.40)
}

const buildCalendarEvent = (ev: AgendaEvent): EventInput => {
  const color = getEventThemeColor(ev)
  const sourceType = ev.source_type === 'recorrente' ? 'recorrente' : 'normal'
  const origColor = resolveEventColor(ev)
  const origRgb = hexToRgb(origColor)

  return {
    title: ev.titulo,
    start: ev.data_inicio,
    end: ev.data_fim || ev.data_inicio,
    backgroundColor: color,
    borderColor: color,
    textColor: getContrastingTextColor(),
    classNames: [`fc-event-${sourceType}`],
    extendedProps: {
      id: ev.source_id,
      type: sourceType,
      sourceType,
      sourceId: ev.source_id,
      exceptionId: ev.excecao_id ?? null,
      remarcado: ev.remarcado ?? false,
      _origR: origRgb?.r ?? 59,
      _origG: origRgb?.g ?? 130,
      _origB: origRgb?.b ?? 246
    }
  }
}

interface AgendaEvent {
  source_type: 'normal' | 'recorrente'
  source_id: number
  titulo: string
  descricao?: string | null
  data_inicio: string
  data_fim?: string | null
  status?: string
  criado_por?: number
  dia_semana?: number
  excecao_id?: number | null
  remarcado?: boolean
  cor?: string | null
  cor_evento?: string | null
}

const fetchEvents = async (info: any) => {
  try {
    const startStr = info.start.toISOString().slice(0, 10)
    const endStr = info.end.toISOString().slice(0, 10)
    const response = await api.get(`/agenda?inicio=${startStr}&fim=${endStr}`)
    return response.data.map((ev: AgendaEvent) => buildCalendarEvent(ev))
  } catch (error) {
    console.error(error)
    return []
  }
}

const currentTitle = ref('')
const prevViewStart = ref<string | null>(null)
let scrollThrottle: ReturnType<typeof setTimeout> | null = null

const handleCalendarWheel = (e: WheelEvent) => {
  if (scrollThrottle) return
  scrollThrottle = setTimeout(() => { scrollThrottle = null }, 600)

  e.preventDefault()

  const calendarApi = fullCalendar.value?.getApi()
  if (!calendarApi) return

  if (e.deltaY > 0) {
    calendarApi.next()
  } else {
    calendarApi.prev()
  }
}

const calendarPrev = () => {
  const api = fullCalendar.value?.getApi()
  if (api) api.prev()
}

const calendarNext = () => {
  const api = fullCalendar.value?.getApi()
  if (api) api.next()
}

const calendarToday = () => {
  const api = fullCalendar.value?.getApi()
  if (api) api.today()
}

const animateCalendarView = (direction: 'next' | 'prev') => {
  const harness = document.querySelector('.fc-view-harness') as HTMLElement
  if (!harness) return

  const offset = direction === 'next' ? 24 : -24

  harness.style.opacity = '0'
  harness.style.transform = `translateX(${offset}px)`

  harness.offsetHeight

  harness.style.transition = 'opacity 0.45s ease-out, transform 0.45s ease-out'
  harness.style.opacity = '1'
  harness.style.transform = 'translateX(0)'

  const onEnd = () => {
    harness.style.transition = ''
    harness.style.opacity = ''
    harness.style.transform = ''
    harness.removeEventListener('transitionend', onEnd)
  }
  harness.addEventListener('transitionend', onEnd)
}

const calendarOptions: CalendarOptions = {
  plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
  locale: 'pt-br',
  headerToolbar: false,
  titleFormat: { year: 'numeric', month: 'long' },
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
  datesSet: (info) => {
    const newStart = info.start.toISOString()
    if (prevViewStart.value) {
      const direction = newStart > prevViewStart.value ? 'next' : 'prev'
      animateCalendarView(direction)
    }
    prevViewStart.value = newStart
    currentTitle.value = info.view.title.replace(' de ', ' ')
  },
  eventClick: (info: any) => {
    const { id, type } = info.event.extendedProps
    selectedEventId.value = id
    selectedEventType.value = type
    modalVisible.value = true
  },
  eventDidMount: (info) => {
    const el = info.el as HTMLElement

    if (el.classList.contains('fc-daygrid-dot-event')) {
      el.style.backgroundColor = info.event.backgroundColor || ''
      if (info.event.textColor) {
        el.style.color = info.event.textColor
      }
      return
    }

    const bgColor = info.event.backgroundColor || '#3B82F6'
    const rgb = hexToRgb(bgColor)
    if (!rgb) return

    const { _origR, _origG, _origB } = info.event.extendedProps
    const lightColor = lightenHex(bgColor, 0.3)

    el.style.setProperty('--evt-bg', bgColor)
    el.style.setProperty('--evt-bg-light', lightColor)
    el.style.setProperty('--evt-r', String(_origR ?? rgb.r))
    el.style.setProperty('--evt-g', String(_origG ?? rgb.g))
    el.style.setProperty('--evt-b', String(_origB ?? rgb.b))

    el.style.background = `linear-gradient(135deg, ${lightColor}, ${bgColor})`
    el.style.borderColor = 'transparent'
    el.style.borderRadius = '12px'
    el.style.padding = '0.6rem 0.9rem'
    el.style.color = info.event.textColor || getContrastingTextColor()
    el.style.boxShadow = `
      inset 0 0 4px rgba(255,255,255,0.2),
      0 0 12px 4px rgba(var(--evt-r), var(--evt-g), var(--evt-b), 0.5),
      0 0 6px rgba(255,255,255,0.25)
    `
    el.style.position = 'relative'
    el.style.zIndex = '0'
    el.style.transition = 'transform 0.28s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.28s ease, filter 0.28s ease'
    el.style.overflow = 'visible'
  },
  eventContent: (arg) => {
    if (!arg.timeText) return
    return {
      html: `<div class="fc-event-time">
        <svg class="evt-clock-icon" viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"/>
          <polyline points="12,6 12,12 16,14"/>
        </svg>
        ${arg.timeText}
      </div>
      <div class="fc-event-title">${arg.event.title}</div>`
    }
  }
}

const changeView = (view: string) => {
  currentView.value = view
  const calendarApi = fullCalendar.value?.getApi()
  if (calendarApi) calendarApi.changeView(view)
  if (!isDesktop.value) isCollapsedMobile.value = true
}

const toggleSidebarDesktop = () => {
  isCollapsedDesktop.value = !isCollapsedDesktop.value
  setTimeout(() => {
    const calendarApi = fullCalendar.value?.getApi()
    if (calendarApi) calendarApi.updateSize()
  }, 300)
}

const toggleSidebarMobile = () => {
  isCollapsedMobile.value = !isCollapsedMobile.value
}

const refreshEvents = () => {
  const calendarApi = fullCalendar.value?.getApi()
  if (calendarApi) calendarApi.refetchEvents()
}

const goToProfile = () => {
  router.push('/perfil')
  if (!isDesktop.value) isCollapsedMobile.value = true
}

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
/* FullCalendar - Estilos Customizados para o Redesign Dark */

:deep(.fc-theme-standard td), 
:deep(.fc-theme-standard th),
:deep(.fc-theme-standard .fc-scrollgrid) {
  border-color: var(--border);
}

:deep(.fc-col-header-cell) {
  padding: 0.75rem 0;
  background-color: transparent;
}

:deep(.fc-col-header-cell-cushion) {
  color: var(--text-secondary);
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
}

:deep(.fc-daygrid-day-number) {
  color: var(--text-secondary);
  padding: 0.5rem;
  font-size: 0.9rem;
}

:deep(.fc-daygrid-day.fc-day-today) {
  background-color: color-mix(in srgb, var(--primary) 8%, transparent) !important;
}

:deep(.fc-daygrid-day:hover) {
  background-color: var(--hover-bg) !important;
  transition: background-color 0.2s ease;
}

.calendar-nav-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 0.5rem;
  border: 1px solid var(--border);
  background-color: transparent;
  color: var(--text-main);
  cursor: pointer;
  transition: background-color 0.2s;
}

.calendar-nav-btn:hover {
  background-color: var(--border);
}

.calendar-today-btn {
  padding: 0.25rem 0.75rem;
  border-radius: 0.5rem;
  border: 1px solid var(--border);
  background-color: transparent;
  color: var(--text-main);
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  white-space: nowrap;
}

.calendar-today-btn:hover {
  background-color: var(--border);
}

.calendar-view-btn {
  padding: 0.3rem 0.75rem;
  border-radius: 0.5rem;
  border: 1px solid var(--border);
  background-color: transparent;
  color: var(--text-secondary);
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.calendar-view-btn:hover {
  background-color: var(--border);
  color: var(--text-main);
}

.calendar-view-btn.active {
  background-color: var(--card);
  color: var(--primary);
  border-color: var(--border);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

@media (max-width: 640px) {
  .calendar-view-btn {
    padding: 0.25rem 0.5rem;
    font-size: 0.78rem;
  }
}

/* ═══════════════════════════════════════════
   Custom Scrollbar — Dark Theme
   ═══════════════════════════════════════════ */

:deep(.fc-scroller) {
  scrollbar-width: thin;
  scrollbar-color: var(--border) transparent;
}

:deep(.fc-scroller::-webkit-scrollbar) {
  width: 6px;
  height: 6px;
}

:deep(.fc-scroller::-webkit-scrollbar-track) {
  background: transparent;
}

:deep(.fc-scroller::-webkit-scrollbar-thumb) {
  background-color: var(--border);
  border-radius: 999px;
  border: 1px solid transparent;
  background-clip: content-box;
}

:deep(.fc-scroller::-webkit-scrollbar-thumb:hover) {
  background-color: var(--text-secondary);
}

:deep(.fc-scroller::-webkit-scrollbar-corner) {
  background: transparent;
}

/* ═══════════════════════════════════════════
   Neon Glow Effect — 3-Layer Light System
   ═══════════════════════════════════════════ */

/* Event outer container */
:deep(.fc-event) {
  border-radius: 12px !important;
  overflow: visible !important;
}

/* Inner wrapper — time on top, title below */
:deep(.fc-event-main) {
  display: flex !important;
  flex-direction: column !important;
  align-items: stretch !important;
  gap: 0.15rem;
}

/* Fix FC's border-radius reset for middle events in month view */
:deep(.fc-daygrid-block-event:not(.fc-event-start)) {
  border-top-left-radius: 12px !important;
  border-bottom-left-radius: 12px !important;
  border-left-width: 1px !important;
  border-left-color: transparent !important;
}

:deep(.fc-daygrid-block-event:not(.fc-event-end)) {
  border-top-right-radius: 12px !important;
  border-bottom-right-radius: 12px !important;
}

/* Layer 2: Ambient glow via pseudo-element — event-colored */
:deep(.fc-event::before) {
  content: '';
  position: absolute;
  inset: -6px;
  border-radius: 16px;
  background: radial-gradient(ellipse, rgba(var(--evt-r), var(--evt-g), var(--evt-b), 0.4), transparent 65%);
  opacity: 0.6;
  filter: blur(10px);
  z-index: -1;
  pointer-events: none;
  transition: opacity 0.28s ease, filter 0.28s ease;
}

/* ═══ Hover ═══ */
:deep(.fc-event:hover) {
  transform: scale(1.02) !important;
  filter: brightness(1.04) !important;
  box-shadow:
    inset 0 0 6px rgba(255,255,255,0.3),
    0 0 16px 6px rgba(var(--evt-r), var(--evt-g), var(--evt-b), 0.45),
    0 0 10px rgba(255,255,255,0.3) !important;
}

:deep(.fc-event:hover::before) {
  opacity: 0.7 !important;
  filter: blur(12px) !important;
}

/* ═══ Typography ═══ */
:deep(.fc-event-title) {
  font-weight: 600;
  font-size: 1rem;
  line-height: 1.35;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  min-width: 0;
}

:deep(.fc-event-time) {
  font-size: 0.85rem;
  font-weight: 700;
  white-space: nowrap;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  opacity: 0.9;
  line-height: 1.25;
  display: inline-flex;
  align-items: center;
  gap: 0.2rem;
}

/* Clock icon inside event time */
:deep(.evt-clock-icon) {
  display: inline-block;
  vertical-align: middle;
  flex-shrink: 0;
  opacity: 0.8;
}

:deep(.fc-daygrid-event-dot) {
  display: none;
}

:deep(.fc-daygrid-day-frame) {
  min-height: 110px !important;
}

/* Week / day view — timegrid event */
:deep(.fc-timegrid-event) {
  border-radius: 8px !important;
  padding: 0.35rem 0.5rem !important;
}

:deep(.fc-timegrid-event .fc-event-main) {
  gap: 0.1rem;
}

:deep(.fc-timegrid-event .fc-event-time) {
  font-size: 0.75rem;
  font-weight: 700;
  white-space: nowrap;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  opacity: 0.9;
}

:deep(.fc-timegrid-event .fc-event-title) {
  font-size: 0.85rem;
  font-weight: 600;
}

:deep(.fc-timegrid-col-events) {
  padding: 0 !important;
  margin: 0 !important;
}

:deep(.fc-timegrid-slot) {
  height: 48px !important;
}

:deep(.fc-daygrid-event) {
  width: 97% !important;
  margin: 4px auto !important;
}

/* ═══ Responsive — smaller screens ═══ */
@media (max-width: 640px) {
  :deep(.fc-event-title) {
    font-size: 0.85rem;
  }
  :deep(.fc-event-time) {
    font-size: 0.75rem;
  }
  :deep(.fc-daygrid-event) {
    width: 95% !important;
    margin: 3px auto !important;
  }
  :deep(.fc-timegrid-slot) {
    height: 40px !important;
  }
  :deep(.fc-daygrid-day-frame) {
    min-height: 90px !important;
  }
}
</style>