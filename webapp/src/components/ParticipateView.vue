<template>
  <div class="participate">
    <h2>Enter Survey Code</h2>
    <form @submit.prevent="submitCode">
      <input v-model="code" type="text" placeholder="Survey Code" required>
      <button type="submit" class="btn" :disabled="isLoading">
        <span v-if="!isLoading">Enter</span>
        <span v-else class="loader"></span>
      </button>
    </form>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
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
        const response = await api.getSurvey(this.code);
        // Emit the event with survey data
        this.$emit('submit-code', { surveyId: this.code, surveyData: response.data });
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

<style scoped>
form {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

input {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 200px;
}

.btn {
  padding: 10px 20px;
  font-size: 18px;
  border: none;
  border-radius: 25px;
  background-color: #3498db;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn:hover:not(:disabled) {
  background-color: #2980b9;
}

.btn:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.loader {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
  display: inline-block;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  color: #721c24;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  padding: 10px;
  margin-top: 10px;
}
</style>