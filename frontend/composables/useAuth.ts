// composables/useAuth.ts
export function useAuth() {
  const isLoggedIn = useState<boolean>('isLoggedIn', () => false)

  // Cookie SSR-friendly (sirve en refresh y en middleware del server)
  const authCookie = useCookie('pt_auth', { sameSite: 'lax', secure: false })

  const login = () => {
    isLoggedIn.value = true
    authCookie.value = '1'
    if (process.client) localStorage.setItem('loggedIn', 'true') // opcional
  }

  const logout = () => {
    isLoggedIn.value = false
    authCookie.value = null
    if (process.client) localStorage.removeItem('loggedIn')
  }

  const check = () => {
    if (authCookie.value === '1') { isLoggedIn.value = true; return true }
    if (process.client && localStorage.getItem('loggedIn') === 'true') {
      isLoggedIn.value = true; return true
    }
    isLoggedIn.value = false
    return false
  }

  return { isLoggedIn, login, logout, check }
}
