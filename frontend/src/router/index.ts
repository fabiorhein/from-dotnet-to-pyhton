import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import LoginView from '../modules/auth/views/LoginView.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresAuth: false },
    },
    {
      path: '/users',
      name: 'users',
      component: () => import('../modules/users/views/UsersListView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/',
      redirect: '/users',
    },
  ],
});

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' });
  } 
  else if (to.name === 'login' && authStore.isAuthenticated) {
    next({ name: 'users' });
  } 
  else {
    next();
  }
});

export default router;