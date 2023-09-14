import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import HomeView from '../views/HomeView.vue'
import UserView from '@/components/UserView.vue'
import MenuView from '@/components/MenuView.vue'
import RoleView from '@/components/RoleView.vue'
import PermissionView from '@/components/PermissionView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      children: [
        {
          name: "user",
          path: '/user',
          component: UserView
        },
        {
          name: "menu",
          path: '/menu',
          component: MenuView
        },
        {
          name: "role",
          path: '/role',
          component: RoleView
        },
        {
          name: "permission",
          path: '/permission',
          component: PermissionView
        }
      ],
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
  ]
})

export default router

