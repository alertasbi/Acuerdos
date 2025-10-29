<template>
  <header
    class="fixed top-0 left-0 right-0 z-30 flex justify-between items-center bg-white border-b border-gray-200 px-6 py-3 shadow-sm"
  >
    <!-- Logo y usuario -->
    <div class="flex items-center gap-6">
      <!-- 🔗 Logo (ahora alineado a la izquierda absoluta) -->
      <NuxtLink
        to="/home"
        class="flex items-center absolute left-6 top-5 hover:opacity-90 transition"
      >
        <img
          src="~/assets/images/Logonew_smart2.png"
          alt="PriceTravel"
          class="w-44"
        />
      </NuxtLink>

      <!-- Espacio para usuario (desplazado por el logo) -->
      <div class="flex items-center gap-3 ml-56">
        <div class="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6 text-gray-600"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M5.121 17.804A9 9 0 1118.364 4.56a9 9 0 01-13.243 13.243z"
            />
          </svg>
        </div>
        <p class="font-semibold text-gray-700 text-base">Alan Cano</p>
      </div>
    </div>

    <!-- Botón cerrar sesión -->
    <button
      @click="onLogout"
      class="bg-gradient-to-r from-yellow-400 via-pink-600 via-purple-700 to-sky-500
             text-white font-semibold px-4 py-2 rounded-lg shadow-md hover:opacity-90 transition"
    >
      Cerrar sesión
    </button>
  </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()
const { logout } = useAuth()

const onLogout = () => {
  logout()
  router.push('/login')
}
</script>
