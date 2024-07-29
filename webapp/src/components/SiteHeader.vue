<template>
  <header class="font-sans mb-8 sm:mb-16">
    <div class="max-w-[859px] mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16 sm:h-20">
        <div class="flex items-center cursor-pointer" @click="navigateTo('/')">
          <img src="/assets/backwave.svg" alt="Backwave logo" class="w-10 h-10 sm:w-16 sm:h-16" />
          <h1 class="text-xl sm:text-3xl md:text-5xl font-bold ml-2 text-primary self-start mt-1">{{ $t('header.title') }}</h1>
        </div>
        <nav class="hidden sm:flex items-center space-x-4 sm:space-x-8">
          <NavItem 
            v-for="item in navItems" 
            :key="item.name" 
            :item="item" 
            :isActive="item.name === activeTab"
            @click="handleNavItemClick(item.name)"
          />
        </nav>
        <button @click="toggleMobileMenu" class="sm:hidden">
          <inline-svg src="/assets/menu-icon.svg" class="w-6 h-6 text-primary" />
        </button>
      </div>
      
      <!-- Mobile menu -->
      <div v-if="isMobileMenuOpen" class="sm:hidden mt-4">
        <nav class="flex flex-col space-y-4">
          <NavItem 
            v-for="item in navItems" 
            :key="item.name" 
            :item="item" 
            :isActive="item.name === activeTab"
            @click="handleNavItemClick(item.name)"
          />
        </nav>
      </div>

      <div v-if="(activeTab === 'participate' && route.name !== 'TakeSurvey') || (activeTab === 'analyze' && route.name !== 'Results')" class="mt-4">
        <div class="flex flex-col bg-neutral-100 rounded-3xl sm:rounded-full w-full sm:w-[420px]">
          <div class="flex items-center w-full p-2 sm:p-0 sm:pl-4">
            <img :src="activeTab === 'participate' ? '/assets/hash-icon.svg' : '/assets/analyze-icon.svg'" :alt="activeTab" class="w-8 h-8 mr-2" />
            <input
              v-if="activeTab === 'participate'"
              v-model="participateCode"
              type="text"
              :placeholder="$t('header.participatePlaceholder')"
              class="bg-transparent text-lg font-regular text-neutral-400 w-full flex-grow focus:outline-none"
            />
            <input
              v-else
              v-model="creatorCode"
              type="text"
              :placeholder="$t('header.analyzePlaceholder')"
              class="bg-transparent text-lg font-regular text-neutral-400 w-full flex-grow focus:outline-none"
            />
          </div>
          <div class="px-2 pb-2 sm:pr-1 sm:pb-1">
            <button
              @click="activeTab === 'participate' ? submitParticipateCode() : handleAnalyze()"
              :disabled="isLoading"
              class="bg-primary text-white text-lg font-bold px-6 py-2 rounded-full w-full"
            >
              <span v-if="!isLoading">{{ $t(activeTab === 'participate' ? 'header.participateButton' : 'header.analyzeButton') }}</span>
              <span v-else class="inline-block animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></span>
            </button>
          </div>
        </div>
      </div>
      
      <ToastView :message="toastMessage" :type="toastType" @hidden="clearToast" />
    </div>
  </header>
</template>

<script>
import { ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import InlineSvg from 'vue-inline-svg';
import api from '@/services/api';
import ToastView from '@/components/ToastView.vue';
import NavItem from '@/components/NavItem.vue';

export default {
  name: 'SiteHeader',
  components: {
    InlineSvg,
    ToastView,
    NavItem,
  },
  setup() {
    const { t } = useI18n();
    const router = useRouter();
    const route = useRoute();
    const activeTab = ref(null);
    const participateCode = ref('');
    const creatorCode = ref('');
    const isLoading = ref(false);
    const errorMessage = ref('');
    const toastMessage = ref('');
    const toastType = ref('');
    const isMobileMenuOpen = ref(false);

    const navItems = [
      { name: 'participate', icon: '/assets/hash-icon.svg', label: t('header.participate') },
      { name: 'create', icon: '/assets/yes-icon.svg', label: t('header.create') },
      { name: 'analyze', icon: '/assets/analyze-icon.svg', label: t('header.analyze') },
    ];

    const navigateTo = (path) => {
      router.push(path);
      activeTab.value = null;
      isMobileMenuOpen.value = false;
    };

    const handleNavItemClick = (tabName) => {
      if (tabName === 'create') {
        navigateTo('/create');
      } else {
        activeTab.value = activeTab.value === tabName ? null : tabName;
      }
      isMobileMenuOpen.value = false;
    };

    const toggleMobileMenu = () => {
      isMobileMenuOpen.value = !isMobileMenuOpen.value;
    };

    function clearToast() {
      toastMessage.value = '';
      toastType.value = '';
    }

    const submitParticipateCode = async () => {
      if (!participateCode.value.trim()) {
        toastMessage.value = t('header.emptyCodeError');
        toastType.value = 'error';
        return;
      }

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
        errorMessage.value = t('header.errorLoadingSurvey');
      } finally {
        isLoading.value = false;
      }
    };

    const handleAnalyze = async () => {
      if (!creatorCode.value.trim()) {
        toastMessage.value = t('header.emptyCodeError');
        toastType.value = 'error';
        return;
      }

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
        errorMessage.value = t('header.errorLoadingResults');
      } finally {
        isLoading.value = false;
      }
    };

    // Watch for route changes to update activeTab
    watch(() => route.name, (newRouteName) => {
      if (newRouteName === 'Create') {
        activeTab.value = 'create';
      } else if (newRouteName === 'TakeSurvey') {
        activeTab.value = 'participate';
      } else if (newRouteName === 'Results') {
        activeTab.value = 'analyze';
      } else {
        activeTab.value = null;
      }
    }, { immediate: true });

    return {
      activeTab,
      participateCode,
      creatorCode,
      isLoading,
      errorMessage,
      navigateTo,
      handleNavItemClick,
      submitParticipateCode,
      handleAnalyze,
      clearToast,
      toastMessage,
      toastType,
      isMobileMenuOpen,
      toggleMobileMenu,
      navItems,
      route, // Add route to the returned object
    };
  },
};
</script>