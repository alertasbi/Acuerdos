// middleware/auth.global.ts
export default defineNuxtRouteMiddleware((to) => {
  // Rutas públicas (solo login por ahora)
  const publicPaths = ['/login']
  if (publicPaths.includes(to.path)) return

  const { check } = useAuth()
  const ok = check()
  if (!ok) {
    return navigateTo('/login', { replace: true })
  }
})
