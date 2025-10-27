<template>
  <div class="min-h-screen flex bg-gray-50">
    <!-- Sidebar fijo -->
    <Sidebar />

    <!-- Contenedor principal -->
    <div class="flex flex-col flex-1 min-h-screen ml-64 transition-all duration-300">
      <Header />


      <FooterBar />
    </div>
  </div>
</template>

<script setup lang="ts">
import Sidebar from '~/components/Layout/Sidebar.vue'
import Header from '~/components/Layout/Header.vue'
import FooterBar from '~/components/Layout/FooterBar.vue'
</script>
