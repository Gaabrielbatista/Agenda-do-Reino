import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import CalendarView from '@/views/CalendarView.vue'
import PerfilView from '@/views/PerfilView.vue'
import ExcecoesView from '@/views/ExcecoesView.vue'
import { useAuthStore } from '@/stores/auth'

const routes = [
  { path: '/login', name: 'login', component: LoginView, meta: { requiresAuth: false } },
  { path: '/', name: 'calendar', component: CalendarView, meta: { requiresAuth: false } },
  { path: '/perfil', name: 'perfil', component: PerfilView, meta: { requiresAuth: true } },
  { path: '/evento/recorrente/:id/excecoes', name: 'excecoes', component: ExcecoesView, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = !!authStore.token

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router