<template>
  <div class="font-sans min-h-screen bg-white">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Hero section -->
      <div class="mt-8 p-6 sm:p-8 bg-neutral-100 rounded-3xl min-h-[320px] sm:min-h-[420px] flex flex-col justify-end">
        <inline-svg src="/assets/high-five.svg" class="text-neutral-700 w-20 h-20 sm:w-24 sm:h-24 mx-auto mb-4 sm:mb-6" />
        
        <div class="text-center"> <!-- Centering container -->
          <TextAnimate 
            :text="$t('homeView.title')" 
            type="popIn"
            :delay="0.3"
            :duration="0.75"
            class="text-3xl sm:text-4xl font-bold text-primary mb-1"
          />

        </div>
        <TypeWriter 
          :texts="subtitleTexts" 
          class="text-lg sm:text-xl text-center text-primary mb-6 sm:mb-8"
        />
        <div class="flex justify-center">
          <router-link to="/new" class="bg-accent-green text-primary text-lg sm:text-xl font-bold px-6 sm:px-8 py-2 rounded-full">
            {{ $t('homeView.createButton') }}
          </router-link>
        </div>
      </div>

      <!-- Statistics section -->
      <div class="mt-12 flex justify-around">
        <div class="text-center">
          <AnimatedNumber :value="totalSurveys" class="text-2xl font-bold text-primary" />
          <p class="text-sm text-neutral-500">Total Surveys</p>
        </div>
        <div class="text-center">
          <AnimatedNumber :value="totalParticipants" class="text-2xl font-bold text-primary" />
          <p class="text-sm text-neutral-500">Total Participants</p>
        </div>
      </div>

      <!-- Participate section - Only visible on desktop -->
      <div class="hidden sm:block mt-12">
        <TextAnimate 
          :text="$t('homeView.participateTitle')"
          type="fadeInUp"
          :delay="0.5"
          class="text-xl font-semibold text-primary text-left mb-2"
        />
        <p class="text-lg text-primary mb-3 text-left">
          {{ $t('homeView.participateSubtitle') }}
        </p>
        <div class="flex items-center bg-neutral-100 rounded-full w-[420px]">
          <img src="/assets/question-icon.svg" alt="Question" class="w-10 h-10 ml-4 mr-2" />
          <input
            v-model="participateCode"
            type="text"
            :placeholder="$t('homeView.participatePlaceholder')"
            class="bg-transparent text-xl font-regular text-neutral-400 flex-grow px-2 py-2 focus:outline-none"
          />
          <button
            @click="submitParticipateCode"
            :disabled="isLoading"
            class="bg-primary text-accent-green text-xl font-bold px-8 py-2 rounded-full"
          >
            <span v-if="!isLoading">{{ $t('homeView.participateButton') }}</span>
            <span v-else class="inline-block animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-accent-green"></span>
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
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import InlineSvg from 'vue-inline-svg';
import TextAnimate from '@/components/ui/TextAnimate.vue';
import TypeWriter from '@/components/ui/TypeWriter.vue';
import AnimatedNumber from '@/components/ui/AnimatedNumber.vue';

export default {
  name: 'HomeView',
  components: {
    InlineSvg,
    TextAnimate,
    TypeWriter,
    AnimatedNumber,
  },
  setup() {
    const { t } = useI18n();
    const router = useRouter();
    const participateCode = ref('');
    const isLoading = ref(false);
    const errorMessage = ref('');
    const totalSurveys = ref(23);  // Fallback number
    const totalParticipants = ref(313);  // Fallback number

    const subtitleTexts = [
      "Compare what you think about yourself...",
      "...with how others perceive you.",
      "Gain insights into your self-awareness.",
      "Improve your understanding of yourself.",
    ];

    const submitParticipateCode = async () => {
      isLoading.value = true;
      errorMessage.value = '';
      try {
        const response = await api.getSurvey(participateCode.value);
        if (response.data && response.data.questions) {
          console.log('Navigating to TakeSurvey');
          await router.push({
            name: 'TakeSurvey',
            params: { surveyId: participateCode.value },
            props: { surveyData: response.data }
          });
          console.log('Navigation completed');
        } else {
          throw new Error('Invalid survey data received');
        }
      } catch (error) {
        console.error('Error fetching survey:', error);
        errorMessage.value = t('homeView.errorMessage');
      } finally {
        isLoading.value = false;
      }
    };

    return {
      participateCode,
      isLoading,
      errorMessage,
      submitParticipateCode,
      subtitleTexts,
      totalSurveys,
      totalParticipants,
    };
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;700&display=swap');
</style>