<script setup lang="ts">
import { initTheme } from '@/composables/useTheme'
import { useToast } from '@/composables/useToast'
import ToastNotification from '@/components/ToastNotification.vue'

initTheme()
const { toasts, removeToast } = useToast()
</script>

<template>
  <router-view />
  <div class="toast-wrapper">
    <ToastNotification
      v-for="toast in toasts"
      :key="toast.id"
      :id="toast.id"
      :message="toast.message"
      :type="toast.type"
      @close="removeToast(toast.id)"
    />
  </div>
</template>

<style>
.toast-wrapper {
  position: fixed;
  top: 70px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  z-index: 11000;
  align-items: flex-end;
}
</style>