import { defineStore } from 'pinia'

export const useToggleStore = defineStore('toggle', {
  state: () => ({
    isToggled: false,
  }),
  actions: {
    toggle() {
      this.isToggled = !this.isToggled
    },
  },
})
