/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        page: 'var(--page)',
        card: 'var(--card)',
        sidebar: 'var(--sidebar)',
        primary: 'var(--primary)',
        'primary-hover': 'var(--primary-hover)',
        'accent-warm': 'var(--accent-warm)',
        'accent-cool': 'var(--accent-cool)',
        success: 'var(--success)',
        danger: 'var(--danger)',
        border: 'var(--border)',
        text: {
          main: 'var(--text-main)',
          secondary: 'var(--text-secondary)'
        }
      }
    },
  },
  plugins: [],
}
