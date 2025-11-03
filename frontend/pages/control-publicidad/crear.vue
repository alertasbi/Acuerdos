<template>
  <div class="flex flex-col min-h-screen bg-gray-50">
    <Header />

    <main class="flex-grow container mx-auto px-6 pt-24 pb-24">
      <!-- Encabezado -->
      <div class="mb-10">
        <h1 class="text-xl font-semibold text-gray-700">
          Crear nuevo acuerdo
        </h1>
        <div class="mt-3 h-1 bg-gradient-to-r from-yellow-400 via-pink-600 to-sky-500 rounded-full w-40"></div>
      </div>

      <!-- Contenedor del formulario -->
      <div class="bg-white shadow-md rounded-2xl border border-gray-100 p-8">
        <!-- Paso 1 -->
        <div v-if="step === 1">
        <h2 class="text-lg font-semibold text-gray-700 mb-2">
            Paso 1: Selección del tipo de acuerdo
        </h2>
        <p class="text-sm text-gray-500 mb-6">(*) Campos obligatorios</p>

        <p class="text-gray-600 mb-6">
            Primero debe seleccionar si desea
            <strong>generar un PDF</strong> o
            <strong>subir un acuerdo existente</strong>.
        </p>

        <!-- Botones de selección -->
        <div class="flex flex-col sm:flex-row gap-4 mb-8">
            <button
            @click="selectedOption = 'pdf'"
            :class="[
                'flex-1 py-3 rounded-lg border-2 font-semibold transition-all text-center',
                selectedOption === 'pdf'
                ? 'border-blue-500 text-blue-600 bg-blue-50 shadow-sm'
                : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
            ]"
            >
            📄 Generar PDF
            </button>

            <button
            @click="selectedOption = 'upload'"
            :class="[
                'flex-1 py-3 rounded-lg border-2 font-semibold transition-all text-center',
                selectedOption === 'upload'
                ? 'border-blue-500 text-blue-600 bg-blue-50 shadow-sm'
                : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
            ]"
            >
            ⬆️ Subir Acuerdo
            </button>
        </div>

        <!-- Si elige subir, aparece input -->
        <div v-if="selectedOption === 'upload'" class="mb-6">
            <label class="block text-gray-700 font-medium mb-2">
            Cargar archivo desde su computadora (*)
            </label>
            <input
            type="file"
            accept=".pdf,.doc,.docx"
            @change="handleFileUpload"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 cursor-pointer hover:border-blue-400 transition"
            />
            <p v-if="fileName" class="text-sm text-gray-500 mt-2">
            Archivo seleccionado: <strong>{{ fileName }}</strong>
            </p>
        </div>

        <!-- Botones de navegación -->
        <div class="flex justify-between mt-10">
            <button
            disabled
            class="px-6 py-2 rounded-lg bg-gray-200 text-gray-400 font-semibold cursor-not-allowed"
            >
            Anterior
            </button>

            <button
            @click="nextStep"
            :disabled="!selectedOption"
            class="bg-gradient-to-r from-yellow-400 via-pink-600 to-sky-500 text-white px-6 py-2 rounded-lg font-semibold shadow-md disabled:opacity-50 disabled:cursor-not-allowed transition-transform hover:scale-[1.03]"
            >
            Siguiente
            </button>
        </div>
        </div>

        <!-- Paso 2 -->
        <div v-else-if="step === 2">
        <h2 class="text-lg font-semibold text-gray-700 mb-2">
            Paso 2: Detalles del acuerdo
        </h2>
        <p class="text-sm text-gray-500 mb-6">(*) Campos obligatorios</p>

        <form @submit.prevent="submitForm" class="space-y-6">
            <!-- Grid principal -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Equipo -->
            <div>
                <label class="block text-gray-700 font-medium mb-2">Equipo (*)</label>
                <select
                v-model="form.equipo"
                required
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                <option value="">Seleccione equipo</option>
                <option>RCP Colombia</option>
                <option>RCP México</option>
                <option>RCP Terrestres</option>
                <option>RCP Aerolíneas</option>
                <option>Destinos</option>
                <option>RCP Caribe</option>
                </select>
            </div>

            <!-- Tipo de acuerdo -->
            <div>
                <label class="block text-gray-700 font-medium mb-2">Tipo de acuerdo (*)</label>
                <select
                v-model="form.tipoAcuerdo"
                required
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                <option value="">Seleccione tipo</option>
                <option>Fondo Media</option>
                <option>Paquete Fijo</option>
                </select>
            </div>

            <!-- Folio Media -->
            <div>
                <label class="block text-gray-700 font-medium mb-2">Folio Media</label>
                <input
                v-model="form.folioMedia"
                type="text"
                placeholder="Ingrese el folio"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
            </div>

            <!-- Moneda -->
            <div>
                <label class="block text-gray-700 font-medium mb-2">Moneda (*)</label>
                <select
                v-model="form.moneda"
                required
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                <option value="">Seleccione moneda</option>
                <option value="CAD">CAD - Dólar canadiense</option>
                <option value="COP">COP - Peso colombiano</option>
                <option value="EUR">EUR - Euro</option>
                <option value="MXN">MXN - Peso mexicano</option>
                <option value="USD">USD - Dólar estadounidense</option>
                </select>
            </div>

            <!-- Precio sin IVA -->
            <div>
                <label class="block text-gray-700 font-medium mb-2">Precio sin IVA</label>
                <input
                v-model="form.precioSinIVA"
                type="number"
                step="0.01"
                min="0"
                placeholder="0.00"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
            </div>

            <!-- IVA -->
            <div>
                <label class="block text-gray-700 font-medium mb-2">IVA (%)</label>
                <select
                v-model="form.iva"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                <option value="">Seleccione</option>
                <option value="0">0</option>
                <option value="8">8</option>
                <option value="16">16</option>
                <option value="19">19</option>
                </select>
            </div>

            <!-- Porcentaje -->
            <div>
                <label class="block text-gray-700 font-medium mb-2">Porcentaje</label>
                <input
                v-model="form.porcentaje"
                type="number"
                step="0.01"
                min="0"
                max="100"
                placeholder="0.00"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
            </div>

            <!-- Tipo -->
            <div>
                <label class="block text-gray-700 font-medium mb-2">Tipo</label>
                <input
                v-model="form.tipo"
                type="text"
                placeholder="Ingrese tipo"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
            </div>
            </div>

            <!-- Botones -->
            <div class="flex justify-between mt-4 pt-4 border-t border-gray-200">
            <button
                type="button"
                @click="prevStep"
                class="px-6 py-2 rounded-lg border border-gray-300 text-gray-700 font-medium hover:border-blue-400 hover:text-blue-600 transition"
            >
                Anterior
            </button>

            <button
                type="button"
                @click="nextStep"
                class="bg-gradient-to-r from-yellow-400 via-pink-600 to-sky-500 text-white px-6 py-2 rounded-lg font-semibold shadow-md hover:scale-[1.03] transition-transform"
            >
                Siguiente
            </button>
            </div>

        </form>
        </div>

        <!-- Paso 3 -->
        <div v-else-if="step === 3">
        <h2 class="text-lg font-semibold text-gray-700 mb-2">
            Paso 3: Periodo del acuerdo
        </h2>
        <p class="text-sm text-gray-500 mb-6">(*) Campos obligatorios</p>

        <form @submit.prevent="submitForm" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Fecha inicio -->
            <div>
                <label class="block text-gray-700 font-medium mb-2">Fecha de inicio (*)</label>
                <input
                v-model="form.fechaInicio"
                type="date"
                required
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
            </div>

            <!-- Fecha término -->
            <div>
                <label class="block text-gray-700 font-medium mb-2">Fecha de término (*)</label>
                <input
                v-model="form.fechaTermino"
                type="date"
                required
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
            </div>
            </div>

            <!-- Botones -->
            <div class="flex justify-between mt-4 pt-6 border-t border-gray-200">
            <button
                type="button"
                @click="prevStep"
                class="px-6 py-2 rounded-lg border border-gray-300 text-gray-700 font-medium hover:border-blue-400 hover:text-blue-600 transition"
            >
                Anterior
            </button>

            <button
                type="button"
                @click="nextStep"
                class="bg-gradient-to-r from-yellow-400 via-pink-600 to-sky-500 text-white px-6 py-2 rounded-lg font-semibold shadow-md hover:scale-[1.03] transition-transform"
            >
                Siguiente 
            </button>
            </div>
        </form>
        </div>

        <!-- Paso 4 -->
        <div v-else-if="step === 4">
        <h2 class="text-lg font-semibold text-gray-700 mb-2">
            Paso 4: Datos de facturación
        </h2>
        <p class="text-sm text-gray-500 mb-6">(*) Campos obligatorios</p>

        <form @submit.prevent="submitForm" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Comprobante -->
            <div>
                <label class="block text-gray-700 font-medium mb-2">Comprobante (*)</label>
                <select
                v-model="form.comprobante"
                required
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                <option value="">Seleccione tipo</option>
                <option value="Factura">Factura</option>
                <option value="Invoice">Invoice</option>
                </select>
            </div>

            <!-- Número de factura -->
            <div>
                <label class="block text-gray-700 font-medium mb-2">Número de factura</label>
                <input
                v-model="form.numeroFactura"
                type="text"
                placeholder="Ingrese número de factura"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
            </div>

            <!-- Fecha de facturación -->
            <div>
                <label class="block text-gray-700 font-medium mb-2">Fecha de facturación</label>
                <input
                v-model="form.fechaFacturacion"
                type="date"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
            </div>

            <!-- Forma de pago -->
            <div>
                <label class="block text-gray-700 font-medium mb-2">Forma de pago (*)</label>
                <select
                v-model="form.formaPago"
                required
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                <option value="">Seleccione forma de pago</option>
                <option value="Descuento">Descuento</option>
                <option value="Depósito o Transferencia">Depósito o Transferencia</option>
                <option value="Intercambio">Intercambio</option>
                <option value="Patrocinio">Patrocinio</option>
                <option value="Otro">Otro</option>
                </select>
            </div>
            </div>

            <!-- Comentarios -->
            <div class="mt-4">
            <label class="block text-gray-700 font-medium mb-2">Comentarios</label>
            <textarea
                v-model="form.comentarios"
                rows="4"
                placeholder="Ingrese observaciones o detalles adicionales..."
                class="w-full border border-gray-300 rounded-lg px-3 py-2 resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            ></textarea>
            </div>

            <!-- Botones -->
            <div class="flex justify-between mt-4 pt-6 border-t border-gray-200">
            <button
                type="button"
                @click="prevStep"
                class="px-6 py-2 rounded-lg border border-gray-300 text-gray-700 font-medium hover:border-blue-400 hover:text-blue-600 transition"
            >
                Anterior
            </button>

            <button
                type="button"
                @click="nextStep"
                class="bg-gradient-to-r from-yellow-400 via-pink-600 to-sky-500 text-white px-6 py-2 rounded-lg font-semibold shadow-md hover:scale-[1.03] transition-transform"
            >
                Siguiente 
            </button>
            </div>
        </form>
        </div>

        <!-- Paso 5 -->
        <div v-else-if="step === 5">
        <h2 class="text-lg font-semibold text-gray-700 mb-2">
            Paso 5: Datos del cliente
        </h2>
        <p class="text-sm text-gray-500 mb-6">(*) Campos obligatorios</p>

        <form @submit.prevent="submitForm" class="space-y-8">
            <!-- Cliente o RFC -->
            <div>
            <label class="block text-gray-700 font-medium mb-2">Cliente o RFC (*)</label>
            <input
                v-model="form.clienteRFC"
                type="text"
                placeholder="Ingrese el cliente o RFC"
                required
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            </div>

            <!-- Contactos -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-y-8" style="column-gap: 6rem;">



            <!-- Contacto Contabilidad -->
            <div>
                <h3 class="text-md font-semibold text-gray-700 mb-4 border-b border-gray-200 pb-1">
                Contacto Contabilidad
                </h3>

                <div class="space-y-4">
                <div>
                    <label class="block text-gray-700 text-sm font-medium mb-1">Nombre</label>
                    <input
                    v-model="form.contabilidadNombre"
                    type="text"
                    placeholder="Nombre"
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                </div>

                <div>
                    <label class="block text-gray-700 text-sm font-medium mb-1">Cargo</label>
                    <input
                    v-model="form.contabilidadCargo"
                    type="text"
                    placeholder="Cargo"
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                </div>

                <div>
                    <label class="block text-gray-700 text-sm font-medium mb-1">E-mail</label>
                    <input
                    v-model="form.contabilidadEmail"
                    type="email"
                    placeholder="correo@empresa.com"
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                </div>

                <div>
                    <label class="block text-gray-700 text-sm font-medium mb-1">Teléfono</label>
                    <input
                    v-model="form.contabilidadTelefono"
                    type="tel"
                    placeholder="Ej. +52 998 123 4567"
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                </div>
                </div>
            </div>

            <!-- Contacto Marketing -->
            <div>
                <h3 class="text-md font-semibold text-gray-700 mb-4 border-b border-gray-200 pb-1">
                Contacto Marketing
                </h3>

                <div class="space-y-4">
                <div>
                    <label class="block text-gray-700 text-sm font-medium mb-1">Nombre</label>
                    <input
                    v-model="form.marketingNombre"
                    type="text"
                    placeholder="Nombre"
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                </div>

                <div>
                    <label class="block text-gray-700 text-sm font-medium mb-1">Cargo</label>
                    <input
                    v-model="form.marketingCargo"
                    type="text"
                    placeholder="Cargo"
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                </div>

                <div>
                    <label class="block text-gray-700 text-sm font-medium mb-1">E-mail</label>
                    <input
                    v-model="form.marketingEmail"
                    type="email"
                    placeholder="correo@empresa.com"
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                </div>

                <div>
                    <label class="block text-gray-700 text-sm font-medium mb-1">Teléfono</label>
                    <input
                    v-model="form.marketingTelefono"
                    type="tel"
                    placeholder="Ej. +52 998 123 4567"
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                </div>
                </div>
            </div>
            </div>

            <!-- Botones -->
            <div class="flex justify-between mt-14 pt-6 border-t border-gray-200">
            <button
                type="button"
                @click="prevStep"
                class="px-6 py-2 rounded-lg border border-gray-300 text-gray-700 font-medium hover:border-blue-400 hover:text-blue-600 transition"
            >
                Anterior
            </button>

            <button
                type="button"
                @click="nextStep"
                class="bg-gradient-to-r from-yellow-400 via-pink-600 to-sky-500 text-white px-6 py-2 rounded-lg font-semibold shadow-md hover:scale-[1.03] transition-transform"
            >
                Siguiente
            </button>
            </div>
        </form>
        </div>

        <!-- Paso 6 -->
        <div v-else-if="step === 6">
        <h2 class="text-lg font-semibold text-gray-700 mb-2">
            Paso 6: Datos de Hoteles
        </h2>
        <p class="text-sm text-gray-500 mb-6">(*) Campos obligatorios</p>

        <form @submit.prevent="submitForm" class="space-y-6">
            <!-- Tipo de selección -->
            <div>
            <label class="block text-gray-700 font-medium mb-2">Tipo de acuerdo con hotel (*)</label>
            <select
                v-model="form.tipoHotel"
                @change="cambiarTipoHotel"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
                <option value="">Seleccione tipo</option>
                <option value="Corporativo">Corporativo</option>
                <option value="Individual">Individual</option>
            </select>
            </div>

            <!-- Buscador dinámico -->
            <div v-if="form.tipoHotel" class="mt-4">
            <label class="block text-gray-700 font-medium mb-2">
                Buscar por {{ form.tipoHotel === 'Corporativo' ? 'nombre corporativo' : 'ID o nombre del hotel' }}
            </label>
            <input
                v-model="busquedaHotel"
                type="text"
                placeholder="Ingrese término de búsqueda"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                @input="filtrarHoteles"
            />
            </div>

            <!-- Tabla de resultados -->
            <div v-if="hotelesFiltrados.length" class="mt-4 overflow-x-auto">
            <table class="min-w-full border border-gray-200 rounded-lg">
                <thead class="bg-gray-100 text-gray-700">
                <tr>
                    <th class="px-4 py-2 border-b text-left">
                    <input type="checkbox" v-model="seleccionarTodos" @change="toggleTodos" class="w-4 h-4" />
                    <span class="ml-2 font-medium">Todo</span>
                    </th>
                    <th class="px-4 py-2 border-b">ID {{ form.tipoHotel === 'Corporativo' ? 'Corporativo' : 'Hotel' }}</th>
                    <th class="px-4 py-2 border-b">{{ form.tipoHotel === 'Corporativo' ? 'Nombre del Corporativo' : 'Hotel' }}</th>
                </tr>
                </thead>
                <tbody>
                <tr
                    v-for="item in hotelesFiltrados"
                    :key="item.id"
                    class="hover:bg-gray-50 transition"
                >
                    <td class="px-4 py-2 border-b">
                    <input type="checkbox" v-model="item.seleccionado" class="w-4 h-4" />
                    </td>
                    <td class="px-4 py-2 border-b">{{ item.id }}</td>
                    <td class="px-4 py-2 border-b">{{ item.nombre }}</td>
                </tr>
                </tbody>
            </table>
            </div>

            <div v-else-if="form.tipoHotel && !busquedaHotel" class="text-gray-500 text-sm mt-6">
             Ingrese un término para buscar hoteles o corporativos.
            </div>

            <div v-else-if="form.tipoHotel && busquedaHotel && !hotelesFiltrados.length" class="text-gray-500 text-sm mt-6">
            ⚠️ No se encontraron resultados.
            </div>

            <!-- Botones -->
            <div class="flex justify-between mt-4 pt-6 border-t border-gray-200">
            <button
                type="button"
                @click="prevStep"
                class="px-6 py-2 rounded-lg border border-gray-300 text-gray-700 font-medium hover:border-blue-400 hover:text-blue-600 transition"
            >
                Anterior
            </button>

            <button
                type="submit"
                @click="nextStep"
                class="bg-gradient-to-r from-yellow-400 via-pink-600 to-sky-500 text-white px-6 py-2 rounded-lg font-semibold shadow-md hover:scale-[1.03] transition-transform"
            >
                Siguiente
            </button>
            </div>
        </form>
        </div>

        <!-- Paso 7 -->
        <div v-else-if="step === 7" class="text-center">
        <h2 class="text-lg font-semibold text-gray-700 mb-2">
            Paso 7: Confirmación final
        </h2>
        <p class="text-sm text-gray-500 mb-10">Revise los datos antes de finalizar el acuerdo.</p>

        <div class="flex flex-col items-center space-y-10">
            <div class="flex justify-center mt-4 gap-6">
            <!-- Botón Anterior -->
            <button
                type="button"
                @click="prevStep"
                class="px-6 py-2 rounded-lg border border-gray-300 text-gray-700 font-medium hover:border-blue-400 hover:text-blue-600 transition"
            >
                Anterior
            </button>

            <!-- Botón Vista Previa PDF -->
            <button
                type="button"
                @click="vistaPreviaPDF"
                class="px-6 py-2 rounded-lg bg-gray-200 text-gray-700 font-semibold hover:bg-gray-300 transition"
            >
                📄 Vista previa PDF
            </button>

            <!-- Botón Terminar -->
            <button
                type="button"
                @click="finalizarAcuerdo"
                class="bg-gradient-to-r from-yellow-400 via-pink-600 to-sky-500 text-white px-6 py-2 rounded-lg font-semibold shadow-md hover:scale-[1.03] transition-transform"
            >
                Terminar
            </button>
            </div>
        </div>

        <!-- Notificación -->
        <transition name="fade">
            <div
            v-if="mensajeExito"
            class="fixed bottom-6 right-6 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg text-sm z-50"
            >
            {{ mensajeExito }}
            </div>
        </transition>
        </div>





      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup lang="ts">
import Header from '~/components/Layout/Header.vue'
import Footer from '~/components/Layout/FooterBar.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const mensajeExito = ref('')

const vistaPreviaPDF = () => {
  alert('📝 Aquí se generará la vista previa del PDF (pendiente de conexión).')
}

const finalizarAcuerdo = () => {
  mensajeExito.value = '✅ Acuerdo creado con éxito'
  setTimeout(() => {
    mensajeExito.value = ''
    router.push('/home') // redirige al home
  }, 1000)
}


const step = ref(1)
const selectedOption = ref<string | null>(null)
const fileName = ref<string | null>(null)

const form = reactive({
  equipo: '',
  tipoAcuerdo: '',
  folioMedia: '',
  moneda: '',
  precioSinIVA: '',
  iva: '',
  porcentaje: '',
  tipo: '',
  fechaInicio: '',
  fechaTermino: '',
  comprobante: '',
  numeroFactura: '',
  fechaFacturacion: '',
  formaPago: '',
  comentarios: '',
  clienteRFC: '',
  contabilidadNombre: '',
  contabilidadCargo: '',
  contabilidadEmail: '',
  contabilidadTelefono: '',
  marketingNombre: '',
  marketingCargo: '',
  marketingEmail: '',
  marketingTelefono: ''
})

const busquedaHotel = ref('')
const seleccionarTodos = ref(false)

// Hoteles individuales
const hotelesIndividuales = [
  { id: 1, nombre: 'Hotel Riviera', seleccionado: false },
  { id: 2, nombre: 'Hotel Sol Caribe', seleccionado: false },
  { id: 3, nombre: 'Hotel Ocean View', seleccionado: false },
]

// Corporativos
const corporativos = [
  { id: 101, nombre: 'Grupo Barceló', seleccionado: false },
  { id: 102, nombre: 'Riu Hotels & Resorts', seleccionado: false },
]

const hotelesFiltrados = ref([])

// cambia el dataset según el tipo seleccionado
const cambiarTipoHotel = () => {
  busquedaHotel.value = ''
  seleccionarTodos.value = false
  hotelesFiltrados.value =
    form.tipoHotel === 'Corporativo'
      ? [...corporativos]
      : [...hotelesIndividuales]
}

// filtra en tiempo real
const filtrarHoteles = () => {
  const termino = busquedaHotel.value.toLowerCase()
  const base =
    form.tipoHotel === 'Corporativo' ? corporativos : hotelesIndividuales

  hotelesFiltrados.value = base.filter(
    (h) =>
      h.nombre.toLowerCase().includes(termino) ||
      String(h.id).includes(termino)
  )
}

// seleccionar/deseleccionar todos
const toggleTodos = () => {
  hotelesFiltrados.value.forEach(
    (h) => (h.seleccionado = seleccionarTodos.value)
  )
}

const handleFileUpload = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    fileName.value = target.files[0].name
  } else {
    fileName.value = null
  }
}

const nextStep = () => {
  if (step.value < 7) step.value++ // 🔹 te prepara hasta el paso 6
}

const submitForm = () => {
  // por ahora solo para pruebas, luego conectamos con backend
  alert(`✅ Datos guardados temporalmente.\nPaso actual: ${step.value}`)
}


const prevStep = () => {
  step.value--
}



</script>
