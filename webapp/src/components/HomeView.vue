<template>
  <div class="font-sans min-h-screen bg-white">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Hero section -->
      <div class="mt-8 p-6 sm:p-8 bg-neutral-100 rounded-3xl min-h-[320px] sm:min-h-[420px] flex flex-col justify-end">
        <inline-svg src="/assets/high-five.svg" class="text-neutral-700 w-20 h-20 sm:w-24 sm:h-24 mx-auto mb-4 sm:mb-6" />
        <TextAnimate 
          :text="$t('homeView.title')" 
          class="text-3xl sm:text-4xl font-bold text-center text-primary mb-1"
        />
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

      <!-- Rest of the component remains the same -->
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
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
    // const { t } = useI18n();
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
      // ... (rest of the function remains the same)
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