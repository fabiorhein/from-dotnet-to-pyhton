<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../../stores/auth';
import { LogIn } from '@lucide/vue';

const email = ref('');
const password = ref('');
const isLoading = ref(false);
const errorMessage = ref('');

const authStore = useAuthStore();
const router = useRouter();

async function handleSubmit() {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    await authStore.login(email.value, password.value);
    router.push('/users');
  } catch (error: any) {
    if (error.response && error.response.data?.detail) {
      errorMessage.value = error.response.data.detail;
    } else {
      errorMessage.value = 'Ocorreu um erro ao tentar fazer login. Tente novamente.';
    }
  } finally {
    isLoading.value = false;
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-900 px-4">
    <div class="max-w-md w-full bg-slate-800 rounded-xl shadow-2xl border border-slate-700 p-8 space-y-6">
      
      <div class="text-center space-y-2">
        <div class="inline-flex p-3 bg-blue-600/10 text-blue-500 rounded-lg mb-2">
          <LogIn class="w-8 h-8" />
        </div>
        <h1 class="text-2xl font-bold text-white">Acessar a Conta</h1>
        <p class="text-slate-400 text-sm">Insira suas credenciais para continuar</p>
      </div>

      <div v-if="errorMessage" class="bg-red-500/10 border border-red-500/50 text-red-400 p-3 rounded-lg text-sm text-center">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-slate-300 mb-1">E-mail</label>
          <input 
            v-model="email"
            type="email" 
            required
            placeholder="seu@email.com"
            class="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-300 mb-1">Senha</label>
          <input 
            v-model="password"
            type="password" 
            required
            placeholder="••••••••"
            class="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
          />
        </div>

        <button 
          type="submit" 
          :disabled="isLoading"
          class="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-medium rounded-lg transition duration-200 flex items-center justify-center cursor-pointer"
        >
          <span v-if="isLoading">Autenticando...</span>
          <span v-else>Entrar</span>
        </button>
      </form>

    </div>
  </div>
</template>