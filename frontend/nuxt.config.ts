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

  // 🔥 AGREGA ESTO – ACTIVA PINIA
  modules: [
    '@pinia/nuxt',
  ],

  pinia: {
    autoImports: ['defineStore'],
  },

  app: {
    head: {
      link: [
        { rel: 'preload', as: 'style', href: '/_nuxt/assets/css/tailwind.css' }
      ],
    },
  },
})
