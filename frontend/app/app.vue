<template>
  <main style="padding: 2rem; font-family: sans-serif;">
    <h1>Frontend listo ✅</h1>
    <p>Estado del backend (API): <strong>{{ status }}</strong></p>
  </main>
</template>

<script setup lang="ts">
let status = 'sin conexión'

try {
  // Llamamos al endpoint del backend
  const res = await $fetch<{ status: string }>('http://127.0.0.1:5000/api/health')
  status = res.status
} catch {
  status = 'error de conexión'
}
</script>
