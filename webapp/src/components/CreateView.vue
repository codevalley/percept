<template>
  <div class="max-w-2xl mx-auto p-4">
    <!-- Survey Title and Description Section -->
    <div class="mb-8 text-center">
      <input 
        v-model="surveyTitle" 
        type="text" 
        class="w-full max-w-md px-4 py-2 text-2xl font-bold text-center border-b border-gray-300 focus:border-blue-500 focus:outline-none bg-transparent"
        required
      >
      <textarea 
        v-model="surveyDescription" 
        class="w-full max-w-md mt-4 px-4 py-2 text-lg text-center border-b border-gray-300 focus:border-blue-500 focus:outline-none bg-transparent resize-none"
        maxlength="240"
      ></textarea>
    </div>
    
    <!-- Guidance for creator answers -->
    <div v-if="creationStage === 'completion'" class="text-center text-lg font-bold text-blue-500 mb-6">
      Can you answer these yourself first?
    </div>

    <!-- Question Creation Stage -->
    <div v-if="creationStage === 'questions'" class="space-y-4 mb-8">
      <div class="flex flex-col space-y-2">
        <input v-model="newQuestion.text" type="text" placeholder="Enter your question" required
               class="w-full px-4 py-2 border border-gray-300 rounded-md focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50">
      </div>
      <div class="flex space-x-2">
        <select v-model="newQuestion.response_type" required
                class="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50">
          <option value="scale">Scale</option>
          <option value="boolean">Yes/No</option>
        </select>
        <input v-if="newQuestion.response_type === 'scale'" v-model.number="newQuestion.response_scale_max" 
               type="number" min="2" max="10" placeholder="Max scale value" required
               class="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50">
      </div>
      <div class="flex space-x-2">
        <button @click="addQuestion" class="flex-1 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition duration-300">Add Question</button>
        <button @click="startSurveyCompletion" :disabled="questions.length === 0" 
                class="flex-1 px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50 transition duration-300 disabled:bg-gray-400 disabled:cursor-not-allowed">Finish</button>
      </div>
    </div>

    <ul class="space-y-4">
      <li v-for="(question, index) in questions" :key="question.id" class="border border-gray-200 rounded-lg overflow-hidden">
        <div class="bg-gray-50 p-4 flex justify-between items-center">
          <span class="font-semibold">{{ question.text }}</span>
          <span class="text-sm px-2 py-1 rounded-full" 
                :class="question.response_type === 'scale' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'">
            {{ question.response_type === 'scale' ? `Scale (1-${question.response_scale_max})` : 'Yes/No' }}
          </span>
        </div>
        
        <!-- Creator Answer Section -->
        <div v-if="creationStage === 'completion'" class="p-4 bg-white">
          <div v-if="question.response_type === 'scale'" class="flex justify-center space-x-2">
            <button 
              v-for="n in question.response_scale_max" 
              :key="n" 
              @click="selectAnswer(index, n)"
              :class="['w-10 h-10 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300',
                       creatorAnswers[index] === n ? 'bg-blue-500 text-white' : 'bg-gray-200 hover:bg-gray-300']"
              :disabled="isSubmitted"
            >
              {{ n }}
            </button>
          </div>
          <div v-else class="flex justify-center space-x-4">
            <button @click="selectAnswer(index, true)" 
                    :class="['px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300',
                             creatorAnswers[index] === true ? 'bg-blue-500 text-white' : 'bg-gray-200 hover:bg-gray-300']"
                    :disabled="isSubmitted">Yes</button>
            <button @click="selectAnswer(index, false)" 
                    :class="['px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300',
                             creatorAnswers[index] === false ? 'bg-blue-500 text-white' : 'bg-gray-200 hover:bg-gray-300']"
                    :disabled="isSubmitted">No</button>
          </div>
        </div>
      </li>
    </ul>

    <!-- Submit Survey Button -->
    <div class="mt-8 text-center">
      <button v-if="creationStage === 'completion' && !showSuccess" @click="finishSurvey" 
              :disabled="!allQuestionsAnswered || isLoading || isSubmitted"
              class="px-6 py-3 bg-blue-500 text-white rounded-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition duration-300 disabled:bg-gray-400 disabled:cursor-not-allowed">
        <span v-if="!isLoading">Submit Survey</span>
        <span v-else class="inline-block animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></span>
      </button>
    </div>

    <div v-if="showSuccess" class="mt-8 p-4 bg-green-100 border border-green-400 text-green-700 rounded-md">
      <h3 class="font-bold text-lg mb-2">Survey Created Successfully!</h3>
      <p>Survey ID: {{ createdSurveyId }}</p>
    </div>
    
    <p v-if="errorMessage" class="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-md">{{ errorMessage }}</p>
  </div>
</template>

<script>
import api from '@/services/api';
import confetti from 'canvas-confetti';

export default {
  name: 'CreateView',
  data() {
    return {
      creationStage: 'questions',
      surveyTitle: 'Help me improve',
      surveyDescription: 'Take 2 minutes to answer a few questions about me',
      newQuestion: {
        text: '',
        response_type: 'scale',
        response_scale_max: 5
      },
      questions: [],
      creatorAnswers: [],
      isLoading: false,
      showSuccess: false,
      createdSurveyId: null,
      errorMessage: '',
      isSubmitted: false
    }
  },
  computed: {
    allQuestionsAnswered() {
      return this.creatorAnswers.length === this.questions.length &&
             this.creatorAnswers.every(answer => answer !== null && answer !== undefined);
    }
  },
  methods: {
    addQuestion() {
      const question = {
        id: Date.now(),
        text: this.newQuestion.text,
        response_type: this.newQuestion.response_type,
        response_scale_max: this.newQuestion.response_type === 'scale' ? this.newQuestion.response_scale_max : undefined
      };
      this.questions.push(question);
      this.newQuestion.text = '';
      this.newQuestion.response_type = 'scale';
      this.newQuestion.response_scale_max = 5;
    },
    startSurveyCompletion() {
      this.creationStage = 'completion';
      this.creatorAnswers = new Array(this.questions.length).fill(null);
    },
    selectAnswer(index, value) {
      if (!this.isSubmitted) {
        this.creatorAnswers[index] = value;
      }
    },
    async finishSurvey() {
      if (this.isSubmitted) return;
      
      this.isLoading = true;
      this.errorMessage = '';
      try {
        const surveyData = {
          title: this.surveyTitle || "Untitled Survey",
          description: this.surveyDescription || "No description provided",
          questions: this.questions.map((q, index) => ({
            ...q,
            creator_answer: this.creatorAnswers[index]
          }))
        };
        const response = await api.createSurvey(surveyData);
        console.log('Survey created', response.data);
        this.createdSurveyId = response.data.survey_id;
        this.showSuccess = true;
        this.isSubmitted = true;
        this.celebrateSuccess();
      } catch (error) {
        console.error('Error creating survey:', error);
        this.errorMessage = 'Error creating survey. Please try again.' + error;
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