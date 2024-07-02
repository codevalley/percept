<template>
  <div class="font-['IBM_Plex_Sans'] min-h-screen bg-white">
    <div class="max-w-4xl mx-auto px-4">
      <!-- Title bar -->
      <div class="flex justify-between items-center py-4">
        <div class="flex items-center">
          <img src="/assets/backwave.svg" alt="Backwave logo" class="w-16 h-16" />
          <h1 class="text-5xl font-bold ml-2 text-black self-start mt-1">Backwave</h1>
        </div>
        <div class="flex items-center bg-gray-100 rounded-full h-12 self-center">
          <input
            v-model="creatorCode"
            type="text"
            placeholder="#creator code"
            class="bg-transparent w-48 h-full px-4 text-xl font-regular text-green-400 focus:outline-none"
          />
          <div class="h-full px-1 flex items-center"> <!-- Padding for button -->
            <button @click="handleAnalyze" class="bg-green-800 text-white h-[80%] aspect-square rounded-full flex items-center justify-center p-2">
              <img src="/assets/analyze-icon.svg" alt="Analyze" class="w-full h-full object-contain brightness-0 invert" />
            </button>
          </div>
        </div>
      </div>

      <!-- Hero section -->
      <div class="mt-8 p-8 bg-neutral-100 rounded-3xl min-h-[420px] flex flex-col justify-end">
        
        <inline-svg src="/assets/high-five.svg" class="text-neutral-700 w-24 h-24 mx-auto mb-6" />
        <h2 class="text-4xl font-bold text-center text-neutral-700 mb-1">
          Calibrate your self awareness
        </h2>
        <p class="text-xl text-center text-neutral-700 mb-8">
          Compare what you think about yourself, what others really look at you as
        </p>
        <div class="flex justify-center">
          <button @click="$emit('create')" class="bg-neutral-800 text-green-400 text-xl font-bold px-8 py-2 rounded-full">
            Create a review
          </button>
        </div>
      </div>

       <!-- Participate section -->
      <div class="mt-12">
        <h3 class="text-xl font-semibold text-sky-950 text-left">Came here for a friend?</h3>
        <p class="text-lg text-sky-950 mb-3 text-left">
          Share some valuable feedback to the creator and see what others are saying
        </p>
        <div class="flex items-center bg-gray-100 rounded-full w-[420px]">
          <img src="/assets/question-icon.svg" alt="Question" class="w-10 h-10 ml-4 mr-2" />
          <input
            v-model="participateCode"
            type="text"
            placeholder="Enter review code"
            class="bg-transparent text-xl font-regular text-zinc-400 flex-grow px-2 py-2 focus:outline-none"
          />
          <button
            @click="submitCode"
            :disabled="isLoading"
            class="bg-zinc-700 text-gray-100 text-xl font-bold px-8 py-2 rounded-full"
          >
            <span v-if="!isLoading">Participate</span>
            <span v-else class="inline-block animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></span>
          </button>
        </div>
        <p v-if="errorMessage" class="mt-4 text-sm text-red-600 bg-red-100 border border-red-400 rounded-md p-2">
          {{ errorMessage }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import api from '@/services/api';
import InlineSvg from 'vue-inline-svg';

export default {
  name: 'HomeView',
  components: {
    InlineSvg,
  },
  emits: ['create', 'submit-code'],
  setup(props, { emit }) {
    const participateCode = ref('');
    const creatorCode = ref('');
    const isLoading = ref(false);
    const errorMessage = ref('');

    const handleAnalyze = () => {
      // Implement creator code analysis logic here
      console.log('Analyzing creator code:', creatorCode.value);
    };

    const submitCode = async () => {
      isLoading.value = true;
      errorMessage.value = '';
      try {
        console.log('Fetching survey with code:', participateCode.value);
        const response = await api.getSurvey(participateCode.value);
        console.log('Received survey data:', response.data);
        if (response.data && response.data.questions) {
          emit('submit-code', { surveyId: participateCode.value, surveyData: response.data });
        } else {
          throw new Error('Invalid survey data received');
        }
      } catch (error) {
        console.error('Error fetching survey:', error);
        errorMessage.value = 'Invalid survey code or survey not found. Please try again.';
      } finally {
        isLoading.value = false;
      }
    };

    return {
      participateCode,
      creatorCode,
      isLoading,
      errorMessage,
      handleAnalyze,
      submitCode,
    };
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;700&display=swap');
</style>