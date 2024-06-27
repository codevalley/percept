<template>
  <div class="max-w-2xl mx-auto p-4" v-if="currentQuestion">
    <h2 class="text-2xl font-bold mb-6 text-center">{{ currentQuestion.text }}</h2>
    <div class="flex justify-center gap-4 mb-8">
      <template v-if="currentQuestion.response_type === 'scale'">
        <button 
          v-for="n in currentQuestion.response_scale_max" 
          :key="n" 
          @click="selectAnswer(n)"
          :class="[
            'w-12 h-12 border rounded-md flex items-center justify-center cursor-pointer transition-colors',
            currentAnswer === n ? 'bg-blue-500 text-white' : 'bg-white text-gray-700 hover:bg-blue-100'
          ]"
        >
          {{ n }}
        </button>
      </template>
      <template v-else-if="currentQuestion.response_type === 'boolean'">
        <button 
          @click="selectAnswer(true)" 
          :class="[
            'px-6 py-2 border rounded-md transition-colors',
            currentAnswer === true ? 'bg-blue-500 text-white' : 'bg-white text-gray-700 hover:bg-blue-100'
          ]"
        >
          Yes
        </button>
        <button 
          @click="selectAnswer(false)" 
          :class="[
            'px-6 py-2 border rounded-md transition-colors',
            currentAnswer === false ? 'bg-blue-500 text-white' : 'bg-white text-gray-700 hover:bg-blue-100'
          ]"
        >
          No
        </button>
      </template>
    </div>
    <div class="w-full h-2 bg-gray-200 rounded-full mb-6">
      <div class="h-full bg-blue-500 rounded-full transition-all duration-300 ease-in-out" :style="{ width: `${progress}%` }"></div>
    </div>
    <button 
      @click="nextQuestion" 
      class="w-full py-3 text-lg font-semibold text-white bg-blue-500 rounded-full hover:bg-blue-600 transition duration-300 disabled:bg-gray-400 disabled:cursor-not-allowed"
      :disabled="currentAnswer === null || isSubmitting"
    >
      {{ isLastQuestion ? 'Finish' : 'Next' }}
    </button>
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
      isSubmitting: false
    }
  },
  computed: {
    currentQuestion() {
      return this.surveyData.questions[this.currentQuestionIndex];
    },
    progress() {
      return ((this.currentQuestionIndex + 1) / this.surveyData.questions.length) * 100;
    },
    isLastQuestion() {
      return this.currentQuestionIndex === this.surveyData.questions.length - 1;
    }
  },
  methods: {
    selectAnswer(value) {
      this.currentAnswer = value;
    },
    async nextQuestion() {
      if (this.currentAnswer === null) return;

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
      try {
        const answersToSubmit = Object.entries(this.answers).map(([questionId, answer]) => ({
          question_id: parseInt(questionId),
          answer
        }));
        console.log('Submitting answers:', answersToSubmit);
        const response = await api.submitAnswers(this.surveyId, { answers: answersToSubmit });
        console.log('Survey submission response:', response.data);
        this.$emit('survey-completed', response.data);
      } catch (error) {
        console.error('Error submitting survey:', error.response ? error.response.data : error);
        this.$emit('survey-error', 'Error submitting survey. Please try again.');
      } finally {
        this.isSubmitting = false;
      }
    }
  }
}
</script>