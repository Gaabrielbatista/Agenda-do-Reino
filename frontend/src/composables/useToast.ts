import { reactive, readonly } from 'vue'

type ToastType = 'success' | 'error'

export interface ToastItem {
  id: number
  message: string
  type: ToastType
}

const state = reactive({
  toasts: [] as ToastItem[],
})

let nextToastId = 1

function removeToast(id: number) {
  const index = state.toasts.findIndex((toast) => toast.id === id)
  if (index !== -1) state.toasts.splice(index, 1)
}

function addToast(message: string, type: ToastType = 'success') {
  const toast: ToastItem = {
    id: nextToastId++,
    message,
    type,
  }
  state.toasts.push(toast)
  return toast.id
}

export function useToast() {
  return {
    toasts: readonly(state.toasts),
    notifySuccess(message: string) {
      addToast(message, 'success')
    },
    notifyError(message: string) {
      addToast(message, 'error')
    },
    removeToast,
  }
}
