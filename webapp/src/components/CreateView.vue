<template>
  <div class="font-['IBM_Plex_Sans'] min-h-screen bg-white relative">
    <div class="max-w-[859px] mx-auto px-4 sm:px-6 pb-24 sm:pb-0">
      
      <!-- Header Section -->
      <div class="flex items-center mb-4 sm:mb-6">
        <div class="w-20 h-20 sm:w-14 sm:h-14 bg-secondary rounded-full mr-5 flex-shrink-0"></div>
        <div class="flex-grow">
          <input
            v-model="surveyTitle"
            class="text-neutral-600 text-xl sm:text-2xl font-semibold leading-8 sm:leading-10 w-full bg-transparent focus:outline-none mb-2"
            maxlength="36"
          />
          <input
            v-model="surveyDescription"
            class="text-neutral-600 text-base sm:text-lg font-normal leading-6 sm:leading-7 w-full bg-transparent focus:outline-none"
            maxlength="96"
          />
        </div>
      </div>

      <template v-if="!isPublished">
        
        <!-- Question Creation Section -->
        <div class="bg-neutral-100 rounded-[25px] p-4 sm:p-7 mb-8 sm:mb-12 relative">
          <div class="relative flex items-start mb-6">
            <inline-svg src="assets/question-icon.svg" class="text-primary mr-2 mt-1 hidden sm:block" />
            <div class="relative w-full">
              <textarea
                v-model="newQuestion.text"
                @keyup.enter="handleAddOrSuggest"
                @input="handleQuestionChange"
                @focus="inputFocused = true"
                @blur="inputFocused = false"
                class="w-full bg-transparent text-xl sm:text-[28px] font-regular text-primary focus:outline-none pr-10 transition-all duration-300 ease-in-out transform hover:scale-102 focus:scale-102 resize-none"
                :placeholder="placeholderText"
                :disabled="isSubmitted"
                rows="2"
              ></textarea>
              <inline-svg
                v-if="newQuestion.isAutogenerated"
                src="assets/magic-icon.svg"
                class="absolute right-2 top-2 w-6 h-6 text-neutral-300"
              />
            </div>
          </div>

          <div class="flex flex-col sm:flex-row justify-between items-stretch sm:items-center space-y-4 sm:space-y-0">
            <div class="flex space-x-4 sm:space-x-5">
              <button
                @click="setQuestionType('scale')"
                :class="[
                  'flex-1 sm:w-28 h-10 rounded-full flex items-center justify-center space-x-2 border border-neutral-300',
                  newQuestion.response_type === 'scale' ? 'bg-primary text-white' : 'bg-white text-primary'
                ]"
                :disabled="isSubmitted"
              >
                <inline-svg
                  src="assets/scale-icon.svg"
                  :class="newQuestion.response_type === 'scale' ? 'text-white' : 'text-primary'"
                  class="w-6 h-6"
                  :key="newQuestion.response_type === 'scale' ? 'scale' : 'default'"
                />
                <span class="text-base font-medium">Rating</span>
              </button>
              <button
                @click="setQuestionType('boolean')"
                :class="[
                  'flex-1 sm:w-28 h-10 rounded-full flex items-center justify-center space-x-2 border border-neutral-300',
                  newQuestion.response_type === 'boolean' ? 'bg-primary text-white' : 'bg-white text-primary'
                ]"
                :disabled="isSubmitted"
              >
                <inline-svg
                  src="assets/yes-no-icon.svg"
                  :class="newQuestion.response_type === 'boolean' ? 'text-white' : 'text-primary'"
                  class="w-6 h-6"
                  :key="newQuestion.response_type === 'boolean' ? 'boolean' : 'default'"
                />
                <span class="text-base font-medium">Yes/No</span>
              </button>
            </div>

            <div class="flex items-center space-x-2 justify-end sm:justify-start">
              <transition name="fade-scale" mode="out-in">
                <button
                  v-if="newQuestion.text.trim() && !newQuestion.isAutogenerated"
                  key="magic-button"
                  @click="suggestReplacementQuestion"
                  class="w-14 sm:w-10 h-10 rounded-full flex items-center justify-center bg-accent"
                  :disabled="isSubmitted"
                  v-tooltip="'Want some question suggestions?'"
                >
                  <inline-svg src="assets/magic-icon.svg" class="w-5 h-5 text-white" />
                </button>
              </transition>
              <transition name="fade-scale" mode="out-in">
                <button
                  @click="handleAddOrSuggest"
                  :disabled="isSubmitted"
                  :key="newQuestion.text.trim() ? (editingQuestionIndex !== null ? 'update' : 'add') : 'suggest'"
                  :class="[
                    'flex-1 sm:w-32 h-10 rounded-full flex items-center justify-center space-x-2 border',
                    newQuestion.text.trim() && !isSubmitted
                      ? 'bg-accent-green text-primary border-accent-green'
                      : isSubmitted
                        ? 'bg-gray-200 text-neutral-300 border-neutral-100'
                        : 'bg-accent text-white border-accent'
                  ]"
                >
                  <inline-svg
                    :src="newQuestion.text.trim() ? 'assets/yes-icon.svg' : 'assets/magic-icon.svg'"
                    class="w-5 h-5 mr-1"
                    :class="newQuestion.text.trim() ? 'text-primary' : 'text-white'"
                  />
                  <span class="text-base font-medium">
                    {{ newQuestion.text.trim() ? (editingQuestionIndex !== null ? 'Update' : 'Add') : 'Suggest' }}
                  </span>
                </button>
              </transition>
            </div>
          </div>
        </div>

        <!-- Question List Section -->
        <div v-if="questions.length > 0" class="bg-neutral-100 rounded-[25px] p-4 sm:p-7 mb-8 sm:mb-12">
          <SortableList
            v-model="questions"
            :disabled="isSubmitted"
            @update:modelValue="handleQuestionReorder"
          >
            <template #default="{ item: question }">
              <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between p-4 sm:p-0 bg-white sm:bg-transparent rounded-2xl sm:rounded-none shadow-sm sm:shadow-none mb-4 relative">
                <div class="flex items-start sm:items-center mb-4 sm:mb-0 sm:flex-grow sm:mr-4">
                  <button
                    @click="editQuestion(question.index)"
                    class="text-accent hover:text-accent-dark focus:outline-none mr-2 sm:ml-0 flex-shrink-0 z-10"
                  >
                    <inline-svg src="assets/edit-icon.svg" class="w-5 h-5" />
                  </button>
                  <div class="relative flex-grow">
                    <TextAnimate
                      :key="question.id"
                      :text="question.text"
                      type="fadeIn"
                      :delay="0.1"
                      :duration="0.5"
                      :disable-animation="isReordering"
                      class="text-lg sm:text-2xl sm:mr-2 break-words z-0"
                      :class="creatorAnswers[question.id] !== null ? 'text-primary' : 'text-neutral-400 sm:text-primary'"
                    />
                    <inline-svg
                      v-if="question.isAutogenerated"
                      src="assets/magic-icon.svg"
                      class="absolute top-0 right-0 w-5 h-5 text-accent ml-2 z-10"
                    />
                  </div>
                </div>

                <div class="flex justify-center sm:justify-end items-center space-x-2 sm:space-x-3 z-10">
                  <div
                    v-if="question.response_type === 'scale'"
                    class="flex space-x-2 sm:space-x-3"
                    v-tooltip="question.index === 0 ? 'Add a self-assessment first to baseline the answers' : ''"
                  >
                    <button
                      v-for="n in 5"
                      :key="n"
                      @click="selectAnswer(question.id, n)"
                      :class="[
                        'w-8 h-8 sm:w-[30px] sm:h-[30px] rounded-full border flex items-center justify-center transition-colors duration-200 ease-in-out',
                        n <= creatorAnswers[question.id] ? 'bg-primary border-primary' : 'bg-white border-neutral-300'
                      ]"
                      :disabled="isSubmitted"
                    >
                      <div
                        :class="[
                          'w-4 h-4 sm:w-[18px] sm:h-[18px] rounded-full',
                          n <= creatorAnswers[question.id] ? 'bg-white' : 'bg-transparent'
                        ]"
                      ></div>
                    </button>
                  </div>

                  <div
                    v-else
                    class="flex space-x-2 sm:space-x-3"
                    v-tooltip="question.index === 0 ? 'Add a self-assessment first to baseline the answers' : ''"
                  >
                    <button
                      @click="selectAnswer(question.id, true)"
                      :class="[
                        'w-8 h-8 sm:w-[30px] sm:h-[30px] rounded-full border flex items-center justify-center transition-colors duration-200 ease-in-out',
                        creatorAnswers[question.id] === true ? 'bg-primary border-primary' : 'bg-white border-neutral-300'
                      ]"
                      :disabled="isSubmitted"
                    >
                      <inline-svg
                        src="assets/yes-icon.svg"
                        :class="['w-4 h-4', creatorAnswers[question.id] === true ? 'text-white' : 'text-neutral-300']"
                      />
                    </button>
                    <button
                      @click="selectAnswer(question.id, false)"
                      :class="[
                        'w-8 h-8 sm:w-[30px] sm:h-[30px] rounded-full border flex items-center justify-center transition-colors duration-200 ease-in-out',
                        creatorAnswers[question.id] === false ? 'bg-primary border-primary' : 'bg-white border-neutral-300'
                      ]"
                      :disabled="isSubmitted"
                    >
                      <inline-svg
                        src="assets/no-icon.svg"
                        :class="['w-4 h-4', creatorAnswers[question.id] === false ? 'text-white' : 'text-neutral-300']"
                      />
                    </button>
                  </div>
                </div>
              </div>
            </template>
          </SortableList>
        </div>

        <!-- Publish Section -->
        <div class="relative">
          <!-- Desktop layout -->
          <div class="hidden sm:block bg-accent-green rounded-[999px] p-4 mb-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-6">
                <FancyInput
                  v-model="surveyCode"
                  :icon="'/assets/bookmark-icon.svg'"
                  :placeholder="'survey ID'"
                  :is-checking="isCheckingCode('survey')"
                  :is-valid="isCodeValid('survey')"
                  :is-error="isCodeInvalid('survey')"
                  :max-width="'300px'"
                  :border-width="2"
                  input-height="40px"
                  icon-size="24px"
                  font-size="text-sm"
                  @rotate="rotateCode('survey')"
                  @input="handleCodeInput('survey')"
                  :loader-color="'#BE185D'"
                  :valid-border-color="'#22C55E'"
                  :bg-color="'white'"
                  :text-color="'text-neutral-500'"
                  :error-bg-color="'#EF4444'"
                  :icon-color="'text-neutral-500'"
                  :min-width="'100px'"
                  v-tooltip="'A Shareable shortcode for the review'"
                />
                <FancyInput
                  v-model="userCode"
                  :icon="'/assets/user-icon.svg'"
                  :placeholder="'user name'"
                  :is-checking="isCheckingCode('user')"
                  :is-valid="isCodeValid('user')"
                  :is-error="isCodeInvalid('user')"
                  :border-width="2"
                  input-height="40px"
                  icon-size="24px"
                  font-size="text-sm"
                  @rotate="rotateCode('user')"
                  @input="handleCodeInput('user')"
                  :loader-color="'#BE185D'"
                  :valid-border-color="'#22C55E'"
                  :bg-color="'white'"
                  :text-color="'text-neutral-500'"
                  :error-bg-color="'#EF4444'"
                  :icon-color="'text-neutral-500'"
                  :min-width="'100px'"
                  v-tooltip="'A secret usercode for you to see results later'"
                />
              </div>
              <FancyButton
                label="Publish"
                :disabled="!canPublish"
                :is-actioning="isPublishing"
                @click="finishSurvey"
                :border-width="3"
                button-height="48px"
                icon-size="24px"
                font-size="text-xl"
                :min-width="'128px'"
                bg-color="black"
                border-color="black"
                disabled-bg-color="gray"
                disabled-border-color="gray"
                text-color="text-white"
                disabled-text-color="text-gray-400"
              />
            </div>
          </div>

          <!-- Mobile layout -->
          <div class="sm:hidden bg-accent-green rounded-[25px] p-4 mb-4">
            <div class="space-y-4">
              <div>
                <FancyInput
                  v-model="surveyCode"
                  :icon="'/assets/bookmark-icon.svg'"
                  :placeholder="'survey ID'"
                  :is-checking="isCheckingCode('survey')"
                  :is-valid="isCodeValid('survey')"
                  :is-error="isCodeInvalid('survey')"
                  :border-width="2"
                  input-height="40px"
                  icon-size="24px"
                  font-size="text-sm"
                  @rotate="rotateCode('survey')"
                  @input="handleCodeInput('survey')"
                  :loader-color="'#BE185D'"
                  :valid-border-color="'#22C55E'"
                  :bg-color="'white'"
                  :text-color="'text-neutral-500'"
                  :error-bg-color="'#EF4444'"
                  :icon-color="'text-neutral-500'"
                  class="w-full"
                  :min-width="'100%'"
                />
                <p class="text-xs text-primary mt-1 ml-2">A Shareable shortcode for the review</p>
              </div>
              <div>
                <FancyInput
                  v-model="userCode"
                  :icon="'/assets/user-icon.svg'"
                  :placeholder="'user name'"
                  :is-checking="isCheckingCode('user')"
                  :is-valid="isCodeValid('user')"
                  :is-error="isCodeInvalid('user')"
                  :border-width="2"
                  input-height="40px"
                  icon-size="24px"
                  font-size="text-sm"
                  @rotate="rotateCode('user')"
                  @input="handleCodeInput('user')"
                  :loader-color="'#BE185D'"
                  :valid-border-color="'#22C55E'"
                  :bg-color="'white'"
                  :text-color="'text-neutral-500'"
                  :error-bg-color="'#EF4444'"
                  :icon-color="'text-neutral-500'"
                  class="w-full"
                  :min-width="'100%'"
                />
                <p class="text-xs text-primary mt-1 ml-2">A secret usercode for you to see results later</p>
              </div>
            </div>
          </div>

          <!-- Error Notes Section -->
          <div class="mb-6">
            <div
              v-if="!allQuestionsAnswered || isCodeInvalid('survey') || isCodeInvalid('user')"
              class="flex flex-col space-y-2 text-accent"
            >
              <div v-if="!allQuestionsAnswered" class="flex items-center space-x-2">
                <inline-svg src="assets/info-icon.svg" class="text-accent w-5 h-5" />
                <span class="text-sm font-medium">Complete self review before publishing</span>
              </div>
              <div v-if="isCodeInvalid('survey')" class="flex items-center space-x-2">
                <inline-svg src="assets/info-icon.svg" class="text-accent w-5 h-5" />
                <span class="text-sm font-medium">{{ getCodeErrorMessage('survey') }}</span>
              </div>
              <div v-if="isCodeInvalid('user')" class="flex items-center space-x-2">
                <inline-svg src="assets/info-icon.svg" class="text-accent w-5 h-5" />
                <span class="text-sm font-medium">{{ getCodeErrorMessage('user') }}</span>
              </div>
            </div>
          </div>
        </div>
      </template>

      <!-- Published Section -->
      <LinkShareSection
        v-if="isPublished"
        :surveyCode="surveyCode"
        :resultsCode="userCode"
        :showSurveyLink="true"
        :showResultsLink="true"
        :surveyLinkLabel="'Review link'"
        :resultsLinkLabel="'Result link'"
        :surveyLinkDescription="'Share it with your friends for feedback'"
        :resultsLinkDescription="'Bookmark and come here later to see results'"
        :baseUrl="baseUrl"
        @copy-success="handleCopySuccess"
        @copy-error="handleCopyError"
      />
    </div>

    <!-- Mobile Publish Button - Moved outside the main content div -->
    <div class="sm:hidden fixed bottom-0 left-0 right-0 p-4 bg-white border-t border-gray-200 z-50">
      <FancyButton
        label="Publish"
        :disabled="!canPublish"
        :is-actioning="isPublishing"
        @click="finishSurvey"
        :border-width="3"
        button-height="48px"
        icon-size="24px"
        font-size="text-xl"
        bg-color="black"
        border-color="black"
        disabled-bg-color="gray"
        disabled-border-color="gray"
        text-color="text-white"
        disabled-text-color="text-gray-400"
        :full-width="true"
      />
    </div>

    <ToastView :message="toastMessage" :type="toastType" @hidden="clearToast" />
  </div>
</template>


<script>
import { ref, computed, watch, onMounted, reactive } from 'vue';
import { useI18n } from 'vue-i18n';
import api from '@/services/api';
import confetti from 'canvas-confetti';
import debounce from 'lodash/debounce';
import InlineSvg from 'vue-inline-svg';
import ToastView from '@/components/ToastView.vue';
import FancyInput from '@/components/FancyInput.vue';
import FancyButton from '@/components/FancyButton.vue';
import LinkShareSection from '@/components/ShareView.vue';
import TextAnimate from '@/components/ui/TextAnimate.vue';
import SortableList from '@/components/ui/SortableList.vue';

export default {
  name: 'CreateView',
  components: {
    InlineSvg,
    ToastView,
    FancyInput,
    FancyButton,
    LinkShareSection,
    TextAnimate,
    SortableList,
  },
  setup() {
    // Localization
    const { t } = useI18n();

    // State Management
    const surveyTitle = ref(t('createView.defaultTitle'));
    const surveyDescription = ref(t('createView.defaultDescription'));
    const newQuestion = ref({ text: '', response_type: 'scale', isAutogenerated: false });
    const questions = ref([]);
    const creatorAnswers = ref({});
    const isLoading = ref(false);
    const isSubmitted = ref(false);
    const isPublished = ref(false);
    const errorMessage = ref('');
    const showSuccess = ref(false);
    const surveyCode = ref('');
    const userCode = ref('');
    const surveyLink = ref('');
    const resultsLink = ref('');
    const availableCodes = ref({ survey: [], user: [] });
    const codeStatus = ref({ survey: null, user: null });
    const isChecking = reactive({ survey: false, user: false });
    const isPublishing = ref(false);
    const baseUrl = computed(() => process.env.VUE_APP_BASE_URL || '');
    const inputFocused = ref(false);
    const toastMessage = ref('');
    const toastType = ref('');
    const editingQuestionIndex = ref(null);
    const isReordering = ref(false);
    const showUserCodeTooltip = ref(false);
    const showSurveyCodeTooltip = ref(false);
    const placeholderText = ref('Enter your question here');

    // Placeholder Management
    const placeholders = [
      'Enter your question here',
      'How would you rate...?',
      'Do you think...?',
      'What\'s your opinion on...?',
    ];
    let placeholderIndex = 0;

    // Suggested Questions
    const suggestedQuestions = [
      { text: "How well do I communicate my ideas?", response_type: "scale" },
      { text: "Am I open to feedback from others?", response_type: "boolean" },
      { text: "How effectively do I manage my time?", response_type: "scale" },
      { text: "Do I actively listen to you and other colleagues?", response_type: "boolean" },
      { text: "How well do I handle stress and pressure?", response_type: "scale" },
      { text: "Am I proactive in solving problems?", response_type: "boolean" },
      { text: "How would I rate my leadership skills?", response_type: "scale" },
      { text: "Do I consistently meet deadlines?", response_type: "boolean" },
      { text: "How adaptable am I to change?", response_type: "scale" },
      { text: "Do I take responsibility for my mistakes?", response_type: "boolean" }
    ];

    // Easter Egg Logic
    let questionAddedTimes = [];
    let lastEasterEggTrigger = 0;
    const EASTER_EGG_COOLDOWN = 30000; // 30 seconds cooldown

    // Computed Properties
    const canPublish = computed(() => 
      allQuestionsAnswered.value &&
      isCodeValid('survey') &&
      isCodeValid('user') &&
      !isLoading.value &&
      !isSubmitted.value
    );

    const allQuestionsAnswered = computed(() =>
      questions.value.length > 0 &&
      questions.value.every(question => creatorAnswers.value[question.id] !== null && creatorAnswers.value[question.id] !== undefined)
    );

    // Methods
    const animatePlaceholder = () => {
      setInterval(() => {
        placeholderIndex = (placeholderIndex + 1) % placeholders.length;
        placeholderText.value = placeholders[placeholderIndex];
      }, 3000);
    };

    const isCheckingCode = (type) => isChecking[type];

    const isValidFormat = (code) => /^[a-zA-Z0-9-]{5,}$/.test(code);

    const getCodeErrorMessage = (type) => {
      const code = type === 'survey' ? surveyCode.value : userCode.value;
      const otherCode = type === 'survey' ? userCode.value : surveyCode.value;

      if (!code || code.length < 5) {
        return `${type === 'survey' ? 'Survey' : 'User'} code must be at least 5 characters long.`;
      }

      if (!isValidFormat(code)) {
        return `${type === 'survey' ? 'Survey' : 'User'} code can only contain letters, numbers, and hyphens.`;
      }

      if (code === otherCode) {
        return `${type === 'survey' ? 'Survey' : 'User'} code cannot be the same as the ${type === 'survey' ? 'user' : 'survey'} code.`;
      }

      return `Invalid ${type === 'survey' ? 'survey' : 'user'} code. Please choose a different one.`;
    };

    const isCodeValid = (type) => {
      const code = type === 'survey' ? surveyCode.value : userCode.value;
      const otherCode = type === 'survey' ? userCode.value : surveyCode.value;
      return !isChecking[type] && isValidFormat(code) && codeStatus.value[type] === 'valid' && code !== otherCode;
    };

    const isCodeInvalid = (type) => {
      const code = type === 'survey' ? surveyCode.value : userCode.value;
      const otherCode = type === 'survey' ? userCode.value : surveyCode.value;
      return !isChecking[type] && (!isValidFormat(code) || codeStatus.value[type] === 'invalid' || code === otherCode);
    };

    const handleCodeInput = debounce((type) => {
      const code = type === 'survey' ? surveyCode.value : userCode.value;
      const otherCode = type === 'survey' ? userCode.value : surveyCode.value;
      const fetchedIdsForType = availableCodes.value[type];

      if (isValidFormat(code)) {
        if (code === otherCode) {
          codeStatus.value[type] = 'invalid';
          isChecking[type] = false;
        } else if (fetchedIdsForType.includes(code)) {
          codeStatus.value[type] = 'valid';
          isChecking[type] = false;
        } else {
          codeStatus.value[type] = null;
          isChecking[type] = true;
          checkCodeAvailability(type);
        }
      } else {
        codeStatus.value[type] = 'invalid';
        isChecking[type] = false;
      }
    }, 300);

    const debounceCheckCode = debounce((type) => {
      const code = type === 'survey' ? surveyCode.value : userCode.value;
      if (isValidFormat(code)) {
        checkCodeAvailability(type);
      } else {
        isChecking[type] = false;
      }
    }, 750);

    const setQuestionType = (type) => {
      newQuestion.value.response_type = type;
      newQuestion.value.isAutogenerated = false;
    };

    const handleAddOrSuggest = () => {
      if (newQuestion.value.text.trim()) {
        addQuestion();
      } else {
        suggestQuestion();
      }
    };

    const addQuestion = () => {
      if (newQuestion.value.text.trim() && !isSubmitted.value) {
        const newQuestionObject = {
          id: newQuestion.value.id || Date.now(),
          text: newQuestion.value.text,
          response_type: newQuestion.value.response_type,
          isAutogenerated: newQuestion.value.isAutogenerated,
        };

        if (editingQuestionIndex.value !== null) {
          questions.value.splice(editingQuestionIndex.value, 0, newQuestionObject);
          updateQuestionIndexes();
          if (newQuestion.value.preservedAnswer !== undefined) {
            creatorAnswers.value[newQuestionObject.id] = newQuestion.value.preservedAnswer;
          } else {
            creatorAnswers.value[newQuestionObject.id] = null;
          }
          editingQuestionIndex.value = null;
        } else {
          questions.value.push(newQuestionObject);
          updateQuestionIndexes();
          creatorAnswers.value[newQuestionObject.id] = null;
        }

        newQuestion.value = { text: '', response_type: 'scale', isAutogenerated: false };
        checkEasterEgg();
      }
    };

    const suggestQuestion = () => {
      const randomIndex = Math.floor(Math.random() * suggestedQuestions.length);
      const suggestedQuestion = suggestedQuestions[randomIndex];
      newQuestion.value = {
        text: suggestedQuestion.text,
        response_type: suggestedQuestion.response_type,
        isAutogenerated: true,
      };
    };

    const handleQuestionReorder = (newOrder) => {
      isReordering.value = true;
      questions.value = newOrder.map((question, index) => ({ ...question, index }));
      setTimeout(() => {
        isReordering.value = false;
      }, 100);
    };

    const handleQuestionChange = () => {
      if (newQuestion.value.isAutogenerated && newQuestion.value.text !== suggestedQuestions.find(q => q.text === newQuestion.value.text)?.text) {
        newQuestion.value.isAutogenerated = false;
      }
    };

    const suggestReplacementQuestion = () => suggestQuestion();

    const selectAnswer = (qId, value) => {
      if (!isSubmitted.value) {
        creatorAnswers.value[qId] = value;
      }
    };

    const celebrateSuccess = () => {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 },
      });
    };

    const clearToast = () => {
      toastMessage.value = '';
      toastType.value = '';
    };

    const openAndCopy = (type) => {
      const url = type === 'survey' ? surveyLink.value : resultsLink.value;
      window.open(url, '_blank');
      copyToClipboard(type);
    };

    const copyToClipboard = (type) => {
      const textToCopy = type === 'survey' ? surveyLink.value : resultsLink.value;
      navigator.clipboard.writeText(textToCopy).then(() => {
        toastMessage.value = t('createView.copySuccess');
        toastType.value = 'success';
      }, (err) => {
        console.error('Could not copy text: ', err);
        toastMessage.value = t('createView.copyError');
        toastType.value = 'error';
      });
    };

    const checkEasterEgg = () => {
      const now = Date.now();
      questionAddedTimes.push(now);

      if (questionAddedTimes.length > 5) {
        questionAddedTimes = questionAddedTimes.slice(-5);
      }

      if (questionAddedTimes.length === 5 && (now - questionAddedTimes[0]) < 10000) {
        if (now - lastEasterEggTrigger > EASTER_EGG_COOLDOWN) {
          triggerEasterEgg();
          lastEasterEggTrigger = now;
          questionAddedTimes = [];
        }
      }
    };

    const triggerEasterEgg = () => {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C1'],
      });
    };

    const updateQuestionIndexes = () => {
      questions.value = questions.value.map((q, i) => ({
        ...q,
        index: i,
      }));
    };

    const editQuestion = (index) => {
      const questionToEdit = questions.value[index];
      if (!questionToEdit) {
        console.error('Question not found at index:', index);
        return;
      }

      newQuestion.value = {
        text: questionToEdit.text,
        response_type: questionToEdit.response_type,
        isAutogenerated: questionToEdit.isAutogenerated,
        id: questionToEdit.id,
      };
      editingQuestionIndex.value = index;

      questions.value.splice(index, 1);
      const { [questionToEdit.id]: removedAnswer, ...remainingAnswers } = creatorAnswers.value;
      creatorAnswers.value = remainingAnswers;

      if (removedAnswer !== undefined) {
        newQuestion.value.preservedAnswer = removedAnswer;
      }
    };

    async function fetchInitialCodes() {
      isChecking.survey = true;
      isChecking.user = true;
      try {
        const response = await api.getIds(10);
        availableCodes.value.survey = response.data.ids.slice(0, 5);
        availableCodes.value.user = response.data.ids.slice(5);
        surveyCode.value = availableCodes.value.survey[0];
        userCode.value = availableCodes.value.user[0];
        codeStatus.value.survey = 'valid';
        codeStatus.value.user = 'valid';
      } catch (error) {
        toastMessage.value = t('createView.errorFetchingCodes');
        toastType.value = 'error';
        codeStatus.value.survey = 'invalid';
        codeStatus.value.user = 'invalid';
      } finally {
        setTimeout(() => {
          isChecking.survey = false;
          isChecking.user = false;
        }, 1000);
      }
    }

    const rotateCode = (type) => {
      const codes = availableCodes.value[type];
      const currentCode = type === 'survey' ? surveyCode.value : userCode.value;
      const currentIndex = codes.indexOf(currentCode);
      const nextIndex = (currentIndex + 1) % codes.length;
      if (type === 'survey') {
        surveyCode.value = codes[nextIndex];
      } else {
        userCode.value = codes[nextIndex];
      }
      codeStatus.value[type] = 'valid';
    };

    async function checkCodeAvailability(type) {
      const code = type === 'survey' ? surveyCode.value : userCode.value;
      isChecking[type] = true;
      codeStatus.value[type] = null;

      try {
        const response = await api.checkIdAvailability(code);
        await new Promise(resolve => setTimeout(resolve, 1000));

        if (!response.data || typeof response.data.available !== 'boolean') {
          throw new Error('Unexpected API response format');
        }

        codeStatus.value[type] = response.data.available ? 'valid' : 'invalid';
        if (!response.data.available) {
          toastMessage.value = t('createView.codeNotAvailable');
          toastType.value = 'error';
        }
      } catch (error) {
        codeStatus.value[type] = 'invalid';
        toastMessage.value = t('createView.errorCheckingCode');
        toastType.value = 'error';
      } finally {
        isChecking[type] = false;
      }
    }

    async function finishSurvey() {
      if (isSubmitted.value || !allQuestionsAnswered.value) return;

      isPublishing.value = true;
      isLoading.value = true;
      errorMessage.value = '';
      try {
        const surveyData = {
          survey_id: surveyCode.value,
          user_code: userCode.value,
          title: surveyTitle.value,
          description: surveyDescription.value,
          questions: questions.value.map((q) => ({
            ...q,
            creator_answer: creatorAnswers.value[q.id],
          })),
        };

        const response = await api.createSurvey(surveyData);  // If response is not used, you can comment or remove this line.
        console.log("Survey created: "+response);
        surveyLink.value = `${baseUrl.value}/${surveyCode.value}`;
        resultsLink.value = `${baseUrl.value}/u/${userCode.value}`;
        isSubmitted.value = true;
        isPublished.value = true;
        showSuccess.value = true;
        celebrateSuccess();
        toastMessage.value = t('createView.toastSuccess');
        toastType.value = 'success';
      } catch (error) {
        errorMessage.value = t('createView.toastError');
        toastMessage.value = t('createView.toastError');
        toastType.value = 'error';
      } finally {
        isLoading.value = false;
        isPublishing.value = false;
      }
    }

    const showSequentialTooltips = () => {
      if (questions.value.length === 1) {
        showUserCodeTooltip.value = true;
        setTimeout(() => {
          showUserCodeTooltip.value = false;
          setTimeout(() => {
            showSurveyCodeTooltip.value = true;
            setTimeout(() => {
              showSurveyCodeTooltip.value = false;
            }, 5000);
          }, 500);
        }, 5000);
      }
    };

    // Lifecycle Hooks
    onMounted(async () => {
      await fetchInitialCodes();
      animatePlaceholder();
    });

    watch(() => newQuestion.value.text, handleQuestionChange);

    watch(() => questions.value.length, (newLength, oldLength) => {
      if (newLength === 1 && oldLength === 0) {
        showSequentialTooltips();
      }
    });

    return {
      t,
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
      toastMessage,
      toastType,
      setQuestionType,
      suggestReplacementQuestion,
      suggestQuestion,
      addQuestion,
      handleAddOrSuggest,
      selectAnswer,
      finishSurvey,
      clearToast,
      userCode,
      resultsLink,
      rotateCode,
      checkCodeAvailability,
      openAndCopy,
      copyToClipboard,
      isCheckingCode,
      isCodeValid,
      isCodeInvalid,
      debounceCheckCode,
      canPublish,
      isValidFormat,
      handleCodeInput,
      getCodeErrorMessage,
      isPublishing,
      placeholderText,
      showUserCodeTooltip,
      showSurveyCodeTooltip,
      editQuestion,
      baseUrl,
      handleQuestionReorder,
      editingQuestionIndex,
      isReordering,
    };
  },
};
</script>



<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;700&display=swap');

/* General Styles */
body {
  font-family: 'IBM Plex Sans', sans-serif;
}

textarea {
  resize: none !important;
}

.pb-24 {
  padding-bottom: 6rem;
}

.fixed {
  z-index: 50;
}

.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Animation Keyframes */
@keyframes blink {
  0%, 100% { opacity: 0; }
  50% { opacity: 1; }
}

/* Animations */
.animate-blink {
  animation: blink 1s infinite;
}

/* Transition Styles */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

.duration-300 {
  transition-duration: 300ms;
}

.ease-in-out {
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Scale Transitions */
.transform {
  transform: translateX(var(--tw-translate-x)) translateY(var(--tw-translate-y)) rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y));
}

.hover\:scale-102:hover {
  --tw-scale-x: 1.02;
  --tw-scale-y: 1.02;
  transform: var(--tw-transform);
}

.focus\:scale-102:focus {
  --tw-scale-x: 1.02;
  --tw-scale-y: 1.02;
  transform: var(--tw-transform);
}

/* Fade and Scale Transitions */
.fade-scale-enter-active,
.fade-scale-leave-active,
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

/* List Transition Styles */
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.list-move {
  transition: transform 0.5s ease;
}

/* Tooltip Styles */
.v-tooltip {
  display: block;
  z-index: 10000;
}

.v-tooltip .tooltip-inner {
  background: #1F2937;
  color: white;
  border-radius: 16px;
  padding: 5px 10px 4px;
}

.v-tooltip .tooltip-arrow {
  width: 0;
  height: 0;
  border-style: solid;
  position: absolute;
  margin: 5px;
  border-color: #1F2937;
}

/* Tooltip Arrow Positions */
.v-tooltip[x-placement^="top"] .tooltip-arrow {
  border-width: 5px 5px 0 5px;
  border-left-color: transparent !important;
  border-right-color: transparent !important;
  border-bottom-color: transparent !important;
  bottom: -5px;
  left: calc(50% - 5px);
  margin-top: 0;
  margin-bottom: 0;
}

/* Add styles for other placements if needed */

/* Code Input Container */
.code-input-container {
  position: relative;
}

.code-input-container .measure-span {
  visibility: hidden;
  white-space: pre;
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1;
}

/* Add these new styles */
input[type="text"], textarea {
  transition: all 0.3s ease;
}

input[type="text"]:focus, textarea:focus {
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
}

/* Specific styles for title and description */
input[v-model="surveyTitle"] {
  height: 40px;
}

input[v-model="surveyDescription"] {
  height: 30px;
}
</style>