<script setup lang="ts">
import { initTheme } from '@/composables/useTheme'
import { useToast } from '@/composables/useToast'
import ToastNotification from '@/components/ToastNotification.vue'

initTheme()
const { toasts, removeToast } = useToast()
</script>

<template>
  <router-view />
  <div class="fixed top-20 right-5 flex flex-col gap-3 z-[11000] items-end pointer-events-none">
    <ToastNotification
      v-for="toast in toasts"
      :key="toast.id"
      :id="toast.id"
      :message="toast.message"
      :type="toast.type"
      @close="removeToast(toast.id)"
      class="pointer-events-auto"
    />
  </div>
</template>