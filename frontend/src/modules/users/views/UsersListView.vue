<script setup lang="ts">
import { useAuthStore } from '../../../stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

function handleLogout() {
  authStore.logout();
  router.push('/login');
}
</script>

<template>
  <div class="min-h-screen bg-slate-900 text-white p-8">
    <div class="max-w-4xl mx-auto space-y-6">
      <div class="flex justify-between items-center border-b border-slate-700 pb-4">
        <h1 class="text-3xl font-bold">Painel de Utilizadores</h1>
        <button 
          @click="handleLogout" 
          class="px-4 py-2 bg-red-600 hover:bg-red-500 rounded-lg text-sm font-medium transition cursor-pointer"
        >
          Sair
        </button>
      </div>

      <div class="bg-slate-800 p-6 rounded-xl border border-slate-700">
        <p class="text-slate-300">
          🎉 Autenticação realizada com sucesso! O Token JWT está guardado e ativo no <code class="bg-slate-900 px-2 py-1 rounded text-blue-400">localStorage</code>.
        </p>
      </div>
    </div>
  </div>
</template>