import { ref } from 'vue';

export const isDark = ref(true);

function applyTheme(dark: boolean) {
  const html = document.documentElement;
  html.setAttribute('data-theme', dark ? 'dark' : 'light');
  if (dark) {
    html.classList.add('dark');
  } else {
    html.classList.remove('dark');
  }
}

export function toggleTheme() {
  isDark.value = !isDark.value;
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light');
  applyTheme(isDark.value);
}

export function initTheme() {
  const saved = localStorage.getItem('theme');
  if (saved) {
    isDark.value = saved === 'dark';
  }
  applyTheme(isDark.value);
}
