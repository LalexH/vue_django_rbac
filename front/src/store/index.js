import { createStore } from 'vuex'

export default createStore({
  state: {
    userInfo: JSON.parse(localStorage.getItem("userInfo")) || ""

  },
  getters: {
  },
  mutations: {
    userInfo(state){
        state.userInfo = JSON.parse(localStorage.getItem("userInfo"))
    }
  },
  actions: {
  },
  modules: {},
})