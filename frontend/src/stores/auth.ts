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
    user: null as Usuario | null,
    token: localStorage.getItem('token') || null
  }),
  actions: {
    async login(email: string, senha: string): Promise<boolean> {
      try {
        const response = await api.post('/auth/login', { email, senha })
        this.token = response.data.token
        this.user = response.data.usuario
        localStorage.setItem('token', this.token!)
        api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        return true
      } catch (error) {
        console.error('Erro no login:', error)
        return false
      }
    },
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
      delete api.defaults.headers.common['Authorization']
    }
  }
})