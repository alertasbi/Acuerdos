<template>
    <section
    class="min-h-screen flex flex-col justify-between items-center bg-gradient-to-b from-gray-50 to-gray-100 transition-opacity duration-500 opacity-0"
    v-show="mounted"
    >
    <!-- Header con logo -->
    <header class="mt-24 sm:mt-32 text-center space-y-6">
      <img
        src="../assets/images/Logonew_smart2.png"
        alt="PriceTravel"
        class="w-48 sm:w-64 md:w-72 mx-auto"
      />
      <h1 class="text-2xl sm:text-3xl font-semibold text-gray-700 tracking-wide">
        Acceso Página Acuerdos
      </h1>
    </header>

    <!-- Formulario centrado (más arriba ahora) -->
    <main class="flex justify-center items-center w-full px-4 -mt-10 sm:-mt-16">
      <LoginForm />
    </main>

    <!-- Footer con barra de colores -->
    <footer class="relative w-full mt-10">
      <div class="relative">
        <img
          src="../assets/images/lineaPriceTravelNew.jpg"
          alt="Decoración PriceTravel"
          class="w-full h-8 sm:h-10 object-cover"
        />
        <p
          class="absolute inset-0 flex items-center justify-center text-white text-xs sm:text-sm font-medium tracking-wide"
        >
          © 2025 PriceTravel, todos los derechos reservados.
        </p>
      </div>
    </footer>
  </section>
</template>

<script setup lang="ts">
import LoginForm from '~/components/Auth/LoginForm.vue'
const mounted = ref(false)
onMounted(() => {
  mounted.value = true
})

</script>
