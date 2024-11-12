import { defineStore } from 'pinia'

export const usePaperStore = defineStore('paper', {
  state: () => ({
    papers: [],
    selectedPaper: null,
  }),
  actions: {
    async fetchPapers(query) {
      // API 호출로 논문 검색
      const response = await fetch(`https://api.example.com/search?q=${query}`)
      this.papers = await response.json()
    },
    selectPaper(paper) {
      this.selectedPaper = paper
    },
  },
})
