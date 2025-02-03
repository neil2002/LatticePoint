// router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import DataProcessor from '../components/DataProcessor.vue';
import DashboardBuilder from '../components/DashboardBuilder.vue';
import Login from '../components/login.vue';
import { useAuthStore } from '../stores/authStore.js'

const routes = [
  {
    path: '/',
    name: 'DataProcessor',
    component: DataProcessor,
    meta: { requiresAuth: true } 
  },
  {
    path: '/dashboard-builder',
    name: 'DashboardBuilder',
    component: DashboardBuilder,
    meta: { requiresAuth: true } 
  },
  { 
    path: '/login', 
    component: Login 
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


// Navigation guard for authentication
// router.beforeEach((to, from, next) => {
//   const authStore = useAuthStore()
  
//   // Check if route requires authentication
//   if (to.matched.some(record => record.meta.requiresAuth)) {
//     // If not authenticated, redirect to login
//     if (!authStore.isAuthenticated) {
//       next('/login')
//       return
//     }
//   }
  
//   // If trying to access login while already authenticated, redirect to dashboard
//   if (to.path === '/login' && authStore.isAuthenticated) {
//     next('/dashboard')
//     return
//   }
  
//   next()
// })

export default router;
