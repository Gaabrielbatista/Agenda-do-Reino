<template>
  <div 
    class="flex items-center gap-3 max-w-xs p-4 rounded-xl shadow-2xl backdrop-blur-md cursor-pointer transition-all duration-200 hover:-translate-y-0.5 border"
    :class="[
      type === 'success' 
        ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' 
        : 'bg-red-500/10 border-red-500/30 text-red-400'
    ]"
    @click="closeToast"
  >
    <component :is="iconComponent" class="w-6 h-6 shrink-0" aria-hidden="true" />
    <div class="flex-1">
      <p class="m-0 text-sm font-medium text-text-main leading-snug">{{ message }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { CheckCircleIcon, ExclamationTriangleIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  id: { type: Number, required: true },
  message: { type: String, required: true },
  type: { type: String as () => 'success' | 'error', default: 'success' },
  duration: { type: Number, default: 3500 },
})

const iconComponent = computed(
  () => (props.type === 'error' ? ExclamationTriangleIcon : CheckCircleIcon)
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
