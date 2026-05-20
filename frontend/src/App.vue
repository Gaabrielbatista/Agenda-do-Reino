<template>
  <div>
    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
if (authStore.token) {
  import('@/services/api').then(module => {
    module.default.defaults.headers.common['Authorization'] = `Bearer ${authStore.token}`
  })
}
</script>