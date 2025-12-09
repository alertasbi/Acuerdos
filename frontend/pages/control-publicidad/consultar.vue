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

      <!-- 🔍 Filtros -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 mb-4">
        <input
          v-model="filtros.anio"
          type="text"
          placeholder="Año"
          class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <input
          v-model="filtros.tipo"
          type="text"
          placeholder="Tipo de acuerdo"
          class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <input
          v-model="filtros.gerente"
          type="text"
          placeholder="Gerente"
          class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <input
          v-model="filtros.proveedor"
          type="text"
          placeholder="Proveedor"
          class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      <div class="flex justify-start mb-6 ml-1">
        <button
          @click="limpiarFiltros"
          class="text-sm text-gray-600 hover:text-blue-600 underline"
        >
          Limpiar filtros
        </button>
      </div>


      <!-- ✅ Vista TARJETAS -->
      <div
        v-if="vista === 'tarjetas'"
        class="grid gap-6 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
      >
        <div
          v-for="(item, i) in acuerdosFiltrados"
          :key="i"
          class="bg-white shadow-md rounded-xl p-4 border border-gray-100 hover:shadow-lg transition-all duration-300 group cursor-pointer h-full"
          @click="abrirDetalle(item)"
        >
          <!-- Contenido de la tarjeta -->
          <div class="select-none">
            <p class="font-bold text-gray-700 mt-1 mb-0.5">Proveedor</p>
            <p class="text-gray-600">{{ item.proveedor }}</p>

            <p class="font-bold text-gray-700 mt-1 mb-0.5">Tipo Acuerdo</p>
            <p class="text-gray-600">{{ item.tipo }}</p>

            <p class="font-bold text-gray-700 mt-1 mb-0.5">Fecha Acuerdo</p>
            <p class="text-gray-600">{{ item.fecha }}</p>

            <p class="font-bold text-gray-700 mt-1 mb-0.5">Gerente</p>
            <p class="text-gray-600">{{ item.gerente }}</p>

            <p class="font-bold text-gray-700 mt-1 mb-0.5">Equipo</p>
            <p class="text-gray-600">{{ item.equipo }}</p>

            <p class="font-bold text-gray-700 mt-1 mb-0.5">Moneda & Monto</p>
            <p class="text-gray-600">{{ item.moneda }} {{ item.monto }}</p>

            <div class="mt-4 flex flex-col gap-2">
              <a
                href="#"
                class="text-blue-600 font-medium hover:underline"
                @click.stop="abrirHoteles(item)"
              >
                Hoteles
              </a>
              <a
                href="#"
                class="text-blue-600 font-medium hover:underline"
                @click.stop
              >
                Archivo
              </a>
            </div>
          </div>

          <!-- Botones inferiores -->
          <div class="flex justify-end gap-2 mt-3">
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
              v-for="(item, i) in acuerdosFiltrados"
              :key="i"
              class="border-b hover:bg-blue-50 cursor-pointer transition"
              @click="abrirDetalle(item)"
            >
              <td class="px-6 py-4">{{ item.proveedor }}</td>
              <td class="px-6 py-4">{{ item.tipo }}</td>
              <td class="px-6 py-4">{{ item.gerente }}</td>
              <td class="px-6 py-4">{{ item.equipo }}</td>
              <td class="px-6 py-4">{{ item.fecha }}</td>
              <td class="px-6 py-4">{{ item.moneda }}</td>
              <td class="px-6 py-4">{{ item.monto }}</td>
              <td class="px-6 py-4">
                <div class="flex flex-wrap justify-center gap-2">
                  <a
                    href="#"
                    class="text-blue-500 hover:underline text-sm whitespace-nowrap"
                    @click.stop="abrirHoteles(item)"
                  >
                    Hoteles
                  </a>
                  <a
                    href="#"
                    class="text-blue-500 hover:underline text-sm whitespace-nowrap"
                    @click.stop
                  >
                    Archivo
                  </a>
                  <button
                    class="px-2 py-1 bg-blue-500 text-white rounded text-xs hover:bg-blue-600 whitespace-nowrap"
                    @click.stop
                  >
                    Editar
                  </button>
                  <button
                    class="px-2 py-1 bg-red-500 text-white rounded text-xs hover:bg-red-600 whitespace-nowrap"
                    @click.stop="abrirConfirmacion(item)"
                  >
                    Eliminar
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>

    <Footer />

    <!-- 🌀 LOADING OVERLAY -->
    <div
      v-if="cargando"
      class="fixed inset-0 bg-white/70 backdrop-blur-sm flex flex-col items-center justify-center z-[9999]"
    >
      <!-- Spinner -->
      <div class="loader mb-4"></div>

      <!-- Texto -->
      <p class="text-gray-700 font-medium">Cargando información...</p>
    </div>


    <!-- 🟣 Modal detalle -->
    <div
      v-if="detalleSeleccionado"
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
          Detalle del Acuerdo – <span class="text-blue-600">{{ detalleSeleccionado?.proveedor }}</span>
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
        <button
          class="absolute top-4 right-4 text-gray-500 hover:text-gray-800"
          @click="cerrarModalHoteles()"
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
import { useUserStore } from '~/stores/user'

const cargando = ref(true)
const acuerdos = ref<any[]>([])
const userStore = useUserStore()
const scrollPos = ref(0)



const vista = ref<'tarjetas' | 'tabla'>('tarjetas')
const detalleSeleccionado = ref<Record<string, any> | null>(null)
const mostrarConfirmacion = ref(false)
const mensajeExito = ref('')
let itemPendiente = ref<any>(null)
const modalHoteles = ref(false)
const hotelesSeleccionados = ref<{ id: string; nombre: string }[]>([])

const filtros = reactive({
  anio: '',
  tipo: '',
  gerente: '',
  id: '',
  proveedor: '',
})

const limpiarFiltros = () => {
  Object.assign(filtros, { anio: '', tipo: '', gerente: '', id: '', proveedor: '' })
}

const abrirHoteles = async (item: any) => {
  // Guardar posición actual
  scrollPos.value = window.scrollY

  // Bloquear scroll del body
  document.body.style.position = "fixed"
  document.body.style.top = `-${scrollPos.value}px`
  document.body.style.left = "0"
  document.body.style.right = "0"
  document.body.style.width = "100%"

  modalHoteles.value = true
  hotelesSeleccionados.value = []

  const controlPublicidadId = item.Registro
  
  try {
    cargando.value = true

    const response = await $fetch("http://127.0.0.1:5000/api/acuerdosHoteles", {
      method: "GET",
      params: {
        controlPublicidadId,
        opcion: 2,
        userId: userStore.idUser
      }
    })

    hotelesSeleccionados.value = response.map((h: any) => ({
      id: h.ID,
      nombre: h.Nombre
    }))
  } finally {
    cargando.value = false
  }
}

const cerrarModalHoteles = () => {
  modalHoteles.value = false

  // Restaurar scroll del body
  document.body.style.position = ""
  document.body.style.top = ""
  document.body.style.left = ""
  document.body.style.right = ""
  document.body.style.width = ""

  // Volver exactamente al punto donde estaba el usuario
  window.scrollTo(0, scrollPos.value)
}



const abrirDetalle = (item: any) => (detalleSeleccionado.value = item)
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
  setTimeout(() => (mensajeExito.value = ''), 2000)
}

const detalleFiltrado = (item: any) => {
  if (!item) return {}
  const keysOrden = [
    'Registro','Equipo','Año','Mes','TipoAcuerdo','Gerente','Proveedor','ID','Moneda','PrecioSinIVA',
    'FolioAcuerdo','MesesContratados','FechaInicio','FechaFin','FechaVenta','RFC','FormaPago',
    'Comentarios','Firmado','ControlAcuerdos'
  ]
  const filtrado: Record<string, any> = {}
  for (const key of keysOrden) if (item[key] !== undefined) filtrado[key] = item[key]
  return filtrado
}

onMounted(async () => {
  cargando.value = true   

  try {
    const response = await $fetch(`http://127.0.0.1:5000/api/acuerdos`, {
      method: "GET",
      params: { userId: userStore.idUser }
    })

    console.log("Acuerdos obtenidos:", response)

    acuerdos.value = response.map((a: any) => ({
      proveedor: a.Proveedor,
      tipo: a.TipoAcuerdo,
      fecha: a.FechaCobro || a.FechaVenta || "",
      gerente: a.Gerente,
      equipo: a.Equipo,
      moneda: a.MonedaAcuerdo,
      monto: a.PrecioSinIVA,
      Registro: a.Registro,
      ...a
    }))
  } catch (err) {
    console.error("❌ Error cargando acuerdos:", err)
  } finally {
    cargando.value = false   // ✔ Oculta loading cuando termina
  }
})





const acuerdosFiltrados = computed(() =>
  acuerdos.value.filter((item) => {
    const coincideAnio = filtros.anio ? String(item.Año || '').toLowerCase().includes(filtros.anio.toLowerCase()) : true
    const coincideTipo = filtros.tipo ? (item.tipo || item.TipoAcuerdo || '').toLowerCase().includes(filtros.tipo.toLowerCase()) : true
    const coincideGerente = filtros.gerente ? (item.gerente || item.Gerente || '').toLowerCase().includes(filtros.gerente.toLowerCase()) : true
    const coincideId = filtros.id ? (item.ID || '').toLowerCase().includes(filtros.id.toLowerCase()) : true
    const coincideProveedor = filtros.proveedor ? (item.proveedor || item.Proveedor || '').toLowerCase().includes(filtros.proveedor.toLowerCase()) : true
    return coincideAnio && coincideTipo && coincideGerente && coincideId && coincideProveedor
  })
)
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
.loader {
  border: 6px solid #e5e7eb; /* gris claro */
  border-top: 6px solid #3b82f6; /* azul */
  border-radius: 50%;
  width: 48px;
  height: 48px;
  animation: spin 0.9s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

</style>
