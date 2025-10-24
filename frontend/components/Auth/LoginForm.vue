<template>
  <div
    class="w-full max-w-lg bg-white/85 backdrop-blur-md p-12 rounded-3xl shadow-2xl border border-white/40"
  >
    <form @submit.prevent="handleLogin" class="space-y-8">
      <!-- Usuario -->
      <div>
        <label for="email" class="block text-sm font-semibold text-gray-700 mb-2">
          Usuario
        </label>
        <input
          id="email"
          v-model="username"
          type="email"
          placeholder="@pricetravel.com.mx"
          required
          class="w-full border border-gray-200 rounded-lg px-4 py-3 text-gray-800 shadow-sm focus:ring-2 focus:ring-blue-600 focus:border-transparent transition"
        />
      </div>

      <!-- Contraseña -->
      <div>
        <label for="password" class="block text-sm font-semibold text-gray-700 mb-2">
          Contraseña
        </label>
        <input
          id="password"
          v-model="password"
          type="password"
          placeholder="••••••••"
          required
          class="w-full border border-gray-200 rounded-lg px-4 py-3 text-gray-800 shadow-sm focus:ring-2 focus:ring-blue-600 focus:border-transparent transition"
        />
      </div>

      <!-- Botón -->
      <button
        type="submit"
        class="w-full py-3.5 rounded-lg font-semibold text-white shadow-md text-lg
               bg-gradient-to-r from-yellow-400 via-pink-600 via-purple-700 to-sky-500
               hover:from-yellow-500 hover:via-pink-700 hover:via-purple-800 hover:to-sky-600
               transition-all duration-300 ease-in-out transform hover:scale-[1.03] active:scale-[0.98]"
      >
        Iniciar sesión
      </button>

      <!-- Mensaje de error -->
      <p
        v-if="errorMsg"
        class="text-red-500 text-sm text-center mt-2 animate-pulse"
      >
        {{ errorMsg }}
      </p>
    </form>
  </div>
</template>

<script setup lang="ts">
const username = ref('')
const password = ref('')
const errorMsg = ref('')
const router = useRouter()

const handleLogin = () => {
  if (username.value === 'admin@pricetravel.com.mx' && password.value === '1234') {
    errorMsg.value = '' // limpia el mensaje
    router.push('/home') // ✅ redirige a Home
  } else {
    errorMsg.value = 'Usuario o contraseña incorrectos.' // ⛔ muestra mensaje rojo
  }
}
</script>
