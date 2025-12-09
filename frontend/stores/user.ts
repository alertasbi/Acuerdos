
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    idUser: null as number | null,
    name: '' as string,
    role: '' as string,
    loggedIn: false
  }),

  actions: {
    setUser(data: any) {
      this.idUser = data.idUser
      this.name = data.name
      this.role = data.role
      this.loggedIn = true
    },

    logout() {
      this.idUser = null
      this.name = ''
      this.role = ''
      this.loggedIn = false
    }
  }
})
