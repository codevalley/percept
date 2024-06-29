<template>
  <div class="font-['IBM_Plex_Sans'] min-h-screen bg-white p-4 pt-[200px]">
    <div class="max-w-[859px] mx-auto">
      <div class="flex items-start mb-12">
        <!-- Profile Icon -->
        <div class="w-14 h-14 bg-[#787885] rounded-full mr-5 flex-shrink-0"></div>
        
        <!-- Header Section -->
        <div class="flex-grow">
          <h1 class="text-neutral-900 text-4xl font-semibold leading-10 mb-2 text-left">{{ surveyTitle }}</h1>
          <p class="text-zinc-700 text-lg font-normal leading-7 text-left">{{ surveyDescription }}</p>
        </div>
      </div>

      <!-- Question Input Section -->
      <div class="bg-[#F1F2F4] rounded-[25px] p-7 mb-12">
        <div class="relative flex items-center mb-6">
          <SvgIcon name="question" :size="42" class="mr-4 text-[#2A2731]" />
          <input 
            v-model="newQuestion.text" 
            @keyup.enter="addQuestion"
            @focus="inputFocused = true"
            @blur="inputFocused = false"
            class="w-full bg-transparent text-[34px] font-bold text-[#2A2731] focus:outline-none"
            :placeholder="inputFocused ? '' : 'Enter your question here'"
            :disabled="isSubmitted"
          >
          <span v-if="!newQuestion.text && !inputFocused" class="absolute right-0 top-1/2 transform -translate-y-1/2 text-[#9590A0] text-[34px] font-bold animate-blink">_</span>
        </div>
        <div class="flex space-x-5">
          <button 
            @click="setQuestionType('scale')"
            :class="['w-28 h-10 rounded-full flex items-center justify-center space-x-2 border border-[#EEECF1]', 
                     newQuestion.response_type === 'scale' ? 'bg-[#2A2731] text-white' : 'bg-white text-[#2A2731]']"
            :disabled="isSubmitted"
          >
            <SvgIcon name="scale" :size="24" :class="newQuestion.response_type === 'scale' ? 'text-white' : 'text-[#2A2731]'" />
            <span class="text-base font-medium">Scale</span>
          </button>
          <button 
            @click="setQuestionType('boolean')"
            :class="['w-28 h-10 rounded-full flex items-center justify-center space-x-2 border border-[#EEECF1]', 
                     newQuestion.response_type === 'boolean' ? 'bg-[#2A2731] text-white' : 'bg-white text-[#2A2731]']"
            :disabled="isSubmitted"
          >
            <SvgIcon name="yes-no" :size="24" :class="newQuestion.response_type === 'boolean' ? 'text-white' : 'text-[#2A2731]'" />
            <span class="text-base font-medium">Yes/No</span>
          </button>
        </div>
      </div>

      <!-- Posted Questions -->
      <div v-if="questions.length > 0" class="bg-[#F7F7F8] rounded-[25px] p-7 space-y-6 mb-12">
        <div v-for="(question, index) in questions" :key="question.id" class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <SvgIcon 
        :name="question.response_type === 'scale' ? 'scale' : 'yes-no'" 
        :size="24" 
        :class="creatorAnswers[index] !== null ? 'text-[#2A2731]' : 'text-[#9590A0]'"
      />
            <span :class="['text-2xl font-bold', creatorAnswers[index] !== null ? 'text-[#2A2731]' : 'text-[#9590A0]']">
              {{ question.text }}
            </span>
          </div>
          <div v-if="question.response_type === 'scale'" class="flex space-x-3">
            <button 
              v-for="n in 5" 
              :key="n"
              @click="selectAnswer(index, n)"
              :class="['w-[30px] h-[30px] rounded-full border', 
                       creatorAnswers[index] === n ? 'bg-[#2A2731] border-[#2A2731]' : 'bg-[#DDDAE3] border-[#DDDAE3]']"
              :disabled="isSubmitted"
            ></button>
          </div>
          <div v-else class="flex space-x-3">
            <button 
              @click="selectAnswer(index, true)"
              :class="['w-[30px] h-[30px] rounded-full border', 
                       creatorAnswers[index] === true ? 'bg-[#2A2731] border-[#2A2731]' : 'bg-[#DDDAE3] border-[#DDDAE3]']"
              :disabled="isSubmitted"
            ></button>
            <button 
              @click="selectAnswer(index, false)"
              :class="['w-[30px] h-[30px] rounded-full border', 
                       creatorAnswers[index] === false ? 'bg-[#2A2731] border-[#2A2731]' : 'bg-[#DDDAE3] border-[#DDDAE3]']"
              :disabled="isSubmitted"
            ></button>
          </div>
        </div>
      </div>

      <!-- Alert Box -->
      <div v-if="!allQuestionsAnswered" class="flex items-center space-x-2 mb-6 text-[#996000]">
        <SvgIcon name="info" :size="20" class="text-[#996000]" />
        <span class="text-sm font-medium">Complete self review before publishing</span>
      </div>

      <!-- Publish Button -->
      <div class="text-left">
        <button 
          @click="finishSurvey"
          :disabled="!allQuestionsAnswered || isLoading || isSubmitted"
          class="w-[152px] h-[56px] bg-[#3C3844] rounded-full text-center text-[#EEECF1] text-2xl font-bold leading-9 disabled:bg-gray-100 disabled:text-neutral-400"
        >
          Publish
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import api from '@/services/api';
import confetti from 'canvas-confetti';
import SvgIcon from './SvgIcon.vue';

export default {
  name: 'CreateView',
  components: {
    SvgIcon,
  },
  setup() {
    const surveyTitle = ref('Help me improve myself');
    const surveyDescription = ref('Share feedback about myself to improve my awareness');
    const newQuestion = ref({ text: '', response_type: 'scale' });
    const questions = ref([]);
    const creatorAnswers = ref([]);
    const isLoading = ref(false);
    const isSubmitted = ref(false);
    const errorMessage = ref('');
    const showSuccess = ref(false);
    const createdSurveyId = ref(null);
    const inputFocused = ref(false);

    const allQuestionsAnswered = computed(() => 
      questions.value.length > 0 &&
      creatorAnswers.value.length === questions.value.length &&
      creatorAnswers.value.every(answer => answer !== null && answer !== undefined)
    );

    function setQuestionType(type) {
      newQuestion.value.response_type = type;
    }

    function addQuestion() {
      if (newQuestion.value.text.trim() && !isSubmitted.value) {
        questions.value.push({
          id: Date.now(),
          text: newQuestion.value.text,
          response_type: newQuestion.value.response_type,
        });
        creatorAnswers.value.push(null);
        newQuestion.value.text = '';
        newQuestion.value.response_type = 'scale';
      }
    }

    function selectAnswer(index, value) {
      if (!isSubmitted.value) {
        creatorAnswers.value[index] = value;
      }
    }

    function celebrateSuccess() {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });
    }

    async function finishSurvey() {
      if (isSubmitted.value || !allQuestionsAnswered.value) return;
      
      isLoading.value = true;
      errorMessage.value = '';
      try {
        const surveyData = {
          title: surveyTitle.value,
          description: surveyDescription.value,
          questions: questions.value.map((q, index) => ({
            ...q,
            creator_answer: creatorAnswers.value[index]
          }))
        };
        const response = await api.createSurvey(surveyData);
        console.log('Survey created', response.data);
        createdSurveyId.value = response.data.survey_id;
        isSubmitted.value = true;
        showSuccess.value = true;
        celebrateSuccess();
      } catch (error) {
        console.error('Error creating survey:', error);
        errorMessage.value = 'Error creating survey. Please try again.' + error;
      } finally {
        isLoading.value = false;
      }
    }

    return {
      surveyTitle,
      surveyDescription,
      newQuestion,
      questions,
      creatorAnswers,
      isLoading,
      isSubmitted,
      errorMessage,
      showSuccess,
      createdSurveyId,
      allQuestionsAnswered,
      inputFocused,
      setQuestionType,
      addQuestion,
      selectAnswer,
      finishSurvey
    };
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;700&display=swap');

@keyframes blink {
  0% { opacity: 0; }
  50% { opacity: 1; }
  100% { opacity: 0; }
}

.animate-blink {
  animation: blink 1s infinite;
}
</style>