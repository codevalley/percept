<template>
  <div class="font-sans min-h-screen bg-white">
    <div v-if="error || isSurveyExpired" class="max-w-[768px] mx-auto px-4 pt-8 sm:pt-16 text-center">
      <p class="text-xl sm:text-2xl text-accent">
        {{ error || t('takeSurvey.surveyExpired') }}
      </p>
    </div>
    <div v-else-if="loadedSurveyData && loadedSurveyData.questions" class="max-w-[768px] mx-auto px-4 pt-8 sm:pt-16">
      <div v-if="loadedSurveyData">
        <!-- Privacy Note -->
        <div class="mb-2">
          <div class="inline-flex items-center px-2 py-1 bg-gray-100 text-gray-600 rounded-full text-xs font-semibold h-6">
            <inline-svg src="/assets/safe-icon.svg" class="w-4 h-4 mr-1 flex-shrink-0"/>
            <span class="whitespace-nowrap leading-none">
              {{ $t('takeSurvey.privacyNote') }}
            </span>
          </div>
        </div>
        <!-- Combined Header and Question Section -->
        <div class="rounded-3xl overflow-hidden">
          <!-- Header Section -->
          <div class="bg-neutral-100 p-4 sm:p-7">
            <!-- SurveyChips just above the title -->
            <div class="mb-2">
              <SurveyChips 
                :is-trending="loadedSurveyData.is_trending"
                :participant-bucket="loadedSurveyData.participant_bucket"
                :time-left="timeLeftInMinutes"
              />
            </div>

            <div class="flex items-start">
              <div class="w-10 h-10 sm:w-12 sm:h-12 bg-secondary rounded-full mr-3 sm:mr-5 mt-1 sm:mt-3 flex-shrink-0"></div>
              <div>
                <h1 class="text-primary text-xl sm:text-2xl font-semibold leading-8 sm:leading-10">{{ loadedSurveyData.title }}</h1>
                <p class="text-primary text-base sm:text-lg font-normal leading-6 sm:leading-7">{{ loadedSurveyData.description }}</p>
              </div>
            </div>
          </div>

          <!-- Question Section -->
          <div v-if="currentQuestion" class="bg-accent-green p-4 sm:p-7 relative min-h-[300px]">
            <!-- Progress Bar -->
            <div class="w-full h-2 sm:h-2.5 bg-neutral-200 absolute top-0 left-0 right-0">
              <div class="h-full bg-accent transition-all duration-300 ease-in-out" :style="{ width: `${progress}%` }"></div>
            </div>

            <!-- Question -->
            <div class="flex items-center mb-4 sm:mb-6 mt-3 sm:mt-0">
              <inline-svg src="assets/question-icon.svg" class="w-6 h-6 sm:w-7 sm:h-7 mr-3 sm:mr-4 text-primary"/>
              <p class="text-primary text-lg sm:text-2xl font-bold leading-7 sm:leading-9">{{ currentQuestion.text }}</p>
            </div>

            <!-- Answer Options -->
            <div class="flex justify-center space-x-2 sm:space-x-5 mb-2 sm:mb-3">
              <template v-if="currentQuestion.response_type === 'scale'">
                <div v-for="n in (currentQuestion.response_scale_max || 5)" :key="n" class="flex flex-col items-center">
                  <button 
                    @click="selectAnswer(n)"
                    :disabled="currentAnswer !== null"
                    :class="[
                      'w-10 h-10 sm:w-14 sm:h-14 rounded-full border-2 sm:border-4 transition-colors flex items-center justify-center text-sm sm:text-base mb-1',
                      n === currentAnswer ? 'bg-primary border-primary text-white' : 
                      currentAnswer !== null ? 'bg-white border-neutral-300 text-neutral-300' :
                      'bg-white border-neutral-200 text-primary hover:bg-neutral-100'
                    ]"
                  >
                    {{ n }}
                  </button>
                  <div class="h-6 flex items-center justify-center mt-1">
                    <transition name="fade" mode="out-in">
                      <div v-if="showDistribution && currentAnswer !== null" 
                           class="bg-gray-100 rounded-full px-2 py-0.5 text-xs text-gray-600 w-14 text-center">
                        <AnimatedNumber 
                          :value="currentQuestion.answer_distribution[n] || 0" 
                          :duration="0.5"
                          :precision="1"
                          :format="(num) => `${num}%`"
                          @animationStart="showAnswerTrendLabel = true"
                        />
                      </div>
                      <div v-else class="invisible bg-gray-100 rounded-full px-2 py-0.5 text-xs w-14 text-center">
                        00.0%
                      </div>
                    </transition>
                  </div>
                </div>
              </template>
              <template v-else-if="currentQuestion.response_type === 'boolean'">
                <div v-for="option in ['true', 'false']" :key="option" class="flex flex-col items-center">
                  <button 
                    @click="selectAnswer(option === 'true')"
                    :disabled="currentAnswer !== null"
                    :class="[
                      'w-10 h-10 sm:w-14 sm:h-14 rounded-full border-2 sm:border-4 transition-colors flex items-center justify-center mb-1',
                      currentAnswer === (option === 'true') ? 'bg-primary border-primary' : 
                      currentAnswer !== null ? 'bg-white border-neutral-300' :
                      'bg-white border-neutral-200 hover:bg-neutral-100'
                    ]"
                  >
                    <inline-svg :src="option === 'true' ? '/assets/yes-icon.svg' : '/assets/no-icon.svg'" 
                                class="w-6 h-6 sm:w-8 sm:h-8" 
                                :class="currentAnswer === (option === 'true') ? 'text-white' : currentAnswer !== null ? 'text-neutral-300' : 'text-primary'"/>
                  </button>
                  <div class="h-6 flex items-center justify-center mt-1">
                    <transition name="fade" mode="out-in">
                      <div v-if="showDistribution && currentAnswer !== null" 
                           class="bg-gray-100 rounded-full px-2 py-0.5 text-xs text-gray-600 w-14 text-center">
                        <AnimatedNumber 
                          :value="currentQuestion.answer_distribution[`${option}_percentage`] || 0" 
                          :duration="0.5"
                          :precision="1"
                          :format="(num) => `${num}%`"
                          @animationStart="showAnswerTrendLabel = true"
                        />
                      </div>
                      <div v-else class="invisible bg-gray-100 rounded-full px-2 py-0.5 text-xs w-14 text-center">
                        00.0%
                      </div>
                    </transition>
                  </div>
                </div>
              </template>
            </div>

            <!-- Answer trend footnote -->
            <div class="text-center h-4 -mt-2">
              <transition name="fade" mode="out-in">
                <span v-if="showDistribution && currentAnswer !== null && showAnswerTrendLabel" class="text-xs text-gray-600">
                  Answer trend
                </span>
                <span v-else class="text-xs text-transparent">Answer trend</span>
              </transition>
            </div>


            <!-- Navigation Buttons and User Code Input -->
            <!-- Mobile Navigation -->
            <div class="sm:hidden flex flex-col items-center space-y-4 mt-8">
              <div class="w-full flex justify-center">
                <FancyInput
                  v-model="userCode"
                  :icon="'/assets/user-icon.svg'"
                  placeholder="user-name"
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
                  v-tooltip="'Your unique participant code'"
                  class="w-full max-w-xs"
                />
              </div>
              <p class="text-xs text-neutral-500">Your unique participant code</p>
              <div class="flex justify-between w-full space-x-2">
                <button 
                  @click="previousQuestion" 
                  class="px-4 sm:px-6 py-2 bg-primary text-white rounded-full text-sm sm:text-base"
                  :class="{ 'invisible': currentQuestionIndex === 0 }"
                >
                  {{ $t('takeSurvey.previousButton') }}
                </button>
                <FancyButton
                  :label="isLastQuestion ? $t('takeSurvey.finishButton') : $t('takeSurvey.nextButton')"
                  :disabled="currentAnswer === null || isSubmitting || !isCodeValid || isSurveyExpired"
                  :is-actioning="isSubmitting"
                  @click="nextQuestion"
                  :border-width="2"
                  button-height="40px"
                  icon-size="20px"
                  font-size="text-sm sm:text-base"
                  :min-width="'100px'"
                  bg-color="black"
                  border-color="primary"
                  loader-color="#6B7280"
                  disabled-bg-color="gray"
                  disabled-border-color="neutral-300"
                  text-color="text-white"
                  disabled-text-color="text-neutral-300"
                />
              </div>
            </div>

            <!-- Desktop Navigation -->
            <div class="hidden sm:flex items-center justify-between w-full space-x-2 mt-8">
              <button 
                @click="previousQuestion" 
                class="px-4 sm:px-6 py-2 bg-primary text-white rounded-full text-sm sm:text-base"
                :class="{ 'invisible': currentQuestionIndex === 0 }"
              >
                {{ $t('takeSurvey.previousButton') }}
              </button>
              <div class="flex justify-center flex-grow">
                <FancyInput
                  v-model="userCode"
                  :icon="'/assets/user-icon.svg'"
                  placeholder="user-name"
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
                  v-tooltip="'Your unique participant code'"
                  class="w-full max-w-xs"
                />
              </div>
              <FancyButton
                :label="isLastQuestion ? $t('takeSurvey.finishButton') : $t('takeSurvey.nextButton')"
                :disabled="currentAnswer === null || isSubmitting || !isCodeValid"
                :is-actioning="isSubmitting"
                @click="nextQuestion"
                :border-width="2"
                button-height="40px"
                icon-size="20px"
                font-size="text-sm sm:text-base"
                :min-width="'100px'"
                bg-color="black"
                border-color="primary"
                loader-color="#6B7280"
                disabled-bg-color="gray"
                disabled-border-color="neutral-300"
                text-color="text-white"
                disabled-text-color="text-neutral-300"
              />
            </div>

          </div>
        </div>
      </div>
      <div v-else-if="isLoading" class="flex justify-center items-center h-64">
        <p class="text-xl sm:text-2xl text-primary">{{ $t('takeSurvey.loadingMessage') }}</p>
      </div>
    </div>
    <div v-else class="flex justify-center items-center h-64">
      <p class="text-xl sm:text-2xl text-primary">{{ $t('takeSurvey.loadingMessage') }}</p>
    </div>
  </div>
</template>



<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import api from '@/services/api';
import InlineSvg from 'vue-inline-svg';
import FancyInput from '@/components/FancyInput.vue';
import debounce from 'lodash/debounce';
import { useHead } from '@vueuse/head'
import FancyButton from '@/components/FancyButton.vue';
import SurveyChips from '@/components/SurveyChips.vue';
import AnimatedNumber from './ui/AnimatedNumber.vue';

const MINIMUM_RESPONSES = 5;
export default {
  name: 'TakeSurvey',
  components: {
    InlineSvg,
    FancyInput,
    FancyButton,
    SurveyChips,
    AnimatedNumber,
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

    const currentQuestion = computed(() => {
      if (loadedSurveyData.value && Array.isArray(loadedSurveyData.value.questions)) {
        return loadedSurveyData.value.questions[currentQuestionIndex.value] || null;
      }
      return null;
    });
    watch([currentQuestion, answers], () => {
      if (currentQuestion.value) {
        currentAnswer.value = answers.value[currentQuestion.value.id] || null;
      }
    }, { immediate: true });
    const progress = computed(() => {
      if (loadedSurveyData.value && Array.isArray(loadedSurveyData.value.questions) && loadedSurveyData.value.questions.length > 0) {
        return ((currentQuestionIndex.value + 1) / loadedSurveyData.value.questions.length) * 100;
      }
      return 0;
    });
    const isLastQuestion = computed(() => {
      if (loadedSurveyData.value && Array.isArray(loadedSurveyData.value.questions)) {
        return currentQuestionIndex.value === loadedSurveyData.value.questions.length - 1;
      }
      return false;
    });
    const showDistribution = computed(() => {
      return loadedSurveyData.value && 
            loadedSurveyData.value.status === 'complete' && 
            currentQuestion.value && 
            currentQuestion.value.answer_distribution &&
            Object.keys(currentQuestion.value.answer_distribution).length > 0;
    });
    const isCheckingCode = computed(() => isChecking.value);
    const isCodeValid = computed(() => codeStatus.value === 'valid');
    const isCodeInvalid = computed(() => codeStatus.value === 'invalid');

    const baseUrl = computed(() => process.env.VUE_APP_BASE_URL || '');
    
    const isSurveyExpired = computed(() => {
      if (!loadedSurveyData.value || !loadedSurveyData.value.expiration_date) {
        return false;
      }
      const expirationDate = new Date(loadedSurveyData.value.expiration_date);
      return expirationDate < new Date();
    });
    useHead(() => {
      if (!loadedSurveyData.value) return {}

      const title = `${loadedSurveyData.value.title} - Backwave Survey`;
      const description = loadedSurveyData.value.description || "Take this survey and provide valuable feedback.";
      const url = `${baseUrl.value}/participate/${props.surveyId}`;
      const image = `${baseUrl.value}/og-image.png`; // Make sure this image exists in your public folder

      return {
        title: title,
        meta: [
          { property: 'og:title', content: title },
          { property: 'og:description', content: description },
          { property: 'og:url', content: url },
          { property: 'og:image', content: image },
          { property: 'og:type', content: 'website' },
          { name: 'twitter:title', content: title },
          { name: 'twitter:description', content: description },
          { name: 'twitter:url', content: url },
          { name: 'twitter:image', content: image },
          { name: 'twitter:card', content: 'summary_large_image' },
        ],
      }
    })
    const timeLeftInSeconds = ref(0);
    const timeLeftInMinutes = computed(() => {
      return Math.ceil(timeLeftInSeconds.value / 60);
    });

    const calculateTotalTime = (questions) => {
      return questions.reduce((total, question) => {
        return total + (question.response_type === 'boolean' ? 15 : 30);
      }, 0);
    };

    const updateTimeLeft = () => {
      if (loadedSurveyData.value && Array.isArray(loadedSurveyData.value.questions)) {
        const unansweredQuestions = loadedSurveyData.value.questions.slice(currentQuestionIndex.value);
        timeLeftInSeconds.value = calculateTotalTime(unansweredQuestions);
      }
    };

    watch(currentQuestionIndex, updateTimeLeft);
    
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
          console.log('API Response:', JSON.stringify(response.data, null, 2));
          loadedSurveyData.value = response.data;
        }
        if (loadedSurveyData.value) {
          // Ensure total_responses is included
          if (typeof loadedSurveyData.value.total_responses === 'undefined') {
            loadedSurveyData.value.total_responses = 0; // or some default value
          }
          if (isSurveyExpired.value) {
            error.value = t('takeSurvey.surveyExpired');
          } else {
            updateTimeLeft();
          }
          // Initialize answer distributions if not present
          if (Array.isArray(loadedSurveyData.value.questions)) {
            loadedSurveyData.value.questions.forEach(question => {
              if (!question.answer_distribution) {
                question.answer_distribution = question.response_type === 'boolean' 
                  ? { true_percentage: 0, false_percentage: 0 }
                  : {};
              }
            });
          } else {
            console.error('loadedSurveyData.questions is not an array:', loadedSurveyData.value);
            error.value = t('takeSurvey.invalidSurveyData');
          }
        }
      } catch (err) {
          console.error('Error fetching survey:', err);
          handleError(err);
        } finally {
          isLoading.value = false;
        }
      }
    );

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

    const showAnswerTrendLabel = ref(false);

    function selectAnswer(value) {
      if (currentQuestion.value) {
        currentAnswer.value = value;
        answers.value[currentQuestion.value.id] = value;
        showAnswerTrendLabel.value = false; // Reset the label visibility
      }
    }

    async function previousQuestion() {
      if (currentQuestionIndex.value > 0) {
        currentQuestionIndex.value--;
        currentAnswer.value = answers.value[currentQuestion.value.id] || null;
        showAnswerTrendLabel.value = false; // Reset the label visibility
      }
    }

    async function nextQuestion() {
      if (currentAnswer.value === null || !isCodeValid.value || isSurveyExpired.value) return;

      if (isLastQuestion.value) {
        await submitSurvey();
      } else {
        currentQuestionIndex.value++;
        currentAnswer.value = answers.value[currentQuestion.value.id] || null;
        showAnswerTrendLabel.value = false; // Reset the label visibility
        updateTimeLeft();
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
        
        // Navigate to results page after a short delay
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
          case 410:
            error.value = t('takeSurvey.surveyExpired');
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
      timeLeftInMinutes,
      isSurveyExpired,
      showDistribution,
      MINIMUM_RESPONSES,
      showAnswerTrendLabel,
    };
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;700&display=swap');

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>