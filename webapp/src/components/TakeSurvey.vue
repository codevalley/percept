<template>
  <div class="take-survey" v-if="isDataLoaded">
    <h2>{{ currentQuestion.text }}</h2>
    <div class="answer-options">
      <template v-if="currentQuestion.response_type === 'scale'">
        <button 
          v-for="n in currentQuestion.response_scale_max" 
          :key="n" 
          @click="selectAnswer(n)"
          :class="['option', { selected: currentAnswer === n }]"
        >
          {{ n }}
        </button>
      </template>
      <template v-else-if="currentQuestion.response_type === 'boolean'">
        <button @click="selectAnswer(true)" :class="['option', { selected: currentAnswer === true }]">Yes</button>
        <button @click="selectAnswer(false)" :class="['option', { selected: currentAnswer === false }]">No</button>
      </template>
    </div>
    <div class="progress-bar">
      <div class="progress" :style="{ width: `${progress}%` }"></div>
    </div>
    <button @click="nextQuestion" class="btn" :disabled="currentAnswer === null || isSubmitting">
      {{ isLastQuestion ? 'Finish' : 'Next' }}
    </button>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
  <div v-else class="loading">
    Loading survey data...
    <p>Survey ID: {{ surveyId }}</p>
    <p>Survey Data: {{ JSON.stringify(surveyData) }}</p>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'TakeSurvey',
  props: {
    surveyId: {
      type: String,
      required: true
    },
    surveyData: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      currentQuestionIndex: 0,
      answers: {},
      currentAnswer: null,
      isSubmitting: false,
      errorMessage: ''
    }
  },
  computed: {
    isDataLoaded() {
      console.log('Survey Data:', this.surveyData);
      return this.surveyData && this.surveyData.questions && this.surveyData.questions.length > 0;
    },
    currentQuestion() {
      return this.isDataLoaded ? this.surveyData.questions[this.currentQuestionIndex] : null;
    },
    progress() {
      return this.isDataLoaded ? ((this.currentQuestionIndex + 1) / this.surveyData.questions.length) * 100 : 0;
    },
    isLastQuestion() {
      return this.isDataLoaded && this.currentQuestionIndex === this.surveyData.questions.length - 1;
    }
  },
  methods: {
    selectAnswer(value) {
      this.currentAnswer = value;
    },
    async nextQuestion() {
      if (!this.currentQuestion) return;
      
      this.answers[this.currentQuestion.id] = this.currentAnswer;
      this.currentAnswer = null;
      
      if (this.isLastQuestion) {
        await this.submitSurvey();
      } else {
        this.currentQuestionIndex++;
      }
    },
    async submitSurvey() {
      this.isSubmitting = true;
      this.errorMessage = '';
      try {
        const response = await api.submitAnswers(this.surveyId, Object.entries(this.answers).map(([questionId, answer]) => ({
          question_id: questionId,
          answer
        })));
        this.$emit('survey-completed', response.data);
      } catch (error) {
        console.error('Error submitting survey:', error);
        this.errorMessage = 'Error submitting survey. Please try again.';
      } finally {
        this.isSubmitting = false;
      }
    }
  },
  mounted() {
    console.log('TakeSurvey mounted. Survey ID:', this.surveyId, 'Survey Data:', this.surveyData);
  }
}
</script>

<style scoped>
.answer-options {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin: 20px 0;
}

.option {
  width: 40px;
  height: 40px;
  border: 1px solid #ccc;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s;
}

.option.selected {
  background-color: #3498db;
  color: white;
}

.progress-bar {
  width: 100%;
  height: 10px;
  background-color: #eee;
  border-radius: 5px;
  margin-bottom: 20px;
}

.progress {
  height: 100%;
  background-color: #3498db;
  border-radius: 5px;
  transition: width 0.3s ease-in-out;
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

.btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.btn:hover:not(:disabled) {
  background-color: #2980b9;
}

.error-message {
  color: #721c24;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  padding: 10px;
  margin-top: 10px;
}

.loading {
  font-size: 18px;
  color: #666;
  margin-top: 20px;
}
</style>