<template>
  <header class="max-w-[859px] mx-auto relative font-['IBM_Plex_Sans'] mb-16">
    <div class="max-w-6xl mx-auto px-4 flex flex-col">
      <div class="flex items-center justify-between h-20">
        <div class="flex items-center cursor-pointer" @click="navigateTo('/')">
          <img src="/assets/backwave.svg" alt="Backwave logo" class="w-16 h-16" />
          <h1 class="text-5xl font-bold ml-2 text-black self-start mt-1">Backwave</h1>
        </div>

        <nav class="flex items-center space-x-8">
          <div
            @click="toggleTab('participate')"
            class="flex items-center relative cursor-pointer"
            :class="{ 'text-zinc-900': currentTab === 'participate', 'text-green-800': currentTab !== 'participate' }"
          >
            <inline-svg src="/assets/hash-icon.svg" class="w-7 h-7 mr-2" />
            <span class="text-xl font-bold leading-9">Participate</span>
            <div v-if="currentTab === 'participate'" class="w-full h-0.5 bg-black absolute bottom-[-4px] left-0"></div>
          </div>
          <div
            @click="navigateTo('/create')"
            class="flex items-center relative cursor-pointer"
            :class="{ 'text-zinc-900': currentTab === 'create', 'text-green-800': currentTab !== 'create' }"
          >
            <inline-svg src="/assets/yes-icon.svg" class="w-7 h-7 mr-2" />
            <span class="text-xl font-bold leading-9">Create</span>
            <div v-if="currentTab === 'create'" class="w-full h-0.5 bg-black absolute bottom-[-4px] left-0"></div>
          </div>
          <div
            @click="toggleTab('analyze')"
            class="flex items-center relative cursor-pointer"
            :class="{ 'text-zinc-900': currentTab === 'analyze', 'text-green-800': currentTab !== 'analyze' }"
          >
            <inline-svg src="/assets/analyze-icon.svg" class="w-7 h-7 mr-2" />
            <span class="text-xl font-bold leading-9">Analyze</span>
            <div v-if="currentTab === 'analyze'" class="w-full h-0.5 bg-black absolute bottom-[-4px] left-0"></div>
          </div>
        </nav>
      
      </div>
      
      <div v-if="activeTab === 'participate'" class="mt-4 flex items-center bg-gray-100 rounded-full w-[420px]">
        <img src="/assets/hash-icon.svg" alt="Question" class="w-10 h-10 ml-4 mr-2" />
        <input
          v-model="participateCode"
          type="text"
          placeholder="Enter review code"
          class="bg-transparent text-xl font-regular text-zinc-400 flex-grow px-2 py-2 focus:outline-none"
        />
        <button
          @click="submitParticipateCode"
          :disabled="isLoading"
          class="bg-zinc-700 text-gray-100 text-xl font-bold px-8 py-2 rounded-full"
        >
          <span v-if="!isLoading">Participate</span>
          <span v-else class="inline-block animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></span>
        </button>
      </div>

      <div v-if="activeTab === 'analyze'" class="mt-4 flex items-center bg-gray-100 rounded-full w-[420px]">
        <img src="/assets/analyze-icon.svg" alt="Analyze" class="w-10 h-10 ml-4 mr-2" />
        <input
          v-model="creatorCode"
          type="text"
          placeholder="Enter creator code"
          class="bg-transparent text-xl font-regular text-zinc-400 flex-grow px-2 py-2 focus:outline-none"
        />
        <button
          @click="handleAnalyze"
          :disabled="isLoading"
          class="bg-green-800 text-white text-xl font-bold px-8 py-2 rounded-full"
        >
          <span v-if="!isLoading">Analyze</span>
          <span v-else class="inline-block animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></span>
        </button>
      </div>
    </div>
  </header>
</template>

<script>
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import InlineSvg from 'vue-inline-svg';
import api from '@/services/api';

export default {
  name: 'SiteHeader',
  components: {
    InlineSvg,
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const activeTab = ref(null);
    const participateCode = ref('');
    const creatorCode = ref('');
    const isLoading = ref(false);
    const errorMessage = ref('');

    const currentTab = computed(() => {
      if (route.name === 'Results') return 'analyze';
      if (route.name === 'TakeSurvey') return 'participate';
      if (route.name === 'Create') return 'create';
      return null;
    });

    const navigateTo = (path) => {
      router.push(path);
      activeTab.value = null;
    };

    const toggleTab = (tab) => {
      activeTab.value = activeTab.value === tab ? null : tab;
    };

    const submitParticipateCode = async () => {
      isLoading.value = true;
      errorMessage.value = '';
      try {
        const response = await api.getSurvey(participateCode.value);
        if (response.data && response.data.questions) {
          router.push({ 
            name: 'TakeSurvey', 
            params: { surveyId: participateCode.value },
            props: { surveyData: response.data }
          });
          activeTab.value = null;
        } else {
          throw new Error('Invalid survey data received');
        }
      } catch (error) {
        console.error('Error fetching survey:', error);
        errorMessage.value = 'Failed to load survey. Please check the code and try again.';
      } finally {
        isLoading.value = false;
      }
    };

    const handleAnalyze = async () => {
      isLoading.value = true;
      errorMessage.value = '';
      try {
        const response = await api.getSurveyResultsByUserCode(creatorCode.value);
        if (response.data) {
          router.push({ 
            name: 'Results', 
            params: { userCode: creatorCode.value },
            query: { fromAnalyze: 'true' }
          });
          activeTab.value = null;
        } else {
          throw new Error('Invalid results data received');
        }
      } catch (error) {
        console.error('Error fetching results:', error);
        errorMessage.value = 'Failed to load results. Please check the creator code and try again.';
      } finally {
        isLoading.value = false;
      }
    };

    return {
      activeTab,
      currentTab,
      participateCode,
      creatorCode,
      isLoading,
      errorMessage,
      navigateTo,
      toggleTab,
      submitParticipateCode,
      handleAnalyze,
      route,
    };
  },
};
</script>