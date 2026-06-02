<template>
  <div class="toast-notification" :class="type" @click="closeToast">
    <i :class="['toast-icon', iconClass]" aria-hidden="true"></i>
    <div class="toast-content">
      <p class="toast-message">{{ message }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'

const props = defineProps({
  id: { type: Number, required: true },
  message: { type: String, required: true },
  type: { type: String as () => 'success' | 'error', default: 'success' },
  duration: { type: Number, default: 3500 },
})

const iconClass = computed(() =>
  props.type === 'error'
    ? 'fas fa-exclamation-triangle'
    : 'fas fa-check-circle'
)

const emit = defineEmits<{
  (event: 'close'): void
}>()

onMounted(() => {
  window.setTimeout(() => emit('close'), props.duration)
})

const closeToast = () => {
  emit('close')
}
</script>

<style scoped>
.toast-notification {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  max-width: 320px;
  padding: 1.1rem 1.3rem;
  border-radius: 14px;
  box-shadow: 0 18px 45px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(10px);
  cursor: pointer;
  transition: transform 0.2s ease, opacity 0.2s ease;
  opacity: 0.98;
}

.toast-notification:hover {
  transform: translateY(-1px);
}

.toast-icon {
  font-size: 1rem;
}

.toast-content {
  flex: 1;
}

.toast-message {
  margin: 0;
  font-size: 1rem;
  line-height: 1.4;
  color: var(--text-primary);
}

.toast-notification.success {
  background: rgba(56, 189, 248, 0.12);
  border: 1px solid rgba(56, 189, 248, 0.3);
}

.toast-notification.error {
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid rgba(239, 68, 68, 0.3);
}

body.dark-theme .toast-notification.success {
  background: rgba(16, 185, 129, 0.18);
  border-color: rgba(16, 185, 129, 0.35);
}

body.dark-theme .toast-notification.error {
  background: rgba(248, 113, 113, 0.18);
  border-color: rgba(248, 113, 113, 0.35);
}

body.dark-theme .toast-message {
  color: var(--text-primary);
}
</style>
