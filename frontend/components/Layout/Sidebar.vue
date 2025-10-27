<template>
  <aside
    class="bg-white shadow-lg w-64 h-screen fixed top-0 left-0 flex flex-col border-r border-gray-200 z-40"
  >
    <!-- Logo -->
    <div class="flex items-center justify-center py-6 border-b">
      <img
        src="~/assets/images/Logonew_smart2.png"
        alt="PriceTravel"
        class="w-44"
      />
    </div>

    <!-- Navegación -->
    <nav class="flex-1 overflow-y-auto p-4 text-gray-700">
      <div v-for="(item, index) in menu" :key="index" class="mb-4">
        <button
          @click="toggleSection(index)"
          class="w-full text-left font-semibold hover:text-blue-600 flex justify-between items-center"
        >
          <span>{{ item.title }}</span>
          <span class="text-sm">{{ isOpen(index) ? '−' : '+' }}</span>
        </button>

        <transition name="fade">
          <ul
            v-if="isOpen(index)"
            class="mt-2 ml-4 space-y-1 text-sm text-gray-600"
          >
            <li
              v-for="sub in item.sub"
              :key="sub"
              class="cursor-pointer hover:text-blue-500 transition"
            >
              {{ sub }}
            </li>
          </ul>
        </transition>
      </div>
    </nav>
  </aside>
</template>

<script setup lang="ts">
// Ahora guardamos un conjunto de secciones abiertas
const openSections = ref<Set<number>>(new Set())

const toggleSection = (index: number) => {
  if (openSections.value.has(index)) {
    openSections.value.delete(index)
  } else {
    openSections.value.add(index)
  }
}

const isOpen = (index: number) => {
  return openSections.value.has(index)
}

const menu = [
  { title: 'Control de Publicidad', sub: ['Consultar', 'Crear', 'Crear desde PDF'] },
  { title: 'Marketing Deal (Rappel)', sub: ['Consultar', 'Crear', 'Crear desde PDF'] },
  { title: 'Destinos', sub: ['Consultar', 'Crear'] },
  { title: 'PPA', sub: ['Consultar', 'Crear', 'Crear desde PDF'] },
  { title: 'Finanzas', sub: ['Cargar Archivo', 'Editar'] },
  { title: 'Administración', sub: ['Usuarios', 'Perfiles', 'Permisos', 'Regenerar PDF'] },
]
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}
</style>
