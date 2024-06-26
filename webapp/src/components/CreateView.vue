<template>
  <div class="font-['IBM_Plex_Sans']  min-h-screen bg-white ">
    <SiteHeader initialPage="create" @page-changed="handlePageChange" />
    <div class="max-w-[859px] mx-auto">
      <div class="flex items-start mb-4">
        <!-- Profile Icon -->
        <div class="w-14 h-14 bg-secondary rounded-full mr-5 flex-shrink-0 mt-2"></div>
        
        <!-- Header Section -->
        <div class="flex-grow">
          <h1 class="text-primary text-4xl font-semibold leading-10  text-left">{{ surveyTitle }}</h1>
          <p class="text-primary text-lg font-normal leading-7 text-left">{{ surveyDescription }}</p>
        </div>
      </div>

      <template v-if="!isPublished">
        <!-- Question Input Section -->
        <div class="bg-neutral-400 rounded-[25px] p-7 mb-12 relative">
          <div class="relative flex items-center mb-6">
            <inline-svg src="assets/question-icon.svg" class="text-primary mr-2 mt-1" />
            <input 
              v-model="newQuestion.text" 
              @keyup.enter="addQuestion"
              @focus="inputFocused = true"
              @blur="inputFocused = false"
              class="w-full bg-transparent text-[34px] font-bold text-primary focus:outline-none"
              :placeholder="inputFocused ? '' : 'Enter your question here'"
              :disabled="isSubmitted"
            >
            <span v-if="!newQuestion.text && !inputFocused" class="absolute right-0 top-1/2 transform -translate-y-1/2 text-neutral-300 text-[34px] font-bold animate-blink">_</span>
          </div>
          <div class="flex justify-between items-center">
            <div class="flex space-x-5">
              <!-- Scale button -->
              <button 
                @click="setQuestionType('scale')"
                :class="['w-28 h-10 rounded-full flex items-center justify-center space-x-2 border border-neutral-100', 
                        newQuestion.response_type === 'scale' ? 'bg-primary text-white' : 'bg-white text-primary']"
                :disabled="isSubmitted"
              >
                <inline-svg src="assets/scale-icon.svg" :class="newQuestion.response_type === 'scale' ? 'text-white' : 'text-primary'" 
                            class="w-6 h-6"
                            :key="newQuestion.response_type === 'scale' ? 'scale' : 'default'" />
                <span class="text-base font-medium">Rating</span>
              </button>

              <!-- Yes/No button -->
              <button 
                @click="setQuestionType('boolean')"
                :class="['w-28 h-10 rounded-full flex items-center justify-center space-x-2 border border-neutral-100', 
                        newQuestion.response_type === 'boolean' ? 'bg-primary text-white' : 'bg-white text-primary']"
                :disabled="isSubmitted"
              >
                <inline-svg src="assets/yes-no-icon.svg"  
                            :class="newQuestion.response_type === 'boolean' ? 'text-white' : 'text-primary'"
                            class="w-6 h-6"
                            :key="newQuestion.response_type === 'boolean' ? 'boolean' : 'default'"
                            />
                <span class="text-base font-medium">Yes/No</span>
              </button>
            </div>

            <!-- Add button -->
            <button 
              @click="addQuestion"
              :disabled="!newQuestion.text.trim() || isSubmitted"
              :class="[
                'w-28 h-10 rounded-full flex items-center justify-center space-x-2 border',
                !newQuestion.text.trim() || isSubmitted 
                  ? 'bg-gray-200 disabled text-neutral-300 border-neutral-100' 
                  : 'bg-accent-green text-white border-accent-green'
              ]"
            >
              <span class="text-base font-medium">Add</span>
            </button>
          </div>
        </div>

        <!-- Posted Questions -->
        <div v-if="questions.length > 0" class="bg-neutral-500 rounded-[25px] p-7 space-y-6 mb-12">
          <div v-for="(question, index) in questions" :key="question.id" class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <inline-svg :src="question.response_type === 'scale' ? 'assets/scale-icon.svg' : 'assets/yes-no-icon.svg'"  
                          :class="creatorAnswers[index] !== null ? 'text-primary' : 'text-neutral-300'" class="w-6 h-6"/>
              <span :class="['text-2xl font-bold', creatorAnswers[index] !== null ? 'text-primary' : 'text-neutral-300']">
                {{ question.text }}
              </span>
            </div>
            <div v-if="question.response_type === 'scale'" class="flex space-x-3">
              <button 
                v-for="n in 5" 
                :key="n"
                @click="selectAnswer(index, n)"
                :class="['w-[30px] h-[30px] rounded-full border flex items-center justify-center', 
                        n <= creatorAnswers[index] ? 'bg-primary border-primary' : 'bg-neutral-200 border-neutral-200']"
                :disabled="isSubmitted"
              >
                <div :class="['w-[18px] h-[18px] rounded-full', n <= creatorAnswers[index] ? 'bg-white' : 'bg-transparent']"></div>
              </button>
            </div>
            <div v-else class="flex space-x-3">
              <button 
                @click="selectAnswer(index, true)"
                :class="['w-[30px] h-[30px] rounded-full border flex items-center justify-center', 
                        creatorAnswers[index] === true ? 'bg-primary border-primary' : 'bg-neutral-200 border-neutral-200']"
                :disabled="isSubmitted"
              >
                <inline-svg 
                  src="assets/yes-icon.svg" 
                  :class="[
                    'w-4 h-4', 
                    creatorAnswers[index] === true ? 'text-white' : 'text-neutral-300'
                  ]" 
                />
              </button>
              <button 
                @click="selectAnswer(index, false)"
                :class="['w-[30px] h-[30px] rounded-full border flex items-center justify-center', 
                        creatorAnswers[index] === false ? 'bg-primary border-primary' : 'bg-neutral-200 border-neutral-200']"
                :disabled="isSubmitted"
              >
                <inline-svg 
                  src="assets/no-icon.svg" 
                  :class="[
                    'w-4 h-4', 
                    creatorAnswers[index] === false ? 'text-white' : 'text-neutral-300'
                  ]" 
                />
              </button>
            </div>
          </div>
        </div>

        <!-- Publish Button -->
        <div class="text-left">
          <button 
            @click="finishSurvey"
            :disabled="!allQuestionsAnswered || isLoading || isSubmitted"
            :class="[
              'w-[152px] h-[56px] rounded-full text-center text-2xl font-bold leading-9',
              !allQuestionsAnswered || isLoading || isSubmitted
                ? 'bg-gray-100 text-neutral-300'
                : 'bg-accent-green text-white'
            ]"
          >
            Publish
          </button>
        </div>

        <!-- Alert Box -->
        <div v-if="!allQuestionsAnswered" class="flex items-center space-x-2 mb-6 text-accent" style="padding-top: 20px;">
          <inline-svg src="assets/info-icon.svg" class="text-accent w-5 h-5"/>
          <span class="text-sm font-medium">Complete self review before publishing</span>
        </div>
      </template>

      <!-- Published Section -->
      <div v-if="isPublished" class="bg-[#D8F89D] rounded-[25px] p-7 mb-12">
        <div class="w-full text-sky-950 text-2xl font-bold font-['IBM Plex Sans'] leading-9 mb-6 text-left">
          The review is published and live!
        </div>
        
        <div class="flex items-center justify-start space-x-4">
          <div class="flex items-center space-x-4">
            <span class="text-primary text-lg font-normal leading-7 whitespace-nowrap">Review code</span>
            <button 
              class="h-10 bg-accent-green text-white rounded-full flex items-center justify-between px-4 border border-accent-green"
              @click="copyToClipboard(surveyCode)"
            >
              <span class="text-base font-medium mr-2">{{ surveyCode }}</span>
              <inline-svg src="assets/copy-icon.svg" class="w-5 h-5 text-white" />
            </button>
          </div>
          
          <div class="flex items-center space-x-4">
            <span class="text-primary text-lg font-normal leading-7 whitespace-nowrap">Review Link</span>
            <button 
              class="h-10 bg-accent-green text-white rounded-full flex items-center justify-between px-4 border border-accent-green"
              @click="copyToClipboard(surveyLink)"
            >
              <span class="text-base font-medium mr-2">Copy URL</span>
              <inline-svg src="assets/copy-icon.svg" class="w-5 h-5 text-white" />
            </button>
          </div>
        </div>

      </div>
    </div>
    <ToastView :message="toastMessage" :type="toastType" @hidden="clearToast" />
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import api from '@/services/api';
import confetti from 'canvas-confetti';
import InlineSvg from 'vue-inline-svg';
import SiteHeader from './SiteHeader.vue';
import ToastView from '@/components/ToastView.vue';

export default {
  name: 'CreateView',
  components: {
    InlineSvg,
    ToastView,
    SiteHeader,
  },
  setup() {
    const surveyTitle = ref('Help me improve myself');
    const surveyDescription = ref('Share feedback about myself to improve my awareness');
    const newQuestion = ref({ text: '', response_type: 'scale' });
    const questions = ref([]);
    const creatorAnswers = ref([]);
    const isLoading = ref(false);
    const isSubmitted = ref(false);
    const isPublished = ref(false);
    const errorMessage = ref('');
    const showSuccess = ref(false);
    const surveyCode = ref('');
    const surveyLink = ref('');
    const inputFocused = ref(false);
    const toastMessage = ref('');
    const toastType = ref('');

    const allQuestionsAnswered = computed(() => 
      questions.value.length > 0 &&
      creatorAnswers.value.length === questions.value.length &&
      creatorAnswers.value.every(answer => answer !== null && answer !== undefined)
    );

    const isAddButtonDisabled = computed(() => !newQuestion.value.text.trim() || isSubmitted.value);

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

    function clearToast() {
      toastMessage.value = '';
      toastType.value = '';
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
        surveyCode.value = response.data.survey_id;
        surveyLink.value = response.data.share_link;
        isSubmitted.value = true;
        isPublished.value = true;
        showSuccess.value = true;
        celebrateSuccess();
        toastMessage.value = 'Survey created successfully!';
        toastType.value = 'success';
      } catch (error) {
        console.error('Error creating survey:', error);
        errorMessage.value = 'Error creating survey. Please try again.';
        toastMessage.value = 'Failed to create survey. Please try again.';
        toastType.value = 'error';
      } finally {
        isLoading.value = false;
      }
    }

    function copyToClipboard(text) {
      navigator.clipboard.writeText(text).then(() => {
        toastMessage.value = 'Copied to clipboard!';
        toastType.value = 'success';
      }, (err) => {
        console.error('Could not copy text: ', err);
        toastMessage.value = 'Failed to copy to clipboard';
        toastType.value = 'error';
      });
    }
    const handlePageChange = (page) => {
      console.log(`Page changed to: ${page}`);
      // Here you would typically handle navigation, but since we don't have a router,
      // we'll just log it for now. In a full app, you might emit an event to a parent
      // component to handle the navigation.
    };

    return {
      surveyTitle,
      surveyDescription,
      newQuestion,
      questions,
      creatorAnswers,
      isLoading,
      isSubmitted,
      isPublished,
      errorMessage,
      showSuccess,
      surveyCode,
      surveyLink,
      allQuestionsAnswered,
      inputFocused,
      isAddButtonDisabled,
      toastMessage,
      toastType,
      setQuestionType,
      addQuestion,
      selectAnswer,
      finishSurvey,
      clearToast,
      handlePageChange,
      copyToClipboard
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