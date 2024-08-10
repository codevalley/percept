<template>
    <div class="bg-accent-green rounded-[25px] p-4 sm:p-7 mb-6 sm:mb-8">
      <div class="flex flex-col space-y-6 sm:space-y-8">
        <div v-if="showSurveyLink" class="flex flex-col space-y-1">
          <div class="flex flex-col sm:flex-row sm:items-center space-y-2 sm:space-y-0 sm:space-x-4">
            <span class="text-primary text-base sm:text-lg font-normal leading-7">{{ surveyLinkLabel }}</span>
            <button
              @click="openAndCopy('survey')"
              class="h-10 bg-white text-primary rounded-full flex items-center justify-between px-4 border border-primary w-full sm:w-auto"
            >
              <span class="text-base font-medium truncate mr-2">{{ surveyCode }}</span>
              <inline-svg 
                @click.stop="copyToClipboard('surveyCode')" 
                src="/assets/copy-icon.svg"
                class="w-5 h-5 flex-shrink-0"
              />
            </button>
          </div>
          <span class="text-primary text-sm italic sm:ml-4">{{ surveyLinkDescription }}</span>
        </div>
  
        <div class="flex flex-col space-y-1">
          <div class="flex flex-col sm:flex-row sm:items-center space-y-2 sm:space-y-0 sm:space-x-4">
            <span class="text-primary text-base sm:text-lg font-normal leading-7">{{ userLinkLabel }}</span>
            <button
              @click="openAndCopy('user')"
              class="h-10 bg-white text-primary rounded-full flex items-center justify-between px-4 border border-primary w-full sm:w-auto"
            >
              <span class="text-base font-medium truncate mr-2">{{ userCode }}</span>
              <inline-svg 
                @click.stop="copyToClipboard('userCode')" 
                src="/assets/copy-icon.svg" 
                class="w-5 h-5 flex-shrink-0" 
              />
            </button>
          </div>
          <span class="text-primary text-sm italic sm:ml-4">{{ userLinkDescription }}</span>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { computed } from 'vue';
  import InlineSvg from 'vue-inline-svg';
  
  export default {
    name: 'LinkShareSection',
    components: {
      InlineSvg,
    },
    props: {
      surveyCode: {
        type: String,
        required: true,
      },
      userCode: {
        type: String,
        required: true,
      },
      isCreator: {
        type: Boolean,
        default: false,
      },
      showSurveyLink: {
        type: Boolean,
        default: true,
      },
    },
    setup(props, { emit }) {
      const baseUrl = computed(() => process.env.VUE_APP_BASE_URL || '');
      const surveyLink = computed(() => `${baseUrl.value}/${props.surveyCode}`);
      const resultsLink = computed(() => `${baseUrl.value}/u/${props.userCode}`);
  
      const surveyLinkLabel = computed(() => props.isCreator ? "Review link" : "This is your review link");
      const userLinkLabel = computed(() => props.isCreator ? "Result link" : "Your results code");
      const surveyLinkDescription = computed(() => "Share it with your friends for feedback");
      const userLinkDescription = computed(() => props.isCreator 
        ? "Bookmark and come here later to see results" 
        : "Use this code to access your results in the future");
  
      const openAndCopy = (type) => {
        const url = type === 'survey' ? surveyLink.value : resultsLink.value;
        window.open(url, '_blank');
        copyToClipboard(type === 'survey' ? 'surveyCode' : 'userCode');
      };
  
      const copyToClipboard = (type) => {
        let textToCopy = type === 'surveyCode' ? surveyLink.value : resultsLink.value;
        navigator.clipboard.writeText(textToCopy).then(() => {
          emit('copy-success');
        }, () => {
          emit('copy-error');
        });
      };
  
      return {
        surveyLinkLabel,
        userLinkLabel,
        surveyLinkDescription,
        userLinkDescription,
        openAndCopy,
        copyToClipboard,
      };
    },
  }
  </script>