<template>
  <div class="font-['IBM_Plex_Sans'] min-h-screen bg-white">
    <SiteHeader initialPage="participate" @page-changed="handlePageChange" />
    <div v-if="loadedSurveyData" class="max-w-[768px] mx-auto px-4 pt-[176px]">
      <!-- Combined Header and Question Section -->
      <div class="rounded-3xl overflow-hidden">
        <!-- Header Section -->
        <div class="bg-neutral-100 p-7">
          <div class="flex items-start">
            <div class="w-14 h-14 bg-secondary rounded-full mr-5 flex-shrink-0"></div>
            <div>
              <h1 class="text-neutral-600 text-2xl font-semibold leading-10 mb-2">{{ loadedSurveyData.title }}</h1>
              <p class="text-neutral-600 text-lg font-normal leading-7">{{ loadedSurveyData.description }}</p>
            </div>
          </div>
        </div>

        <!-- Question Section -->
        <div v-if="currentQuestion" class="bg-[#D8F89D] p-7 relative">
          <!-- Progress Bar -->
          <div class="w-full h-2.5 bg-neutral-200 absolute top-0 left-0 right-0">
            <div class="h-full bg-accent-green transition-all duration-300 ease-in-out" :style="{ width: `${progress}%` }"></div>
          </div>

          <!-- Question -->
          <div class="flex items-center mb-12 mt-6">
            <inline-svg src="assets/question-icon.svg" class="w-7 h-7 mr-4 text-primary"/>
            <p class="text-primary text-2xl font-bold leading-9">{{ currentQuestion.text }}</p>
          </div>

          <!-- Answer Options -->
          <div class="flex justify-center space-x-5 mb-6">
            <template v-if="currentQuestion.response_type === 'scale'">
              <button 
                v-for="n in (currentQuestion.response_scale_max || 5)" 
                :key="n" 
                @click="selectAnswer(n)"
                :class="[
                  'w-14 h-14 rounded-full border-4 transition-colors flex items-center justify-center',
                  n <= currentAnswer ? 'bg-primary border-primary text-white' : 'bg-white border-neutral-200 text-primary'
                ]"
              >
                {{ n }}
              </button>
            </template>
            <template v-else-if="currentQuestion.response_type === 'boolean'">
              <button 
                @click="selectAnswer(true)"
                :class="[
                  'w-14 h-14 rounded-full border-4 transition-colors flex items-center justify-center',
                  currentAnswer === true ? 'bg-primary border-primary' : 'bg-white border-neutral-200'
                ]"
              >
                <inline-svg src="assets/yes-icon.svg" class="w-8 h-8" :class="currentAnswer === true ? 'text-white' : 'text-primary'"/>
              </button>
              <button 
                @click="selectAnswer(false)"
                :class="[
                  'w-14 h-14 rounded-full border-4 transition-colors flex items-center justify-center',
                  currentAnswer === false ? 'bg-primary border-primary' : 'bg-white border-neutral-200'
                ]"
              >
                <inline-svg src="assets/no-icon.svg" class="w-8 h-8" :class="currentAnswer === false ? 'text-white' : 'text-primary'"/>
              </button>
            </template>
          </div>
        </div>
      </div>

      <!-- Navigation Buttons -->
      <div class="flex justify-between mt-6">
        <button 
          @click="previousQuestion" 
          v-if="currentQuestionIndex > 0"
          class="px-6 py-2 bg-primary text-white rounded-full"
        >
          Previous
        </button>
        <button 
          @click="nextQuestion" 
          :disabled="currentAnswer === null || isSubmitting"
          class="px-6 py-2 bg-primary text-white rounded-full ml-auto"
        >
          {{ isLastQuestion ? 'Finish' : 'Next' }}
        </button>
      </div>
    </div>
    <div v-else class="max-w-[768px] mx-auto px-4 pt-[176px] flex justify-center items-center">
      <p class="text-2xl text-primary">Loading survey...</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import api from '@/services/api';
import InlineSvg from 'vue-inline-svg';

export default {
  name: 'TakeSurvey',
  components: {
    InlineSvg,
  },
  props: {
    surveyId: {
      type: String,
      required: true
    },
    surveyData: {
      type: Object,
      default: null
    }
  },
  setup(props) {
    const loadedSurveyData = ref(null);
    const isLoading = ref(true);

    onMounted(async () => {
      if (props.surveyData) {
        loadedSurveyData.value = props.surveyData;
        isLoading.value = false;
      } else {
        try {
          const response = await api.getSurvey(props.surveyId);
          loadedSurveyData.value = response.data;
        } catch (error) {
          console.error('Error fetching survey:', error);
          // Handle error (e.g., show error message)
        } finally {
          isLoading.value = false;
        }
      }
    });

    // Rest of your component logic

    return {
      loadedSurveyData,
      isLoading,
      // Other returned values
    };
  }
}
</script>