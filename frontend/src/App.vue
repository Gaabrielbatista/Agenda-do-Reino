<script setup lang="ts">
import { onMounted } from 'vue'
import { initTheme } from '@/composables/useTheme'

onMounted(() => {
  initTheme()
})
</script>

<template>
  <router-view />
</template>

<style>
/* Se houver algum estilo antigo aqui, pode limpar se já estiver nos arquivos base.css */
</style>