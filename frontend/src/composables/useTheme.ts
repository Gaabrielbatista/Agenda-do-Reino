import { ref } from 'vue';

export const isDark = ref(false);

function applyTheme(dark: boolean) {
  const body = document.body;
  const html = document.documentElement;
  if (dark) {
    body.classList.add('dark-theme');
    body.classList.remove('light-theme');
    html.setAttribute('data-theme', 'dark');
  } else {
    body.classList.remove('dark-theme');
    body.classList.add('light-theme');
    html.setAttribute('data-theme', 'light');
  }
}

export function toggleTheme() {
  isDark.value = !isDark.value;
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light');
  applyTheme(isDark.value);
}

export function initTheme() {
  const saved = localStorage.getItem('theme');
  isDark.value = saved === 'dark';
  applyTheme(isDark.value);
}
