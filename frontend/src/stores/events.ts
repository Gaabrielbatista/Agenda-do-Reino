import { defineStore } from 'pinia'
import api from '@/services/api'

export const useEventsStore = defineStore('events', {
  state: () => ({
    normalEvents: [],
    recurringEvents: []
  }),
  actions: {
    async fetchNormalEvents() {
      const response = await api.get('/eventos/normais')
      this.normalEvents = response.data
    },
    async fetchRecurringEvents() {
      const response = await api.get('/eventos/recorrentes')
      this.recurringEvents = response.data
    },
    async createEvent(data: any, type: 'normal' | 'recorrente') {
      const endpoint = type === 'normal' ? '/eventos/normais' : '/eventos/recorrentes'
      const response = await api.post(endpoint, data)
      return response.data
    }
    // ... outros métodos (update, delete, exceptions)
  }
})