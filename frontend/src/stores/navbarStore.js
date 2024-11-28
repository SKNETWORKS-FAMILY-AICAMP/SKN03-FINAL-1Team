import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useNavbarStore = defineStore('navbar', () => {
  const selectedNavItem = ref(null)

  const setSelectedNavItem = (id) => {
    selectedNavItem.value = id
  }

  return { selectedNavItem, setSelectedNavItem }
})
