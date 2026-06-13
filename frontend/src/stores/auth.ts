import { defineStore } from 'pinia'
import api from '@/services/api'

interface Usuario {
  id: number
  nome: string
  email: string
  tipo: 'admin' | 'membro' | 'visitante'
}

const readStoredUser = (): Usuario | null => {
  const user = localStorage.getItem('user')
  if (!user) return null

  try {
    return JSON.parse(user) as Usuario
  } catch {
    localStorage.removeItem('user')
    return null
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: readStoredUser(),
    token: localStorage.getItem('token') || null
  }),
  getters: {
    isAuthenticated: (state) => !!state.token
  },
  actions: {
    async login(email: string, senha: string): Promise<boolean> {
      try {
        const response = await api.post('/auth/login', { email, senha })
        const token = response.data.token
        const user = response.data.usuario
        if (token && user) {
          this.setAuth(token, user)
          return true
        }
        return false
      } catch (error) {
        console.error('Login error:', error instanceof Error ? error.message : error)
        return false
      }
    },
    setAuth(token: string, user: Usuario) {
      this.token = token
      this.user = user
      localStorage.setItem('user', JSON.stringify(user))
      localStorage.setItem('token', token)
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`
    },
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      delete api.defaults.headers.common['Authorization']
    }
  }
})