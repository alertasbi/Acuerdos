export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: ['~/assets/css/tailwind.css'],

  postcss: {
    plugins: {
      '@tailwindcss/postcss': {},
      autoprefixer: {},
    },
  },

  // 👇 Añade esto:
  app: {
    head: {
      link: [
        { rel: 'preload', as: 'style', href: '/_nuxt/assets/css/tailwind.css' }
      ],
    },
  },
})
