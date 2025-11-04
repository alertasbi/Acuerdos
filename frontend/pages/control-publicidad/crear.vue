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
            accept=".pdf,.png"
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
                <label class="block text-gray-700 font-medium mb-2">Porcentaje</label>
                <select
                v-model="form.porcentaje"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                <option value="">Seleccione porcentaje</option>
                <option v-for="n in 10" :key="n" :value="n">{{ n }}%</option>
                </select>
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
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
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
            <div v-if="form.tipoHotel === 'Individual'" class="mt-4">
            <label class="block text-gray-700 font-medium mb-2">ID o Nombre del hotel (*)</label>
            <input
                v-model="busquedaHotel"
                @keyup.enter="buscarHotelesIndividual"
                type="text"
                placeholder="Ejemplo: 100101, Hotel1, Hotel2"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <p class="text-xs text-gray-500 mt-1">
                Usar comas (,) como separador para búsquedas avanzadas. Ejemplo: 100101, Hotel1, 123456.
            </p>
            <div class="flex justify-end mt-2">
                <button
                type="button"
                @click="buscarHotelesIndividual"
                class="bg-blue-500 text-white px-5 py-1 rounded-lg text-sm hover:bg-blue-600 transition"
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


const alertaPaso2 = ref('')

const handleTipoAcuerdo = () => {
  // Limpia porcentaje y tipo si cambia a Paquete Fijo
  if (form.tipoAcuerdo !== 'Fondo Media') {
    form.porcentaje = ''
    form.tipo = ''
  }
}

const validarPaso2 = () => {
  // Verifica campos obligatorios
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

  // Si es Fondo Media, validar también porcentaje y tipo
  if (form.tipoAcuerdo === 'Fondo Media' && (!form.porcentaje || !form.tipo)) {
    alertaPaso2.value = '⚠️ Por favor selecciona porcentaje y tipo para Fondo Media.'
    setTimeout(() => (alertaPaso2.value = ''), 3000)
    return
  }

  // Si pasa validación, sigue al siguiente paso
  nextStep()
}

const alertaPaso3 = ref('')

const validarPaso3 = () => {
  if (!form.fechaInicio || !form.fechaTermino) {
    alertaPaso3.value = '⚠️ Por favor llena ambos campos de fecha antes de continuar.'
    setTimeout(() => (alertaPaso3.value = ''), 3000)
    return
  }

  // Validar que la fecha final sea posterior o igual a la inicial
  if (new Date(form.fechaTermino) < new Date(form.fechaInicio)) {
    alertaPaso3.value = '⚠️ La fecha de término no puede ser anterior a la fecha de inicio.'
    setTimeout(() => (alertaPaso3.value = ''), 3000)
    return
  }

  nextStep()
}

const alertaPaso4 = ref('')

const validarPaso4 = () => {
  if (
    !form.comprobante ||
    !form.numeroFactura ||
    !form.fechaFacturacion ||
    !form.formaPago
  ) {
    alertaPaso4.value = '⚠️ Por favor llena todos los campos obligatorios antes de continuar.'
    setTimeout(() => (alertaPaso4.value = ''), 3000)
    return
  }

  nextStep()
}

const alertaPaso5 = ref('')
const buscando = ref(false)
const clienteNoEncontrado = ref(false)

const validarPaso5 = () => {
  if (!form.clienteRFC) {
    alertaPaso5.value = '⚠️ Por favor ingresa un cliente o RFC antes de continuar.'
    setTimeout(() => (alertaPaso5.value = ''), 3000)
    return
  }

  if (!form.contabilidadNombre || !form.contabilidadEmail || !form.marketingNombre || !form.marketingEmail) {
    alertaPaso5.value = '⚠️ Por favor completa los campos obligatorios (Nombre y E-mail) en ambos contactos.'
    setTimeout(() => (alertaPaso5.value = ''), 3000)
    return
  }

  nextStep()
}

// 🔍 Simulación de búsqueda ficticia
const buscarCliente = () => {
  if (!form.clienteRFC) {
    alertaPaso5.value = '⚠️ Ingresa un RFC para realizar la búsqueda.'
    setTimeout(() => (alertaPaso5.value = ''), 3000)
    return
  }

  buscando.value = true
  clienteNoEncontrado.value = false

  setTimeout(() => {
    // cliente simulado
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
      form.contabilidadNombre = ''
      form.contabilidadCargo = ''
      form.contabilidadEmail = ''
      form.contabilidadTelefono = ''
      form.marketingNombre = ''
      form.marketingCargo = ''
      form.marketingEmail = ''
      form.marketingTelefono = ''
    }

    buscando.value = false
  }, 1200)
}

const alertaPaso6 = ref('')
const seleccionarTodos = ref(false)
const corporativoSeleccionado = ref('')
const buscandoHoteles = ref(false)
const busquedaHotel = ref('')


const corporativosDisponibles = [
  "AA-Independent", "Accor", "Akela", "Alsol", "Americas Hotels Group",
  "Aristos", "Ayenda Hoteles", "B&B Hoteles", "Bahia Principe", "Barcelo",
  "Be Live", "Belmond", "Best Western", "BH Hoteles", "Blue Doors",
  "Blue Tree", "BlueBay", "Böëna Wilderness Lodge", "Bourbon", "Caesars Entertainment",
  "Camino Real", "Carimundi", "Casa Andina", "Catalonia", "CHL Suites",
  "CHOICE", "Costa del Sol", "Daniel Reyes", "Dann", "Decameron",
  "Disney", "Dorado Plaza", "DOT Hotels", "El Dorado San Andrés", "EM Hotels",
  "Emporio", "Enjoy Cuba", "ePhoneix", "Estelar", "Eurostars Hotels",
  "Fairmont", "Faranda Hotels", "Fasano", "Fontan", "GHL",
  "Grupo Habita", "Grupo Milenium", "GRUPO POSADAS", "Grupo Welcome", "Hardrock",
  "Havanatur / Tainotur", "Hilton", "HM Hotels", "Hotel Gallery", "Hoteles Cosmos",
  "Hoteles Geh Suites", "Hoteles Movich", "Hoteles San Agustin", "Hoteles Solar",
  "Hoteles Xcaret", "Hotusa Hotels", "Hover Tours", "Hyatt", "Hyatt Inclusive Collection",
  "Iberostar", "IHG", "Intercity", "Islander Collection", "Karisma",
  "Krystal", "LAHRES", "Las Brisas", "Latour", "Lomas Hospitality",
  "Louvre Hotels Group", "Lucerna", "Marival", "Marriott", "MasHoteles",
  "Mayan Palace", "Melia", "MGM Resorts", "Mision", "MS Hoteles",
  "NH", "Oasis", "Ocean by H10", "Oetker Collection", "Omni",
  "On Vacation", "Operadora SI", "Original Resorts", "Ostar", "Oxo Hotel",
  "Oyo Rooms", "Palace", "Palladium Hotel Group", "Park Royal", "Playa Resorts",
  "PortoBay", "Presidente Intercontinental", "Prisma Hoteles", "Proturs", "Pueblo Bonito",
  "RCD HOTELS", "Regency & Santorini", "RIU", "Rosewood Hotels", "Royalton Hotels & Resorts",
  "Sandals", "Sandos", "Selina", "Sercotel", "Sonesta",
  "Station Casinos", "The Cayuga Collection", "The Q Project", "Travelers", "Universal",
  "Velas Resorts", "Viaggio", "Vila Galé", "Villa Group", "Wyndham",
  "Wynn Las Vegas", "Zar", "Zona Estrategica"
];


// Simulados (deberán venir desde API)
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

// 🔍 Buscar hoteles de corporativo seleccionado
const buscarHotelesCorporativo = () => {
  if (!corporativoSeleccionado.value) return
  buscandoHoteles.value = true

  setTimeout(() => {
    hotelesFiltrados.value = [...hotelesCorporativos]
    buscandoHoteles.value = false
  }, 800)
}

// 🔍 Buscar por ID o nombre
const buscarHotelesIndividual = () => {
  if (!busquedaHotel.value) {
    alertaPaso6.value = '⚠️ Ingresa al menos un ID o nombre para buscar.'
    setTimeout(() => (alertaPaso6.value = ''), 3000)
    return
  }

  buscandoHoteles.value = true
  const terminos = busquedaHotel.value.split(',').map(t => t.trim().toLowerCase())

  setTimeout(() => {
    hotelesFiltrados.value = hotelesIndividuales.filter(hotel =>
      terminos.some(t => hotel.nombre.toLowerCase().includes(t) || String(hotel.id).includes(t))
    )
    buscandoHoteles.value = false
  }, 800)
}

// 🔘 Seleccionar todos
const toggleTodos = () => {
  hotelesFiltrados.value.forEach(h => (h.seleccionado = seleccionarTodos.value))
}

// ✅ Validar paso
const validarPaso6 = () => {
  if (!form.tipoHotel) {
    alertaPaso6.value = '⚠️ Selecciona el tipo de acuerdo con hotel.'
    setTimeout(() => (alertaPaso6.value = ''), 3000)
    return
  }

  const seleccionados = hotelesFiltrados.value.filter(h => h.seleccionado)
  if (seleccionados.length === 0) {
    alertaPaso6.value = '⚠️ Debes seleccionar al menos un hotel para continuar.'
    setTimeout(() => (alertaPaso6.value = ''), 3000)
    return
  }

  nextStep()
}


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


const alertaPaso1 = ref('')

const handleFileUpload = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (!target.files || target.files.length === 0) {
    fileName.value = null
    return
  }

  const file = target.files[0]
  const allowedTypes = ['application/pdf', 'image/png']
  const maxSize = 10 * 1024 * 1024 // 10 MB

  // Validar tipo de archivo
  if (!allowedTypes.includes(file.type)) {
    alertaPaso1.value = '⚠️ Solo se permiten archivos PDF o PNG.'
    fileName.value = null
    target.value = '' // limpiar input
    setTimeout(() => (alertaPaso1.value = ''), 3000)
    return
  }

  // Validar tamaño
  if (file.size > maxSize) {
    alertaPaso1.value = '⚠️ El archivo no debe superar los 10 MB.'
    fileName.value = null
    target.value = '' // limpiar input
    setTimeout(() => (alertaPaso1.value = ''), 3000)
    return
  }

  // Si pasa las validaciones
  fileName.value = file.name
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
