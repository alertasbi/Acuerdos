<template>
  <div class="flex flex-col min-h-screen bg-gray-50">
    <Header />

    <main class="flex-grow container mx-auto px-6 pt-24 pb-24">
      <!-- Encabezado -->
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-xl font-semibold text-gray-700">
          Control de Publicidad
        </h1>

        <div class="flex gap-3">
          <button
            @click="vista = 'tarjetas'"
            :class="[ 
              'px-4 py-2 rounded-lg text-sm font-semibold transition',
              vista === 'tarjetas'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300',
            ]"
          >
            Vista tarjetas
          </button>
          <button
            @click="vista = 'tabla'"
            :class="[ 
              'px-4 py-2 rounded-lg text-sm font-semibold transition',
              vista === 'tabla'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300',
            ]"
          >
            Vista tabla
          </button>
        </div>
      </div>

      <!-- ✅ Vista TARJETAS -->
    <div
    v-if="vista === 'tarjetas'"
    class="grid gap-8 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3"
    >
    <div
        v-for="(item, i) in acuerdos"
        :key="i"
        class="bg-white shadow-lg rounded-2xl p-6 border border-gray-100 hover:shadow-xl transition-all duration-300 group cursor-pointer"
        @click="abrirDetalle(item)"
    >
        <!-- Contenido de la tarjeta -->
        <div class="select-none">
        <p class="font-bold text-gray-700 mb-1">Proveedor</p>
        <p class="text-gray-600">{{ item.proveedor }}</p>

        <p class="font-bold text-gray-700 mt-3 mb-1">Tipo Acuerdo</p>
        <p class="text-gray-600">{{ item.tipo }}</p>

        <p class="font-bold text-gray-700 mt-3 mb-1">Fecha Acuerdo</p>
        <p class="text-gray-600">{{ item.fecha }}</p>

        <p class="font-bold text-gray-700 mt-3 mb-1">Gerente</p>
        <p class="text-gray-600">{{ item.gerente }}</p>

        <p class="font-bold text-gray-700 mt-3 mb-1">Equipo</p>
        <p class="text-gray-600">{{ item.equipo }}</p>

        <p class="font-bold text-gray-700 mt-3 mb-1">Moneda & Monto</p>
        <p class="text-gray-600">{{ item.moneda }} {{ item.monto }}</p>

        <div class="mt-4 flex flex-col gap-2">
            <a
            href="#"
            class="text-blue-600 font-medium hover:underline"
            @click.stop="abrirHoteles(item)"
            >
            Ver Hoteles
            </a>
            <a
            href="#"
            class="text-blue-600 font-medium hover:underline"
            @click.stop
            >
            Ver Archivo
            </a>
        </div>
        </div>

        <!-- Botones inferiores -->
        <div class="flex justify-end gap-3 mt-6">
        <button
            class="px-4 py-1.5 rounded-lg bg-blue-500 text-white hover:bg-blue-600 transition text-sm"
            @click.stop
        >
            Editar
        </button>
        <button
            class="px-4 py-1.5 rounded-lg bg-red-500 text-white hover:bg-red-600 transition text-sm"
            @click.stop="abrirConfirmacion(item)"
        >
            Eliminar
        </button>
        </div>
    </div>
    </div>


      <!-- ✅ Vista TABLA -->
      <div
        v-else
        class="overflow-x-auto bg-white shadow-md rounded-2xl border border-gray-100"
      >
        <table class="w-full text-sm text-left text-gray-700">
          <thead class="text-xs uppercase bg-gray-100 text-gray-600">
            <tr>
              <th class="px-6 py-3">Proveedor</th>
              <th class="px-6 py-3">Tipo Acuerdo</th>
              <th class="px-6 py-3">Gerente</th>
              <th class="px-6 py-3">Equipo</th>
              <th class="px-6 py-3">Fecha</th>
              <th class="px-6 py-3">Moneda</th>
              <th class="px-6 py-3">Monto</th>
              <th class="px-6 py-3 text-center">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(item, i) in acuerdos"
              :key="i"
              class="border-b hover:bg-gray-50"
            >
              <td class="px-6 py-4">{{ item.proveedor }}</td>
              <td class="px-6 py-4">{{ item.tipo }}</td>
              <td class="px-6 py-4">{{ item.gerente }}</td>
              <td class="px-6 py-4">{{ item.equipo }}</td>
              <td class="px-6 py-4">{{ item.fecha }}</td>
              <td class="px-6 py-4">{{ item.moneda }}</td>
              <td class="px-6 py-4">{{ item.monto }}</td>
              <td class="px-6 py-4 text-center space-x-2">
                <a href="#" class="text-blue-500 hover:underline text-sm" @click.stop="abrirHoteles(item)">Ver Hoteles</a>
                <a href="#" class="text-blue-500 hover:underline text-sm">Ver Archivo</a>
                <button
                  class="px-2 py-1 bg-blue-500 text-white rounded text-xs hover:bg-blue-600"
                >
                  Editar
                </button>
                <button
                  class="px-2 py-1 bg-red-500 text-white rounded text-xs hover:bg-red-600"
                  @click="abrirConfirmacion(item)"
                >
                  Eliminar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>

    <Footer />

    <!-- 🟣 Modal detalle -->
    <div
      v-if="detalleSeleccionado && vista === 'tarjetas'"
      class="fixed inset-0 flex items-center justify-center bg-black/60 z-50"
    >
      <div
        class="bg-white w-full max-w-2xl p-8 rounded-2xl shadow-2xl relative overflow-y-auto max-h-[90vh]"
      >
        <button
          class="absolute top-4 right-4 text-gray-500 hover:text-gray-800"
          @click="detalleSeleccionado = null"
        >
          ✕
        </button>
        <h2 class="text-xl font-semibold text-gray-800 mb-6 text-center">
          Detalle del Acuerdo
        </h2>
        <div class="grid grid-cols-2 gap-x-6 gap-y-3 text-gray-700 text-sm">
          <template
            v-for="(valor, key) in detalleFiltrado(detalleSeleccionado)"
            :key="key"
          >
            <p class="font-semibold">{{ key }}</p>
            <p>{{ valor }}</p>
          </template>
        </div>
      </div>
    </div>

    <!-- 🔴 Modal confirmación eliminación -->
    <div
      v-if="mostrarConfirmacion"
      class="fixed inset-0 flex items-center justify-center bg-black/60 z-50"
    >
      <div
        class="bg-white w-full max-w-md p-8 rounded-2xl shadow-2xl relative text-center"
      >
        <h2 class="text-lg font-semibold text-gray-800 mb-4">
          ¿Estás seguro de eliminar este elemento?
        </h2>
        <p class="text-gray-600 mb-6">
          Esta acción no se puede deshacer (por ahora no elimina realmente).
        </p>
        <div class="flex justify-center gap-4">
          <button
            class="px-4 py-2 bg-gray-300 rounded-lg hover:bg-gray-400 transition"
            @click="cancelarEliminacion"
          >
            Cancelar
          </button>
          <button
            class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition"
            @click="confirmarEliminacion"
          >
            Sí, eliminar
          </button>
        </div>
      </div>
    </div>

    <!-- 🏨 Modal Ver Hoteles -->
    <div
    v-if="modalHoteles"
    class="fixed inset-0 flex items-center justify-center bg-black/60 z-50"
    >
    <div
        class="bg-white w-full max-w-lg p-8 rounded-2xl shadow-2xl relative overflow-y-auto max-h-[90vh]"
    >
        <!-- Botón cerrar -->
        <button
        class="absolute top-4 right-4 text-gray-500 hover:text-gray-800"
        @click="modalHoteles = false"
        >
        ✕
        </button>

        <h2 class="text-xl font-semibold text-gray-800 mb-6 text-center">
        Hoteles del Acuerdo
        </h2>

        <table class="w-full text-sm text-left text-gray-700 border-collapse">
        <thead
            class="bg-gradient-to-r from-yellow-400 via-pink-600 via-purple-700 to-sky-500 text-white uppercase text-xs"
        >
            <tr>
            <th class="px-4 py-2 border-b">ID Hotel</th>
            <th class="px-4 py-2 border-b">Nombre del Hotel</th>
            </tr>
        </thead>
        <tbody>
            <tr
            v-for="(hotel, index) in hotelesSeleccionados"
            :key="index"
            class="border-b hover:bg-gray-50"
            >
            <td class="px-4 py-2">{{ hotel.id }}</td>
            <td class="px-4 py-2">{{ hotel.nombre }}</td>
            </tr>
            <tr v-if="!hotelesSeleccionados.length">
            <td colspan="2" class="text-center py-4 text-gray-500">
                No hay hoteles asociados a este acuerdo.
            </td>
            </tr>
        </tbody>
        </table>
    </div>
    </div>


    <!-- ✅ Mensaje de éxito -->
    <transition name="fade">
      <div
        v-if="mensajeExito"
        class="fixed bottom-6 right-6 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg text-sm"
      >
        {{ mensajeExito }}
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">




import Header from '~/components/Layout/Header.vue'
import Footer from '~/components/Layout/FooterBar.vue'

const vista = ref<'tarjetas' | 'tabla'>('tarjetas')
const detalleSeleccionado = ref<Record<string, any> | null>(null)
const mostrarConfirmacion = ref(false)
const mensajeExito = ref('')
let itemPendiente = ref<any>(null)

const modalHoteles = ref(false)
const hotelesSeleccionados = ref<{ id: string; nombre: string }[]>([])

const abrirHoteles = (item: any) => {
  // 🔹 Simulamos una lista de hoteles del acuerdo (por ahora fija)
  hotelesSeleccionados.value = [
    { id: 'HTL001', nombre: 'Occidental Tucancun' },
    { id: 'HTL002', nombre: 'Grand Oasis Cancun' },
    { id: 'HTL003', nombre: 'Emporio Cancun' },
  ]

  modalHoteles.value = true
}

const abrirDetalle = (item: any) => {
  detalleSeleccionado.value = item
}

const abrirConfirmacion = (item: any) => {
  itemPendiente.value = item
  mostrarConfirmacion.value = true
}

const cancelarEliminacion = () => {
  mostrarConfirmacion.value = false
  itemPendiente.value = null
}

const confirmarEliminacion = () => {
  mostrarConfirmacion.value = false
  mensajeExito.value = '✅ Elemento eliminado correctamente'
  setTimeout(() => {
    mensajeExito.value = ''
  }, 2000)
}

const detalleFiltrado = (item: any) => {
  if (!item) return {}
  const keysOrden = [
    'Registro', 'Equipo', 'Año', 'Mes', 'TipoAcuerdo', 'Gerente', 'Proveedor',
    'ID', 'Moneda', 'PrecioSinIVA', 'FolioAcuerdo', 'MesesContratados',
    'FechaInicio', 'FechaFin', 'FechaVenta', 'RFC', 'FormaPago',
    'Comentarios', 'Firmado', 'ControlAcuerdos'
  ]
  const filtrado: Record<string, any> = {}
  for (const key of keysOrden) {
    if (item[key] !== undefined) filtrado[key] = item[key]
  }
  return filtrado
}

const acuerdos = ref([
  {
    Registro: '1682',
    Equipo: 'RCP México',
    Año: '2025',
    Mes: 'Septiembre',
    TipoAcuerdo: 'Paquete Fijo',
    Gerente: 'Christians Beatriz Ortiz Caballero',
    Proveedor: '1682/Occidental Tucancun/',
    ID: '100038/',
    Moneda: 'USD',
    PrecioSinIVA: '$7,500.00',
    FolioAcuerdo: '16431',
    MesesContratados: 1,
    FechaInicio: '01/09/2025',
    FechaFin: '30/09/2025',
    FechaVenta: '29/09/2025',
    RFC: 'PTU0608299B4',
    FormaPago: 'Descuento',
    Comentarios: '*Paquete Elite Aniversario PT / Pago en 2 Facturas',
    Firmado: 'Sí',
    ControlAcuerdos: 'Tucancun-firmada-2.pdf',
    proveedor: 'Occidental Tucancun',
    tipo: 'Paquete Fijo',
    fecha: '2025-09-01',
    gerente: 'Christians Ortiz',
    equipo: 'RCP México',
    moneda: 'USD',
    monto: '7,500.00',
  },
])
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

<style scoped>
/* ✋ Hace que solo el cuerpo de la tarjeta muestre el cursor pointer, 
   pero no los botones ni enlaces */
.group:hover {
  transform: translateY(-3px);
}
.group * {
  cursor: default;
}
.group {
  cursor: pointer;
}
.group button,
.group a {
  cursor: pointer;
}
</style>

