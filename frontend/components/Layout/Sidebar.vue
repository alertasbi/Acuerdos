<template>
  <aside
    class="bg-white shadow-lg w-64 h-screen fixed top-[70px] left-0 flex flex-col border-r border-gray-200 z-40"
  >
    <!-- Navegación -->
    <nav class="flex-1 overflow-y-auto p-4 text-gray-700">
      <div
        v-for="(item, index) in menu"
        :key="index"
        class="mb-4"
      >
        <!-- Botón del grupo -->
        <button
          @click="toggleSection(index)"
          class="w-full text-left font-semibold hover:text-blue-600 flex justify-between items-center"
        >
          <span>{{ item.title }}</span>
          <span class="text-sm">{{ isOpen(index) ? '−' : '+' }}</span>
        </button>

        <!-- Submenú -->
        <transition name="fade">
          <ul
            v-if="isOpen(index)"
            class="mt-2 ml-4 space-y-1 text-sm text-gray-600"
          >
            <li
              v-for="sub in item.sub"
              :key="sub.label"
              class="cursor-pointer hover:text-blue-500 transition"
            >
              <NuxtLink
                :to="sub.to"
                class="block py-1"
                active-class="text-blue-600 font-semibold"
              >
                {{ sub.label }}
              </NuxtLink>
            </li>
          </ul>
        </transition>
      </div>
    </nav>
  </aside>
</template>

<script setup lang="ts">
const openSections = ref<Set<number>>(new Set())

// 🔄 Permite abrir varios apartados simultáneamente
const toggleSection = (index: number) => {
  if (openSections.value.has(index)) openSections.value.delete(index)
  else openSections.value.add(index)
}
const isOpen = (index: number) => openSections.value.has(index)

const menu = [
  {
    title: 'Control de Publicidad',
    sub: [
      { label: 'Consultar', to: '/control-publicidad/consultar' },
      { label: 'Crear', to: '/control-publicidad/crear' },
      { label: 'Crear desde PDF', to: '/control-publicidad/crear-desde-pdf' },
    ],
  },
  {
    title: 'Marketing Deal (Rappel)',
    sub: [
      { label: 'Consultar', to: '/marketing-deal/consultar' },
      { label: 'Crear', to: '/marketing-deal/crear' },
      { label: 'Crear desde PDF', to: '/marketing-deal/crear-desde-pdf' },
    ],
  },
  {
    title: 'Destinos',
    sub: [
      { label: 'Consultar', to: '/destinos/consultar' },
      { label: 'Crear', to: '/destinos/crear' },
    ],
  },
  {
    title: 'PPA',
    sub: [
      { label: 'Consultar', to: '/ppa/consultar' },
      { label: 'Crear', to: '/ppa/crear' },
      { label: 'Crear desde PDF', to: '/ppa/crear-desde-pdf' },
    ],
  },
  {
    title: 'Finanzas',
    sub: [
      { label: 'Cargar Archivo', to: '/finanzas/cargar' },
      { label: 'Editar', to: '/finanzas/editar' },
    ],
  },
  {
    title: 'Administración',
    sub: [
      { label: 'Usuarios', to: '/administracion/usuarios' },
      { label: 'Perfiles', to: '/administracion/perfiles' },
      { label: 'Permisos', to: '/administracion/permisos' },
      { label: 'Regenerar PDF', to: '/administracion/regenerar-pdf' },
    ],
  },
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
