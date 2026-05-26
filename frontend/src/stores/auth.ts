import { defineStore } from 'pinia'
import api from '@/services/api'

interface Usuario {
  id: number
  nome: string
  email: string
  tipo: 'admin' | 'membro'
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: (localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user') as string) : null) as Usuario | null,
    token: localStorage.getItem('token') || null
  }),
  actions: {
    async login(email: string, senha: string): Promise<boolean> {
      try {
        const response = await api.post('/auth/login', { email, senha })
        const token = response.data.token
        const user = response.data.usuario
        if (token && user) {
          this.token = token
          this.user = user
          localStorage.setItem('user', JSON.stringify(user))
          localStorage.setItem('token', token)
          return true
        }
        return false
      } catch (error: any) {
        console.error('Login error:', error.response?.data || error.message)
        return false
      }
    },
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }
})