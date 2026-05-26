import { ref, onMounted } from 'vue';

// Reactive flag for dark mode
export const isDark = ref(false);

/**
 * Apply the theme class to the body and set data-theme attribute.
 * Also updates CSS variables by loading the appropriate stylesheet.
 */
function applyTheme(dark: boolean) {
  const body = document.body;
  const html = document.documentElement;
  if (dark) {
    body.classList.add('dark-theme');
    body.classList.remove('light-theme');
    html.setAttribute('data-theme', 'dark');
    // Load dark CSS if not already loaded
    const linkId = 'theme-dark';
    if (!document.getElementById(linkId)) {
      const link = document.createElement('link');
      link.id = linkId;
      link.rel = 'stylesheet';
      link.href = '/src/assets/themes/dark.css';
      document.head.appendChild(link);
    }
  } else {
    body.classList.remove('dark-theme');
    body.classList.add('light-theme');
    html.setAttribute('data-theme', 'light');
    const linkId = 'theme-light';
    if (!document.getElementById(linkId)) {
      const link = document.createElement('link');
      link.id = linkId;
      link.rel = 'stylesheet';
      link.href = '/src/assets/themes/light.css';
      document.head.appendChild(link);
    }
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

// Auto‑initialize when the app starts
onMounted(() => {
  initTheme();
});
