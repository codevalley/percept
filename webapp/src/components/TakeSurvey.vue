<template>
  <div class="font-sans min-h-screen bg-white">
    <div v-if="error" class="max-w-[768px] mx-auto px-4 pt-16 text-center">
      <p class="text-2xl text-accent">{{ error }}</p>
    </div>
    <div v-else class="max-w-[768px] mx-auto pt-16">
      <!-- User Code Input Section -->
      <div class="mb-8 flex justify-center">
        <FancyInput
          v-model="userCode"
          :icon="'/assets/user-icon.svg'"
          :placeholder="'user-name'"
          :is-checking="isCheckingCode"
          :is-valid="isCodeValid"
          :is-error="isCodeInvalid"
          :loader-color="'#BE185D'"
          :valid-border-color="'border-neutral-300'"
          :neutral-border-color="'border-neutral-300'"
          :text-color="'text-neutral-500'"
          :icon-color="'text-neutral-500'"
          @rotate="rotateCode"
          @input="handleCodeInput"
        />
      </div>

      <div v-if="loadedSurveyData">
        <!-- Combined Header and Question Section -->
        <div class="rounded-3xl overflow-hidden">
          <!-- Header Section -->
          <div class="bg-neutral-100 p-7">
            <div class="flex items-start">
              <div class="w-12 h-12 bg-secondary rounded-full mr-5 mt-3 flex-shrink-0"></div>
              <div>
                <h1 class="text-primary text-2xl font-semibold leading-10">{{ loadedSurveyData.title }}</h1>
                <p class="text-primary text-lg font-normal leading-7">{{ loadedSurveyData.description }}</p>
              </div>
            </div>
          </div>

          <!-- Question Section -->
          <div v-if="currentQuestion" class="bg-accent-green p-7 relative">
            <!-- Progress Bar -->
            <div class="w-full h-2.5 bg-neutral-200 absolute top-0 left-0 right-0">
              <div class="h-full bg-accent transition-all duration-300 ease-in-out" :style="{ width: `${progress}%` }"></div>
            </div>

            <!-- Question -->
            <div class="flex items-center mb-6">
              <inline-svg src="assets/question-icon.svg" class="w-7 h-7 mr-4 text-primary"/>
              <p class="text-primary text-2xl font-bold leading-9">{{ currentQuestion.text }}</p>
            </div>

            <!-- Answer Options -->
            <div class="flex justify-center space-x-5 mb-16">
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
                  <inline-svg src="/assets/yes-icon.svg" class="w-8 h-8" :class="currentAnswer === true ? 'text-white' : 'text-primary'"/>
                </button>
                <button 
                  @click="selectAnswer(false)"
                  :class="[
                    'w-14 h-14 rounded-full border-4 transition-colors flex items-center justify-center',
                    currentAnswer === false ? 'bg-primary border-primary' : 'bg-white border-neutral-200'
                  ]"
                >
                  <inline-svg src="/assets/no-icon.svg" class="w-8 h-8" :class="currentAnswer === false ? 'text-white' : 'text-primary'"/>
                </button>
              </template>
            </div>

            <!-- Navigation Buttons -->
            <div class="absolute bottom-4 left-4 right-4 flex justify-between">
              <button 
                @click="previousQuestion" 
                v-if="currentQuestionIndex > 0"
                class="px-6 py-2 bg-primary text-white rounded-full"
              >
                {{ $t('takeSurvey.previousButton') }}
              </button>
              <div class="flex-grow"></div>
              <button 
                @click="nextQuestion" 
                :disabled="currentAnswer === null || isSubmitting || !isCodeValid"
                :class="[
                  'px-6 py-2 rounded-full transition-colors',
                  (currentAnswer === null || isSubmitting || !isCodeValid) 
                    ? 'bg-white text-neutral-300 cursor-not-allowed' 
                    : 'bg-primary text-white'
                ]"
              >
                <span v-if="!isSubmitting">
                  {{ isLastQuestion ? $t('takeSurvey.finishButton') : $t('takeSurvey.nextButton') }}
                </span>
                <span v-else class="flex items-center">
                  <svg class="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                    <!-- Add your loading spinner SVG here -->
                  </svg>
                  {{ $t('takeSurvey.submittingButton') }}
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-else-if="isLoading" class="flex justify-center items-center">
        <p class="text-2xl text-primary">{{ $t('takeSurvey.loadingMessage') }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import api from '@/services/api';
import InlineSvg from 'vue-inline-svg';
import FancyInput from '@/components/FancyInput.vue';
import debounce from 'lodash/debounce';

export default {
  name: 'TakeSurvey',
  components: {
    InlineSvg,
    FancyInput,
  },
  props: {
    surveyId: {
      type: String,
      default: null
    },
    surveyData: {
      type: Object,
      default: null
    }
  },
  setup(props, { emit }) {
    const { t } = useI18n();
    const router = useRouter();
    const loadedSurveyData = ref(null);
    const error = ref(null);
    const currentQuestionIndex = ref(0);
    const answers = ref({});
    const currentAnswer = ref(null);
    const isSubmitting = ref(false);
    const isLoading = ref(true);
    const userCode = ref('');
    const availableCodes = ref([]);
    const codeStatus = ref(null);
    const isChecking = ref(false);

    const currentQuestion = computed(() => loadedSurveyData.value?.questions[currentQuestionIndex.value]);
    const progress = computed(() => ((currentQuestionIndex.value + 1) / loadedSurveyData.value?.questions.length) * 100);
    const isLastQuestion = computed(() => currentQuestionIndex.value === loadedSurveyData.value?.questions.length - 1);

    const isCheckingCode = computed(() => isChecking.value);
    const isCodeValid = computed(() => codeStatus.value === 'valid');
    const isCodeInvalid = computed(() => codeStatus.value === 'invalid');

    onMounted(async () => {
      if (!props.surveyId) {
        error.value = t('takeSurvey.missingSurveyId');
        isLoading.value = false;
        return;
      }

      try {
        await fetchInitialCode();
        if (props.surveyData) {
          loadedSurveyData.value = props.surveyData;
        } else {
          const response = await api.getSurvey(props.surveyId);
          loadedSurveyData.value = response.data;
        }
      } catch (err) {
        console.error('Error fetching survey:', err);
        handleError(err);
      } finally {
        isLoading.value = false;
      }
    });

    async function fetchInitialCode() {
      try {
        const response = await api.getIds(5);
        availableCodes.value = response.data.ids;
        userCode.value = availableCodes.value[0];
        codeStatus.value = 'valid';
      } catch (error) {
        console.error('Error fetching initial codes:', error);
        error.value = t('takeSurvey.errorFetchingCodes');
      }
    }

    function rotateCode() {
      const currentIndex = availableCodes.value.indexOf(userCode.value);
      const nextIndex = (currentIndex + 1) % availableCodes.value.length;
      userCode.value = availableCodes.value[nextIndex];
      codeStatus.value = 'valid';
    }

    const handleCodeInput = debounce(() => {
      if (isValidFormat(userCode.value)) {
        checkCodeAvailability();
      } else {
        codeStatus.value = 'invalid';
      }
    }, 300);

    function isValidFormat(code) {
      const validFormat = /^[a-zA-Z0-9-]+$/;
      return typeof code === 'string' && code.length >= 5 && validFormat.test(code);
    }

    async function checkCodeAvailability() {
      isChecking.value = true;
      codeStatus.value = null;
      try {
        const response = await api.checkIdAvailability(userCode.value);
        if (response.data.available) {
          codeStatus.value = 'valid';
        } else {
          codeStatus.value = 'invalid';
        }
      } catch (error) {
        console.error('Error checking code availability:', error);
        codeStatus.value = 'invalid';
      } finally {
        isChecking.value = false;
      }
    }

    function selectAnswer(value) {
      currentAnswer.value = value;
    }

    function previousQuestion() {
      if (currentQuestionIndex.value > 0) {
        currentQuestionIndex.value--;
        currentAnswer.value = answers.value[currentQuestion.value.id] || null;
      }
    }

    async function nextQuestion() {
      if (currentAnswer.value === null || !isCodeValid.value) return;

      answers.value[currentQuestion.value.id] = currentAnswer.value;
      
      if (isLastQuestion.value) {
        await submitSurvey();
      } else {
        currentQuestionIndex.value++;
        currentAnswer.value = answers.value[currentQuestion.value.id] || null;
      }
    }

    async function submitSurvey() {
      isSubmitting.value = true;
      try {
        const answersToSubmit = {
          answers: Object.entries(answers.value).map(([questionId, answer]) => ({
            question_id: questionId,
            answer
          })),
          user_code: userCode.value
        };
        const response = await api.submitAnswers(props.surveyId, answersToSubmit);
        
        if (!response.data.user_code) {
          throw new Error('User code not found in API response');
        }
        
        router.push({
          name: 'Results',
          params: { 
            surveyId: props.surveyId,
            userCode: response.data.user_code 
          }
        });
      } catch (error) {
        console.error('Error submitting survey:', error);
        handleError(error);
      } finally {
        isSubmitting.value = false;
      }
    }

    function handleError(err) {
      if (err.response) {
        switch (err.response.status) {
          case 404:
            error.value = t('takeSurvey.surveyNotFound');
            break;
          case 403:
            error.value = t('takeSurvey.surveyAccessDenied');
            break;
          default:
            error.value = t('takeSurvey.errorLoading');
        }
      } else if (err.request) {
        error.value = t('takeSurvey.networkError');
      } else {
        error.value = t('takeSurvey.errorLoading');
      }
      emit('survey-error', error.value);
    }

    return {
      loadedSurveyData,
      currentQuestionIndex,
      currentQuestion,
      currentAnswer,
      isSubmitting,
      isLoading,
      progress,
      isLastQuestion,
      selectAnswer,
      previousQuestion,
      nextQuestion,
      error,
      userCode,
      isCheckingCode,
      isCodeValid,
      isCodeInvalid,
      rotateCode,
      handleCodeInput,
    };
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;700&display=swap');
</style>