<template>
  <div class="create">
    <h2>Create a New Survey</h2>
    <form @submit.prevent="addQuestion">
      <input v-model="newQuestion" type="text" placeholder="Enter your question" required>
      <button type="submit" class="btn">Add Question</button>
    </form>
    <ul class="question-list">
      <li v-for="question in questions" :key="question.id">{{ question.text }}</li>
    </ul>
    <button @click="finishSurvey" class="btn" :disabled="questions.length === 0 || isLoading">
      <span v-if="!isLoading">Finish Survey</span>
      <span v-else class="loader"></span>
    </button>
    <div v-if="showSuccess" class="success-message">
      <h3>Survey Created Successfully!</h3>
      <p>Survey ID: {{ createdSurveyId }}</p>
    </div>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script>
import api from '@/services/api';
import confetti from 'canvas-confetti';

export default {
  name: 'CreateView',
  data() {
    return {
      newQuestion: '',
      questions: [],
      isLoading: false,
      showSuccess: false,
      createdSurveyId: null,
      errorMessage: ''
    }
  },
  methods: {
    addQuestion() {
      this.questions.push({
        id: Date.now(),
        text: this.newQuestion,
        response_type: 'scale',
        response_scale_max: 10,
        creator_answer: 5
      });
      this.newQuestion = '';
    },
    async finishSurvey() {
      this.isLoading = true;
      this.errorMessage = '';
      try {
        const surveyData = {
          title: "New Survey",
          description: "Survey created via Backfeed",
          questions: this.questions
        };
        const response = await api.createSurvey(surveyData);
        console.log('Survey created', response.data);
        this.createdSurveyId = response.data.survey_id;
        this.showSuccess = true;
        this.questions = [];
        this.celebrateSuccess();
      } catch (error) {
        console.error('Error creating survey:', error);
        this.errorMessage = 'Error creating survey. Please try again.'+error;
      } finally {
        this.isLoading = false;
      }
    },
    celebrateSuccess() {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });
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
  margin-bottom: 20px;
}

input {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 300px;
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
  background-color: #ccc;
  cursor: not-allowed;
}

.question-list {
  text-align: left;
  max-width: 500px;
  margin: 0 auto 20px;
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

.success-message {
  background-color: #d4edda;
  border-color: #c3e6cb;
  color: #155724;
  padding: 15px;
  border-radius: 5px;
  margin-top: 20px;
}

.error-message {
  background-color: #f8d7da;
  border-color: #f5c6cb;
  color: #721c24;
  padding: 15px;
  border-radius: 5px;
  margin-top: 20px;
}
</style>