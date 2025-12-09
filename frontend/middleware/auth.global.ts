export default defineNuxtRouteMiddleware((to) => {
  // ⛔ Evitar que el middleware corra en SSR (muy importante con Pinia)
  if (process.server) return

  // Rutas públicas
  const publicPaths = ['/login']
  if (publicPaths.includes(to.path)) return

  const userStore = useUserStore()

  // Si no está logueado → enviar al login
  if (!userStore.loggedIn) {
    return navigateTo('/login', { replace: true })
  }
})
