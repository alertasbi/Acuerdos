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
          Selecciona si deseas <strong>generar un PDF</strong> o 
          <strong>trabajar con un acuerdo existente</strong>.
        </p>

        <!-- Botones -->
        <div class="flex flex-col sm:flex-row gap-4 mb-8">
          <button
            @click="() => { selectedOption = 'pdf'; form.tipoSeleccion = 'pdf' }"
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
            @click="() => { selectedOption = 'upload'; form.tipoSeleccion = 'upload' }"
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

        <!-- NUEVO: Opciones para acuerdo -->
        <div v-if="selectedOption === 'upload'" class="space-y-4">
          <label class="block text-gray-700 font-medium">Tipo de carga</label>
          <div class="flex gap-6">
            <label class="flex items-center gap-2">
              <input
                type="radio"
                value="nuevo"
                v-model="tipoCarga"
                class="w-4 h-4 text-blue-500 focus:ring-blue-400"
              />
              <span>Nuevo</span>
            </label>

            <label class="flex items-center gap-2">
              <input
                type="radio"
                value="pendiente"
                v-model="tipoCarga"
                class="w-4 h-4 text-blue-500 focus:ring-blue-400"
              />
              <span>Pendiente</span>
            </label>
          </div>

          <!-- Si es pendiente -->
          <div v-if="tipoCarga === 'pendiente'" class="mt-4">
            <label class="block text-gray-700 font-medium mb-2">Selecciona acuerdo pendiente</label>
            <select
              v-model="acuerdoSeleccionado"
              @change="cargarDatosAcuerdo"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">Seleccione un acuerdo</option>
              <option v-for="a in acuerdosPendientes" :key="a.id" :value="a.id">
                Acuerdo {{ a.id }}
              </option>
            </select>
          </div>
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


        <!-- Notificación -->
        <transition name="fade">
          <div
            v-if="alertaPaso1"
            class="fixed bottom-20 right-6 z-50 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg text-sm"
          >
            {{ alertaPaso1 }}
          </div>
        </transition>

        </div>

        <!-- Paso 2 -->
        <div v-else-if="step === 2">
        <h2 class="text-lg font-semibold text-gray-700 mb-2">
            Paso 2: Detalles del acuerdo
        </h2>
        <p class="text-sm text-gray-500 mb-6">(*) Campos obligatorios</p>

        <form @submit.prevent="validarPaso2" novalidate class="space-y-6">

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
                @change="handleTipoAcuerdo"
                required
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                <option value="">Seleccione tipo</option>
                <option value="Fondo Media">Fondo Media</option>
                <option value="Paquete Fijo">Paquete Fijo</option>
                </select>
            </div>

            <!-- Folio Media -->
            <div>
                <label class="block text-gray-700 font-medium mb-2">Folio Media (*)</label>
                <input
                v-model.number="form.folioMedia"
                type="number"
                min="1"
                placeholder="Ingrese el folio (solo números)"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
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
                <label class="block text-gray-700 font-medium mb-2">Precio sin IVA (*)</label>
                <input
                v-model.number="form.precioSinIVA"
                type="number"
                step="0.01"
                min="0"
                placeholder="0.00"
                required
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
            </div>

            <!-- IVA -->
            <div>
                <label class="block text-gray-700 font-medium mb-2">IVA (%) (*)</label>
                <select
                v-model="form.iva"
                required
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                <option value="">Seleccione</option>
                <option value="0">0</option>
                <option value="8">8</option>
                <option value="16">16</option>
                <option value="19">19</option>
                </select>
            </div>

            <!-- Porcentaje (solo si es Fondo Media) -->
            <div v-if="form.tipoAcuerdo === 'Fondo Media'">
              <label class="block text-gray-700 font-medium mb-3">Porcentaje</label>

              <div class="flex items-center gap-4">
                <!-- Slider -->
                <input
                  type="range"
                  v-model.number="form.porcentaje"
                  min="0.5"
                  max="10"
                  step="0.5"
                  class="w-full accent-pink-600 cursor-pointer"
                />

                <!-- Valor actual -->
                <span class="text-gray-700 font-semibold w-12 text-right">
                  {{ Number(form.porcentaje).toFixed(1) }}%
                </span>
              </div>

              <div class="flex justify-between text-xs text-gray-500 mt-1">
                <span>0.5%</span>
                <span>10%</span>
              </div>
            </div>


            <!-- Tipo (solo si es Fondo Media) -->
            <div v-if="form.tipoAcuerdo === 'Fondo Media'">
                <label class="block text-gray-700 font-medium mb-2">Tipo</label>
                <select
                v-model="form.tipo"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                <option value="">Seleccione tipo</option>
                <option value="Estancias">Estancias</option>
                <option value="Ventas">Ventas</option>
                </select>
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
                type="submit"
                class="bg-gradient-to-r from-yellow-400 via-pink-600 to-sky-500 text-white px-6 py-2 rounded-lg font-semibold shadow-md hover:scale-[1.03] transition-transform"
            >
                Siguiente
            </button>
            </div>
        </form>

        <!-- Notificación -->
        <transition name="fade">
        <div
            v-if="alertaPaso2"
            class="fixed bottom-20 right-6 z-50 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg text-sm"
        >
            {{ alertaPaso2 }}
        </div>
        </transition>

        </div>


        <!-- Paso 3 -->
        <div v-else-if="step === 3">
        <h2 class="text-lg font-semibold text-gray-700 mb-2">
            Paso 3: Periodo del acuerdo
        </h2>
        <p class="text-sm text-gray-500 mb-6">(*) Campos obligatorios</p>

        <form @submit.prevent="validarPaso3" novalidate class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Fecha inicio -->
            <div>
              <label class="block text-gray-700 font-medium mb-2">Fecha de inicio (*)</label>
              <input
                v-model="form.fechaInicio"
                type="date"
                :min="`${currentYear}-01-01`"
                :max="`${currentYear}-12-31`"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <p class="text-xs text-gray-500 mt-1">
                Solo se permiten fechas dentro del año {{ currentYear }}.
              </p>
            </div>


            <!-- Fecha término -->
            <div>
                <label class="block text-gray-700 font-medium mb-2">Fecha de término (*)</label>
                <input
                v-model="form.fechaTermino"
                type="date"
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
                type="submit"
                class="bg-gradient-to-r from-yellow-400 via-pink-600 to-sky-500 text-white px-6 py-2 rounded-lg font-semibold shadow-md hover:scale-[1.03] transition-transform"
            >
                Siguiente
            </button>
            </div>
        </form>

        <!-- Notificación -->
        <transition name="fade">
            <div
            v-if="alertaPaso3"
            class="fixed bottom-20 right-6 z-50 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg text-sm"
            >
            {{ alertaPaso3 }}
            </div>
        </transition>
        </div>


        <!-- Paso 4 -->
        <div v-else-if="step === 4">
        <h2 class="text-lg font-semibold text-gray-700 mb-2">
            Paso 4: Datos de facturación
        </h2>
        <p class="text-sm text-gray-500 mb-6">(*) Campos obligatorios</p>

        <form @submit.prevent="validarPaso4" novalidate class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Comprobante -->
            <div>
                <label class="block text-gray-700 font-medium mb-2">Comprobante (*)</label>
                <select
                v-model="form.comprobante"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                <option value="">Seleccione tipo</option>
                <option value="Factura">Factura</option>
                <option value="Invoice">Invoice</option>
                </select>
            </div>

            <!-- Número de factura -->
            <div>
                <label class="block text-gray-700 font-medium mb-2">Número de factura (*)</label>
                <select
                v-model="form.numeroFactura"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                <option value="">Seleccione número</option>
                <option v-for="n in 12" :key="n" :value="n">{{ n }}</option>
                </select>
            </div>

            <!-- Fecha de facturación -->
            <div>
                <label class="block text-gray-700 font-medium mb-2">Fecha de facturación (*)</label>
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
            <label class="block text-gray-700 font-medium mb-2">Comentarios (máx. 500 caracteres)</label>
            <textarea
                v-model="form.comentarios"
                rows="4"
                maxlength="500"
                placeholder="Ingrese observaciones o detalles adicionales..."
                class="w-full border border-gray-300 rounded-lg px-3 py-2 resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            ></textarea>
            <p class="text-xs text-gray-500 mt-1 text-right">{{ form.comentarios.length }}/500</p>
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
                class="bg-gradient-to-r from-yellow-400 via-pink-600 to-sky-500 text-white px-6 py-2 rounded-lg font-semibold shadow-md hover:scale-[1.03] transition-transform"
            >
                Siguiente
            </button>
            </div>
        </form>

        <!-- Notificación -->
        <transition name="fade">
            <div
            v-if="alertaPaso4"
            class="fixed bottom-20 right-6 z-50 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg text-sm"
            >
            {{ alertaPaso4 }}
            </div>
        </transition>
        </div>


        <!-- Paso 5 -->
        <div v-else-if="step === 5">
        <h2 class="text-lg font-semibold text-gray-700 mb-2">
            Paso 5: Datos del cliente
        </h2>
        <p class="text-sm text-gray-500 mb-6">(*) Campos obligatorios</p>

        <form @submit.prevent="validarPaso5" novalidate class="space-y-8">
            <!-- Cliente o RFC -->
            <div>
            <label class="block text-gray-700 font-medium mb-2">Cliente o RFC (*)</label>
            <div class="flex gap-3">
                <input
                v-model="form.clienteRFC"
                type="text"
                placeholder="Ingrese el cliente o RFC"
                class="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <button
                type="button"
                @click="buscarCliente"
                class="bg-blue-500 text-white px-5 py-2 rounded-lg font-medium hover:bg-blue-600 transition"
                >
                Buscar
                </button>
            </div>
            <p v-if="buscando" class="text-sm text-gray-500 mt-2">Buscando cliente...</p>
            <p v-if="clienteNoEncontrado" class="text-sm text-red-500 mt-2">
                ⚠️ No se encontró ningún cliente con ese RFC.
            </p>
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
                    <label class="block text-gray-700 text-sm font-medium mb-1">Nombre (*)</label>
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
                    <label class="block text-gray-700 text-sm font-medium mb-1">E-mail (*)</label>
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
                    <label class="block text-gray-700 text-sm font-medium mb-1">Nombre (*)</label>
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
                    <label class="block text-gray-700 text-sm font-medium mb-1">E-mail (*)</label>
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
                type="submit"
                class="bg-gradient-to-r from-yellow-400 via-pink-600 to-sky-500 text-white px-6 py-2 rounded-lg font-semibold shadow-md hover:scale-[1.03] transition-transform"
            >
                Siguiente
            </button>
            </div>
        </form>

        <!-- Notificación -->
        <transition name="fade">
            <div
            v-if="alertaPaso5"
            class="fixed bottom-20 right-6 z-50 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg text-sm"
            >
            {{ alertaPaso5 }}
            </div>
        </transition>
        </div>


        <!-- Paso 6 -->
        <div v-else-if="step === 6">
        <h2 class="text-lg font-semibold text-gray-700 mb-2">
            Paso 6: Datos de Hoteles
        </h2>
        <p class="text-sm text-gray-500 mb-6">(*) Campos obligatorios</p>

        <form @submit.prevent="validarPaso6" novalidate class="space-y-6">
            <!-- Tipo de selección -->
            <div>
            <label class="block text-gray-700 font-medium mb-2">Tipo de acuerdo con hotel (*)</label>
            <select
                v-model="form.tipoHotel"
                @change="resetSeleccion"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
                <option value="">Seleccione tipo</option>
                <option value="Corporativo">Corporativo</option>
                <option value="Individual">Individual</option>
            </select>
            </div>

            <!-- Si es Corporativo -->
            <div v-if="form.tipoHotel === 'Corporativo'" class="mt-4">
            <label class="block text-gray-700 font-medium mb-2">Seleccione corporativo (*)</label>
            <select
                v-model="corporativoSeleccionado"
                @change="buscarHotelesCorporativo"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
                <option value="">Seleccione una cadena o grupo hotelero</option>
                <option v-for="nombre in corporativosDisponibles" :key="nombre" :value="nombre">
                {{ nombre }}
                </option>
            </select>
            </div>

            <!-- Si es Individual -->
            <!-- Si es Individual -->
            <div v-if="form.tipoHotel === 'Individual'" class="mt-4 space-y-4">
              <h3 class="text-gray-700 font-medium mb-3">Filtros de búsqueda</h3>

              <!-- Gerente -->
              <div>
                <label class="block text-gray-700 font-medium mb-2">Gerente</label>
                <select
                  v-model="filtroGerente"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Seleccione un gerente</option>
                  <option v-for="nombre in listaGerentes" :key="nombre" :value="nombre">
                    {{ nombre }}
                  </option>
                </select>
              </div>

              <!-- MarketRPC -->
              <div>
                <label class="block text-gray-700 font-medium mb-2">MarketRPC</label>
                <input
                  v-model="filtroMarket"
                  type="text"
                  placeholder="Ingrese el MarketRPC..."
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <!-- Destino -->
              <div>
                <label class="block text-gray-700 font-medium mb-2">Destino</label>
                <input
                  v-model="filtroDestino"
                  type="text"
                  placeholder="Ingrese el destino..."
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <!-- Botón de búsqueda -->
              <div class="flex justify-end mt-4">
                <button
                  type="button"
                  @click="buscarHotelesIndividual"
                  class="bg-blue-500 text-white px-6 py-2 rounded-lg text-sm font-medium hover:bg-blue-600 transition"
                >
                  Buscar
                </button>
              </div>
            </div>


            <!-- Tabla de resultados -->
            <div v-if="hotelesFiltrados.length" class="mt-6 overflow-x-auto">
            <table class="min-w-full border border-gray-200 rounded-lg">
                <thead class="bg-gray-100 text-gray-700">
                <tr>
                    <th class="px-4 py-2 border-b text-left">
                    <input type="checkbox" v-model="seleccionarTodos" @change="toggleTodos" class="w-4 h-4" />
                    <span class="ml-2 font-medium">Todo</span>
                    </th>
                    <th class="px-4 py-2 border-b">ID Hotel</th>
                    <th class="px-4 py-2 border-b">Hotel</th>
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

            <!-- Sin resultados -->
            <div
            v-else-if="form.tipoHotel && !buscandoHoteles && !hotelesFiltrados.length"
            class="text-gray-500 text-sm mt-4"
            >
            ⚠️ No se encontraron resultados.
            </div>

            <div v-if="buscandoHoteles" class="text-sm text-gray-500 mt-4">
            Buscando hoteles...
            </div>

            <!-- Botones -->
            <div class="flex justify-between mt-8 pt-6 border-t border-gray-200">
            <button
                type="button"
                @click="prevStep"
                class="px-6 py-2 rounded-lg border border-gray-300 text-gray-700 font-medium hover:border-blue-400 hover:text-blue-600 transition"
            >
                Anterior
            </button>

            <button
                type="submit"
                class="bg-gradient-to-r from-yellow-400 via-pink-600 to-sky-500 text-white px-6 py-2 rounded-lg font-semibold shadow-md hover:scale-[1.03] transition-transform"
            >
                Siguiente
            </button>
            </div>
        </form>

        <!-- Notificación -->
        <transition name="fade">
            <div
            v-if="alertaPaso6"
            class="fixed bottom-20 right-6 z-50 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg text-sm"
            >
            {{ alertaPaso6 }}
            </div>
        </transition>
        </div>


      <!-- Paso 7 -->
      <div v-else-if="step === 7" class="text-center">
        <h2 class="text-lg font-semibold text-gray-700 mb-2">
          Paso 7: Confirmación final
        </h2>
        <p class="text-sm text-gray-500 mb-10">
          Revise los datos antes de finalizar el acuerdo.
        </p>

        <!-- Si subió un archivo -->
        <div v-if="selectedOption === 'upload'" class="flex flex-col items-center space-y-6">
          <h3 class="text-md font-semibold text-gray-700 mb-2">📎 Subir archivo del acuerdo</h3>

          <!-- Campo para subir archivo -->
          <div
            class="w-full md:w-3/4 lg:w-2/3 bg-gray-50 border-2 border-dashed border-gray-300 p-8 rounded-xl hover:border-blue-400 transition"
          >
            <input
              type="file"
              accept="application/pdf,image/png"
              @change="manejarArchivo"
              class="block w-full text-sm text-gray-600 cursor-pointer"
            />

            <!-- Vista previa -->
            <div v-if="filePreview" class="mt-6">
              <h4 class="font-medium text-gray-700 mb-3">Vista previa:</h4>

              <div v-if="fileType === 'application/pdf'">
                <iframe
                  :src="filePreview"
                  class="w-full h-[600px] rounded-lg border"
                  title="Vista previa del PDF"
                ></iframe>
              </div>

              <div v-else-if="fileType === 'image/png'">
                <img
                  :src="filePreview"
                  alt="Vista previa del acuerdo"
                  class="mx-auto max-h-[600px] rounded-lg shadow-md"
                />
              </div>
            </div>
          </div>

          <!-- NUEVO BLOQUE: Confirmación de validación -->
          <div class="mt-8 bg-gray-50 border border-gray-200 rounded-lg p-6 w-full md:w-3/4 lg:w-2/3">
            <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <label class="flex items-center gap-3 text-gray-700">
                <input
                  type="checkbox"
                  v-model="datosValidados"
                  class="w-5 h-5 accent-pink-600"
                />
                <span class="text-sm sm:text-base">
                  Confirmo que los datos fueron validados y capturados correctamente.
                </span>
              </label>

              <!-- Enlace de validación (si no marca la casilla) -->
              <div v-if="!datosValidados" class="text-sm text-pink-600 underline cursor-pointer hover:text-pink-700" @click="irAValidar">
                🔍 Validar datos
              </div>
            </div>
          </div>

          <!-- Ver detalles -->
          <button
            type="button"
            @click="mostrarModal = true"
            class="mt-4 bg-blue-500 text-white px-6 py-2 rounded-lg font-semibold hover:bg-blue-600 transition"
          >
            Ver detalles del acuerdo
          </button>
        </div>

        <!-- Si eligió generar PDF -->
        <div v-else-if="form.tipoSeleccion === 'pdf'" class="flex flex-col items-center space-y-6">
          <h3 class="text-md font-semibold text-gray-700 mb-2">📝 Acuerdo generado</h3>
          <button
            type="button"
            @click="generarPDFReal"
            class="bg-blue-500 text-white px-6 py-2 rounded-lg font-semibold shadow-md hover:bg-blue-600 transition"
          >
            🧾 Generar PDF del acuerdo
          </button>

          <div v-if="pdfRealUrl" class="w-full md:w-3/4 lg:w-2/3 mt-6 bg-gray-100 p-4 rounded-lg shadow-inner">
            <iframe
              :src="pdfRealUrl"
              class="w-full h-[600px] rounded-lg border"
              title="PDF del acuerdo generado"
            ></iframe>

            <a
              :href="pdfRealUrl"
              download="acuerdo.pdf"
              class="inline-block mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              Descargar PDF
            </a>
          </div>

          <button
            type="button"
            @click="mostrarModal = true"
            class="mt-4 bg-gray-200 text-gray-700 px-6 py-2 rounded-lg font-semibold hover:bg-gray-300 transition"
          >
            Ver detalles del acuerdo
          </button>
        </div>

        <!-- Botones navegación -->
        <div class="flex justify-center mt-10 gap-6">
          <button
            type="button"
            @click="prevStep"
            class="px-6 py-2 rounded-lg border border-gray-300 text-gray-700 font-medium hover:border-blue-400 hover:text-blue-600 transition"
          >
            Anterior
          </button>

          <!-- Botón final dinámico -->
          <button
            type="button"
            @click="finalizarAcuerdo"
            :disabled="selectedOption === 'upload' && !datosValidados"
            class="bg-gradient-to-r from-yellow-400 via-pink-600 to-sky-500 text-white px-6 py-2 rounded-lg font-semibold shadow-md hover:scale-[1.03] transition-transform disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ form.tipoSeleccion === 'upload' ? 'Subir' : 'Generar' }}
          </button>
        </div>

          <!-- Modal detalles -->
          <transition name="fade">
            <div
              v-if="mostrarModal"
              class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
            >
              <div
                class="bg-white rounded-xl shadow-lg w-11/12 md:w-2/3 lg:w-2/3 p-8 relative max-h-[80vh] overflow-y-auto"
              >
                <button
                  @click="mostrarModal = false"
                  class="absolute top-4 right-4 text-gray-500 hover:text-gray-700 text-xl"
                >
                  ✖
                </button>

                <h3 class="text-lg font-semibold text-gray-700 mb-6 text-center">
                  Detalles del Acuerdo
                </h3>

                <!-- Información general -->
                <div class="space-y-8">
                  <!-- Datos generales -->
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-2 text-left">
                    <p><strong>Equipo:</strong> {{ form.equipo }}</p>
                    <p><strong>Tipo de acuerdo:</strong> {{ form.tipoAcuerdo }}</p>

                    <p><strong>Moneda:</strong> {{ form.moneda }}</p>
                    <p><strong>IVA:</strong> {{ form.iva ? form.iva + '%' : '—' }}</p>

                    <p><strong>Precio sin IVA:</strong> {{ formatMoney(form.precioSinIVA, form.moneda) }}</p>
                    <p v-if="form.tipoAcuerdo === 'Fondo Media'">
                      <strong>Porcentaje (FM):</strong> {{ form.porcentaje ? form.porcentaje + '%' : '—' }}
                    </p>

                    <p><strong>Fecha inicio:</strong> {{ formatDate(form.fechaInicio) }}</p>
                    <p><strong>Fecha término:</strong> {{ formatDate(form.fechaTermino) }}</p>

                    <p><strong>Folio Media:</strong> {{ form.folioMedia || '—' }}</p>
                    <p v-if="form.tipoAcuerdo === 'Fondo Media'">
                      <strong>Tipo (FM):</strong> {{ form.tipo || '—' }}
                    </p>

                    <p><strong>Comprobante:</strong> {{ form.comprobante || '—' }}</p>
                    <p><strong>Núm. factura:</strong> {{ form.numeroFactura || '—' }}</p>

                    <p><strong>Fecha facturación:</strong> {{ formatDate(form.fechaFacturacion) }}</p>
                    <p><strong>Forma de pago:</strong> {{ form.formaPago || '—' }}</p>

                    <p class="md:col-span-2"><strong>Cliente/RFC:</strong> {{ form.clienteRFC }}</p>
                    <p class="md:col-span-2"><strong>Tipo hotel:</strong> {{ form.tipoHotel || '—' }}</p>

                    <p v-if="form.tipoHotel === 'Corporativo'" class="md:col-span-2">
                      <strong>Corporativo seleccionado:</strong> {{ corporativoSeleccionado || '—' }}
                    </p>

                    <!-- Comentarios -->
                    <div class="md:col-span-2 mt-2">
                      <strong>Comentarios:</strong>
                      <div
                        class="mt-1 whitespace-pre-wrap text-gray-700 border border-gray-200 rounded-md p-3 bg-gray-50"
                      >
                        {{ form.comentarios || '—' }}
                      </div>
                    </div>
                  </div>

                  <!-- Hoteles seleccionados -->
                  <div>
                    <h4 class="font-semibold text-gray-700 mb-2 border-b pb-1">Hoteles seleccionados</h4>
                    <div v-if="hotelesSeleccionados.length">
                      <ul class="list-disc pl-6 space-y-1">
                        <li v-for="h in hotelesSeleccionados" :key="h.id">
                          <span class="font-medium">#{{ h.id }}</span> — {{ h.nombre }}
                        </li>
                      </ul>
                    </div>
                    <p v-else class="text-gray-500">No hay hoteles seleccionados.</p>
                  </div>

                  <!-- Contactos -->
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
                    <div>
                      <h4 class="font-semibold text-gray-700 mb-3 border-b pb-1">Contacto Contabilidad</h4>
                      <p><strong>Nombre:</strong> {{ form.contabilidadNombre || '—' }}</p>
                      <p><strong>Cargo:</strong> {{ form.contabilidadCargo || '—' }}</p>
                      <p><strong>E-mail:</strong> {{ form.contabilidadEmail || '—' }}</p>
                      <p><strong>Teléfono:</strong> {{ form.contabilidadTelefono || '—' }}</p>
                    </div>

                    <div>
                      <h4 class="font-semibold text-gray-700 mb-3 border-b pb-1">Contacto Marketing</h4>
                      <p><strong>Nombre:</strong> {{ form.marketingNombre || '—' }}</p>
                      <p><strong>Cargo:</strong> {{ form.marketingCargo || '—' }}</p>
                      <p><strong>E-mail:</strong> {{ form.marketingEmail || '—' }}</p>
                      <p><strong>Teléfono:</strong> {{ form.marketingTelefono || '—' }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </transition>

          <!-- Notificación de éxito -->
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
/* =====================================================
   📦 IMPORTS Y CONFIGURACIÓN INICIAL
===================================================== */
import Header from '~/components/Layout/Header.vue'
import Footer from '~/components/Layout/FooterBar.vue'
import { useRouter } from 'vue-router'

const router = useRouter()


/* =====================================================
   🧩 VARIABLES GLOBALES / ESTADO PRINCIPAL
===================================================== */
const step = ref(1)
const selectedOption = ref<string | null>(null)
const fileName = ref<string | null>(null)
const fileType = ref('')
const filePreview = ref('')
const mensajeExito = ref('')
const mostrarModal = ref(false)


/* =====================================================
   📝 FORMULARIO REACTIVO PRINCIPAL
===================================================== */
const form = reactive({
  tipoSeleccion: '',
  // Paso 2
  equipo: '',
  tipoAcuerdo: '',
  folioMedia: '',
  moneda: '',
  precioSinIVA: '',
  iva: '',
  porcentaje: 0, // antes estaba como string vacío ''
  tipo: '',
  // Paso 3
  fechaInicio: '',
  fechaTermino: '',
  // Paso 4
  comprobante: '',
  numeroFactura: '',
  fechaFacturacion: '',
  formaPago: '',
  comentarios: '',
  // Paso 5
  clienteRFC: '',
  contabilidadNombre: '',
  contabilidadCargo: '',
  contabilidadEmail: '',
  contabilidadTelefono: '',
  marketingNombre: '',
  marketingCargo: '',
  marketingEmail: '',
  marketingTelefono: '',
  // Paso 6
  tipoHotel: '',
})


/* =====================================================
   ⚙️ UTILIDADES GLOBALES (formateo, helpers)
===================================================== */
const formatDate = (iso?: string) => {
  if (!iso) return '—'
  const d = new Date(iso)
  if (isNaN(d.getTime())) return iso
  return d.toLocaleDateString('es-MX', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

const formatMoney = (val: any, currency = 'MXN') => {
  const num = Number(val)
  if (isNaN(num)) return val || '—'
  try {
    return new Intl.NumberFormat('es-MX', {
      style: 'currency',
      currency
    }).format(num)
  } catch {
    return num.toLocaleString('es-MX')
  }
}


/* =====================================================
   🧾 PASO 1 – Subir acuerdo o generar PDF
===================================================== */
const alertaPaso1 = ref('')

// Estado del tipo de carga
const tipoCarga = ref('nuevo')
const acuerdoSeleccionado = ref('')
const acuerdosPendientes = ref([
  { id: '339398', data: { clienteRFC: 'MXC123456789', equipo: 'RCP México', tipoAcuerdo: 'Fondo Media', moneda: 'MXN', precioSinIVA: '10000', iva: '16', porcentaje: '10', tipo: 'Estancias', fechaInicio: '2025-01-01', fechaTermino: '2025-06-30', comprobante: 'Factura', numeroFactura: '1', fechaFacturacion: '2025-01-15', formaPago: 'Transferencia', comentarios: 'Acuerdo pendiente migrado.', contabilidadNombre: 'Laura Gómez', contabilidadEmail: 'laura.gomez@pricetravel.com', marketingNombre: 'Carlos Herrera', marketingEmail: 'carlos.herrera@pricetravel.com', tipoHotel: 'Individual' }},
  { id: '47474', data: { clienteRFC: 'CO123456789', equipo: 'RCP Colombia', tipoAcuerdo: 'Paquete Fijo', moneda: 'COP', precioSinIVA: '50000000', iva: '19', fechaInicio: '2025-02-01', fechaTermino: '2025-07-31', comprobante: 'Invoice', numeroFactura: '2', formaPago: 'Descuento', comentarios: 'Campaña Colombia Q1.' }}
])

const cargarDatosAcuerdo = () => {
  const acuerdo = acuerdosPendientes.value.find(a => a.id === acuerdoSeleccionado.value)
  if (!acuerdo) return

  // Carga los datos en el formulario
  Object.assign(form, acuerdo.data)

  // Alerta opcional visual
  alert(`✅ Acuerdo ${acuerdoSeleccionado.value} cargado exitosamente.`)

  // 🔁 Salta directamente al paso 7
  step.value = 7
}


/* =====================================================
   🧮 PASO 2 – Detalles del acuerdo
===================================================== */
const alertaPaso2 = ref('')

const handleTipoAcuerdo = () => {
  if (form.tipoAcuerdo !== 'Fondo Media') {
    form.porcentaje = ''
    form.tipo = ''
  }
}

const validarPaso2 = () => {
  if (
    !form.equipo ||
    !form.tipoAcuerdo ||
    !form.folioMedia ||
    !form.moneda ||
    !form.precioSinIVA ||
    !form.iva
  ) {
    alertaPaso2.value = '⚠️ Por favor llena todos los campos obligatorios.'
    setTimeout(() => (alertaPaso2.value = ''), 3000)
    return
  }

  if (form.tipoAcuerdo === 'Fondo Media' && (!form.porcentaje || !form.tipo)) {
    alertaPaso2.value = '⚠️ Por favor selecciona porcentaje y tipo para Fondo Media.'
    setTimeout(() => (alertaPaso2.value = ''), 3000)
    return
  }

  nextStep()
}


/* =====================================================
   📅 PASO 3 – Periodo del acuerdo
===================================================== */
const alertaPaso3 = ref('')
// Año actual (para limitar fecha de inicio)
const currentYear = new Date().getFullYear()


const validarPaso3 = () => {
  if (!form.fechaInicio || !form.fechaTermino) {
    alertaPaso3.value = '⚠️ Por favor llena ambos campos de fecha.'
    setTimeout(() => (alertaPaso3.value = ''), 3000)
    return
  }

  if (new Date(form.fechaTermino) < new Date(form.fechaInicio)) {
    alertaPaso3.value = '⚠️ La fecha de término no puede ser anterior a la de inicio.'
    setTimeout(() => (alertaPaso3.value = ''), 3000)
    return
  }

  nextStep()
}


/* =====================================================
   💰 PASO 4 – Datos de facturación
===================================================== */
const alertaPaso4 = ref('')

const validarPaso4 = () => {
  if (!form.comprobante || !form.numeroFactura || !form.fechaFacturacion || !form.formaPago) {
    alertaPaso4.value = '⚠️ Completa todos los campos obligatorios.'
    setTimeout(() => (alertaPaso4.value = ''), 3000)
    return
  }

  nextStep()
}


/* =====================================================
   👥 PASO 5 – Datos del cliente
===================================================== */
const alertaPaso5 = ref('')
const buscando = ref(false)
const clienteNoEncontrado = ref(false)

const validarPaso5 = () => {
  if (!form.clienteRFC) {
    alertaPaso5.value = '⚠️ Ingresa un cliente o RFC antes de continuar.'
    setTimeout(() => (alertaPaso5.value = ''), 3000)
    return
  }

  if (!form.contabilidadNombre || !form.contabilidadEmail || !form.marketingNombre || !form.marketingEmail) {
    alertaPaso5.value = '⚠️ Completa los campos obligatorios (Nombre y E-mail) en ambos contactos.'
    setTimeout(() => (alertaPaso5.value = ''), 3000)
    return
  }

  nextStep()
}

const buscarCliente = () => {
  if (!form.clienteRFC) {
    alertaPaso5.value = '⚠️ Ingresa un RFC para buscar.'
    setTimeout(() => (alertaPaso5.value = ''), 3000)
    return
  }

  buscando.value = true
  clienteNoEncontrado.value = false

  setTimeout(() => {
    if (form.clienteRFC.toLowerCase() === 'pricetravel123') {
      form.contabilidadNombre = 'Laura Gómez'
      form.contabilidadCargo = 'Contadora General'
      form.contabilidadEmail = 'laura.gomez@pricetravel.com'
      form.contabilidadTelefono = '+52 998 222 3344'
      form.marketingNombre = 'Carlos Herrera'
      form.marketingCargo = 'Gerente de Marketing'
      form.marketingEmail = 'carlos.herrera@pricetravel.com'
      form.marketingTelefono = '+52 998 111 2233'
    } else {
      clienteNoEncontrado.value = true
      Object.assign(form, {
        contabilidadNombre: '',
        contabilidadCargo: '',
        contabilidadEmail: '',
        contabilidadTelefono: '',
        marketingNombre: '',
        marketingCargo: '',
        marketingEmail: '',
        marketingTelefono: ''
      })
    }
    buscando.value = false
  }, 1200)
}


/* =====================================================
   🏨 PASO 6 – Datos de hoteles
===================================================== */
const alertaPaso6 = ref('')
const seleccionarTodos = ref(false)
const corporativoSeleccionado = ref('')
const buscandoHoteles = ref(false)
const busquedaHotel = ref('')
// 🔍 Filtros Individual
const filtroGerente = ref('')
const filtroMarket = ref('')
const filtroDestino = ref('')
const datosValidados = ref(false)

const irAValidar = () => {
  datosValidados.value = false
  step.value = 2
  window.scrollTo({ top: 0, behavior: 'smooth' })
}


const listaGerentes = [
  'Laura Gómez',
  'Carlos Herrera',
  'Andrea López',
  'Fernando Díaz',
  'Sofía Martínez',
  'José Ramírez'
]


const corporativosDisponibles = [ "AA-Independent", "Accor", "Akela", "Alsol", "Americas Hotels Group", "Aristos", "Ayenda Hoteles", "B&B Hoteles", "Bahia Principe", "Barcelo", "Be Live", "Belmond", "Best Western", "BH Hoteles", "Blue Doors", "Blue Tree", "BlueBay", "Böëna Wilderness Lodge", "Bourbon", "Caesars Entertainment", "Camino Real", "Carimundi", "Casa Andina", "Catalonia", "CHL Suites", "CHOICE", "Costa del Sol", "Daniel Reyes", "Dann", "Decameron", "Disney", "Dorado Plaza", "DOT Hotels", "El Dorado San Andrés", "EM Hotels", "Emporio", "Enjoy Cuba", "ePhoneix", "Estelar", "Eurostars Hotels", "Fairmont", "Faranda Hotels", "Fasano", "Fontan", "GHL", "Grupo Habita", "Grupo Milenium", "GRUPO POSADAS", "Grupo Welcome", "Hardrock", "Havanatur / Tainotur", "Hilton", "HM Hotels", "Hotel Gallery", "Hoteles Cosmos", "Hoteles Geh Suites", "Hoteles Movich", "Hoteles San Agustin", "Hoteles Solar", "Hoteles Xcaret", "Hotusa Hotels", "Hover Tours", "Hyatt", "Hyatt Inclusive Collection", "Iberostar", "IHG", "Intercity", "Islander Collection", "Karisma", "Krystal", "LAHRES", "Las Brisas", "Latour", "Lomas Hospitality", "Louvre Hotels Group", "Lucerna", "Marival", "Marriott", "MasHoteles", "Mayan Palace", "Melia", "MGM Resorts", "Mision", "MS Hoteles", "NH", "Oasis", "Ocean by H10", "Oetker Collection", "Omni", "On Vacation", "Operadora SI", "Original Resorts", "Ostar", "Oxo Hotel", "Oyo Rooms", "Palace", "Palladium Hotel Group", "Park Royal", "Playa Resorts", "PortoBay", "Presidente Intercontinental", "Prisma Hoteles", "Proturs", "Pueblo Bonito", "RCD HOTELS", "Regency & Santorini", "RIU", "Rosewood Hotels", "Royalton Hotels & Resorts", "Sandals", "Sandos", "Selina", "Sercotel", "Sonesta", "Station Casinos", "The Cayuga Collection", "The Q Project", "Travelers", "Universal", "Velas Resorts", "Viaggio", "Vila Galé", "Villa Group", "Wyndham", "Wynn Las Vegas", "Zar", "Zona Estrategica" ];

const hotelesIndividuales = [
  { id: 101, nombre: "Hotel Riviera", seleccionado: false },
  { id: 102, nombre: "Hotel Playa Azul", seleccionado: false },
  { id: 103, nombre: "Hotel Costa Maya", seleccionado: false },
  { id: 104, nombre: "Hotel San José", seleccionado: false },
]

const hotelesCorporativos = [
  { id: 1, nombre: "RIU Cancun", seleccionado: false },
  { id: 2, nombre: "RIU Palace", seleccionado: false },
  { id: 3, nombre: "RIU Caribe", seleccionado: false },
  { id: 4, nombre: "RIU Plaza", seleccionado: false },
]

const hotelesFiltrados = ref([])

const resetSeleccion = () => {
  seleccionarTodos.value = false
  hotelesFiltrados.value = []
  corporativoSeleccionado.value = ''
  busquedaHotel.value = ''
}

const buscarHotelesCorporativo = () => {
  if (!corporativoSeleccionado.value) return
  buscandoHoteles.value = true
  setTimeout(() => {
    hotelesFiltrados.value = [...hotelesCorporativos]
    buscandoHoteles.value = false
  }, 800)
}

const buscarHotelesIndividual = () => {
  if (!filtroGerente.value && !filtroMarket.value && !filtroDestino.value) {
    alertaPaso6.value = '⚠️ Ingresa al menos un filtro (Gerente, MarketRPC o Destino).'
    setTimeout(() => (alertaPaso6.value = ''), 3000)
    return
  }

  buscandoHoteles.value = true
  hotelesFiltrados.value = [] // Limpia antes de buscar

  setTimeout(() => {
    // Simulación de búsqueda local (puedes conectar a backend después)
    hotelesFiltrados.value = hotelesIndividuales.filter(h => {
      const matchGerente = filtroGerente.value ? h.nombre.includes('Hotel') : true
      const matchMarket = filtroMarket.value ? true : true // Simulado
      const matchDestino = filtroDestino.value ? true : true // Simulado
      return matchGerente && matchMarket && matchDestino
    })

    buscandoHoteles.value = false

    if (!hotelesFiltrados.value.length) {
      alertaPaso6.value = '⚠️ No se encontraron hoteles con esos filtros.'
      setTimeout(() => (alertaPaso6.value = ''), 3000)
    }
  }, 1000)
}


const toggleTodos = () => {
  hotelesFiltrados.value.forEach(h => (h.seleccionado = seleccionarTodos.value))
}

const hotelesSeleccionados = computed(() =>
  hotelesFiltrados.value.filter(h => h.seleccionado)
)

const validarPaso6 = () => {
  if (!form.tipoHotel) {
    alertaPaso6.value = '⚠️ Selecciona el tipo de acuerdo con hotel.'
    setTimeout(() => (alertaPaso6.value = ''), 3000)
    return
  }
  const seleccionados = hotelesFiltrados.value.filter(h => h.seleccionado)
  if (seleccionados.length === 0) {
    alertaPaso6.value = '⚠️ Debes seleccionar al menos un hotel.'
    setTimeout(() => (alertaPaso6.value = ''), 3000)
    return
  }
  nextStep()
}

/* =====================================================
   🚀 PASO 7 – Confirmación final
===================================================== */
import { generarAcuerdoPDF } from '~/utils/generarAcuerdoPDF'

const pdfPreviewUrl = ref<string | null>(null)
const pdfRealUrl = ref<string | null>(null)

/**
 * Genera el PDF principal (acuerdo final)
 */
const generarPDFReal = async () => {
  try {
    const resp = await fetch('http://localhost:5001/api/pdf/acuerdo-detalle', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...form,
        hoteles: hotelesSeleccionados.value
      })
    });

    if (!resp.ok) {
      throw new Error("Error generando PDF");
    }

    const blob = await resp.blob();
    pdfRealUrl.value = URL.createObjectURL(blob);

    mensajeExito.value = "📄 PDF generado correctamente.";
    setTimeout(() => (mensajeExito.value = ""), 2500);
  } catch (error) {
    console.error("❌ Error generando PDF:", error);
    mensajeExito.value = "❌ No se pudo generar el PDF.";
    setTimeout(() => (mensajeExito.value = ""), 2500);
  }
};



/**
 * Termina el flujo del acuerdo (guarda o redirige)
 */
const finalizarAcuerdo = async () => {
  console.log('🧾 Entrando a finalizarAcuerdo con opción:', form.tipoSeleccion)

  if (form.tipoSeleccion === 'pdf') {
    // Si ya generó PDF, muestra mensaje y redirige
    if (pdfRealUrl.value) {
      mensajeExito.value = '✅ Acuerdo generado correctamente.'
      setTimeout(() => router.push('/home'), 1500)
    } else {
      // Si aún no hay PDF generado, sugiere al usuario hacerlo antes
      mensajeExito.value = '⚠️ Primero genera el PDF del acuerdo.'
      setTimeout(() => (mensajeExito.value = ''), 3000)
    }
  } else {
    // Caso: el usuario subió un archivo
    mensajeExito.value = '✅ Acuerdo creado con éxito.'
    setTimeout(() => router.push('/home'), 1500)
  }
}


// 📂 Manejo del archivo subido
const manejarArchivo = (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  fileName.value = file.name
  fileType.value = file.type
  filePreview.value = URL.createObjectURL(file)

  console.log('📁 Archivo seleccionado:', file.name, file.type)
}



/* =====================================================
   🧭 NAVEGACIÓN ENTRE PASOS
===================================================== */
const nextStep = () => { if (step.value < 7) step.value++ }
const prevStep = () => { if (step.value > 1) step.value-- }
const submitForm = () => alert(`✅ Datos guardados.\nPaso actual: ${step.value}`)
</script>
