<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100">
    <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
      <h2 class="text-2xl font-bold mb-6 text-center text-gray-800">Enter Survey Code</h2>
      <form @submit.prevent="submitCode" class="space-y-4">
        <input 
          v-model="code" 
          type="text" 
          placeholder="Survey Code" 
          required
          class="w-full px-4 py-2 text-gray-700 bg-gray-200 rounded-lg focus:outline-none focus:bg-white focus:ring-2 focus:ring-blue-400"
        >
        <button 
          type="submit" 
          class="w-full px-4 py-2 text-white bg-blue-500 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-50 transition duration-300 ease-in-out"
          :disabled="isLoading"
        >
          <span v-if="!isLoading">Enter</span>
          <span v-else class="inline-block animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></span>
        </button>
      </form>
      <p v-if="errorMessage" class="mt-4 text-sm text-red-600 bg-red-100 border border-red-400 rounded-md p-2">
        {{ errorMessage }}
      </p>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'ParticipateView',
  data() {
    return {
      code: '',
      isLoading: false,
      errorMessage: ''
    }
  },
  methods: {
    async submitCode() {
      this.isLoading = true;
      this.errorMessage = '';
      try {
        console.log('Fetching survey with code:', this.code);
        const response = await api.getSurvey(this.code);
        console.log('Received survey data:', response.data);
        if (response.data && response.data.questions) {
          this.$emit('submit-code', { surveyId: this.code, surveyData: response.data });
        } else {
          throw new Error('Invalid survey data received');
        }
      } catch (error) {
        console.error('Error fetching survey:', error);
        this.errorMessage = 'Invalid survey code or survey not found. Please try again.';
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>