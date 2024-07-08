<template>
  <div class="font-['IBM_Plex_Sans'] max-w-3xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-primary mb-6">Survey Results</h1>
    <div v-if="loading" class="text-lg text-primary">Loading results...</div>
    <div v-else-if="error" class="text-lg text-accent">{{ error }}</div>
    <div v-else-if="results">
      <!-- Incomplete Results Section -->
      <div v-if="results.status === 'incomplete'" class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4">
        <p class="font-bold">Results Not Available Yet</p>
        <template v-if="results.is_creator">
          <p>More responses are needed before results are available.</p>
          <p>Current responses: {{ results.current_responses }}</p>
          <p>Minimum responses needed: {{ results.minimum_responses }}</p>
          <p>Remaining responses: {{ results.remaining_responses }}</p>
        </template>
        <template v-else>
          <p>The survey hasn't received enough responses yet. Please check back later.</p>
        </template>
      </div>

      <!-- Complete Results Section -->
      <template v-else>
        <!-- New section for links and codes -->
        <div class="bg-accent-green rounded-[25px] p-7 mb-8">
          <div class="w-full text-primary text-2xl font-bold leading-9 mb-6 text-left">
            {{ results.user_type === 'creator' ? 'Your Survey Information' : 'Your Results Information' }}
          </div>

          <div v-if="results.user_type === 'creator'" class="flex flex-col space-y-4">
            <div class="flex items-center justify-start space-x-4">
              <div class="flex items-center space-x-4">
                <span class="text-primary text-lg font-normal leading-7 whitespace-nowrap">Review code</span>
                <button
                  class="h-10 bg-white text-primary rounded-full flex items-center justify-between px-4 border border-primary"
                  @click="copyToClipboard(surveyId)">
                  <span class="text-base font-medium mr-2">{{ surveyId }}</span>
                  <inline-svg src="assets/copy-icon.svg" class="w-5 h-5 text-primary" />
                </button>
              </div>

              <div class="flex items-center space-x-4">
                <span class="text-primary text-lg font-normal leading-7 whitespace-nowrap">Review Link</span>
                <button
                  class="h-10 bg-white text-primary rounded-full flex items-center justify-between px-4 border border-primary"
                  @click="copyToClipboard(surveyLink)">
                  <span class="text-base font-medium mr-2">Copy URL</span>
                  <inline-svg src="assets/copy-icon.svg" class="w-5 h-5 text-primary" />
                </button>
              </div>
            </div>

            <div class="flex items-center justify-start space-x-4">
              <div class="flex items-center space-x-4">
                <span class="text-primary text-lg font-normal leading-7 whitespace-nowrap">User code</span>
                <button
                  class="h-10 bg-white text-primary rounded-full flex items-center justify-between px-4 border border-primary"
                  @click="copyToClipboard(userCode)">
                  <span class="text-base font-medium mr-2">{{ userCode }}</span>
                  <inline-svg src="assets/copy-icon.svg" class="w-5 h-5 text-primary" />
                </button>
              </div>

              <div class="flex items-center space-x-4">
                <span class="text-primary text-lg font-normal leading-7 whitespace-nowrap">Results Link</span>
                <button
                  class="h-10 bg-white text-primary rounded-full flex items-center justify-between px-4 border border-primary"
                  @click="copyToClipboard(resultsLink)">
                  <span class="text-base font-medium mr-2">Copy URL</span>
                  <inline-svg src="assets/copy-icon.svg" class="w-5 h-5 text-primary" />
                </button>
              </div>
            </div>
          </div>

          <div v-else class="flex items-center justify-start space-x-4">
            <div class="flex items-center space-x-4">
              <span class="text-primary text-lg font-normal leading-7 whitespace-nowrap">User code</span>
              <button
                class="h-10 bg-white text-primary rounded-full flex items-center justify-between px-4 border border-primary"
                @click="copyToClipboard(userCode)">
                <span class="text-base font-medium mr-2">{{ userCode }}</span>
                <inline-svg src="assets/copy-icon.svg" class="w-5 h-5 text-primary" />
              </button>
            </div>

            <div class="flex items-center space-x-4">
              <span class="text-primary text-lg font-normal leading-7 whitespace-nowrap">Results Link</span>
              <button
                class="h-10 bg-white text-primary rounded-full flex items-center justify-between px-4 border border-primary"
                @click="copyToClipboard(resultsLink)">
                <span class="text-base font-medium mr-2">Copy URL</span>
                <inline-svg src="assets/copy-icon.svg" class="w-5 h-5 text-primary" />
              </button>
            </div>
          </div>
        </div>

        <!-- Overall Statistics -->
        <div class="bg-neutral-100 p-6 rounded-lg mb-8">
          <h2 class="text-2xl font-semibold text-primary mb-4">Overall Statistics</h2>
          <p v-if="results.overall_statistics" class="mb-2 text-primary">
            Average Deviation from Aggregate: {{ results.overall_statistics.average_deviation_from_aggregate?.toFixed(2) || 'N/A' }}
          </p>
          <p v-if="results.overall_statistics.deviation_from_creator !== undefined" class="mb-2 text-primary">
            Deviation from Creator: {{ results.overall_statistics.deviation_from_creator?.toFixed(2) || 'N/A' }}
          </p>
          <p v-if="results.overall_statistics.deviation_from_others !== undefined" class="mb-2 text-primary">
            Deviation from Others: {{ results.overall_statistics.deviation_from_others?.toFixed(2) || 'N/A' }}
          </p>
          <p v-if="results.overall_statistics.overall_deviation !== undefined" class="mb-2 text-primary">
            Overall Deviation: {{ results.overall_statistics.overall_deviation?.toFixed(2) || 'N/A' }}
          </p>
        </div>

        <!-- Question Results -->
        <div v-if="results.questions">
          <h2 class="text-2xl font-semibold text-primary mb-4">Question Results</h2>
          <div v-for="question in results.questions" :key="question.id" class="bg-white border border-neutral-200 p-6 rounded-lg mb-4 shadow-sm">
            <h3 class="text-xl font-medium text-primary mb-3">{{ question.text }}</h3>
            <div v-if="question.type === 'scale'" class="space-y-2">
              <p class="text-primary">Your Answer: <span class="font-semibold">{{ question.user_score || 'N/A' }}</span></p>
              <p class="text-primary">Average Score: <span class="font-semibold">{{ question.average_score?.toFixed(2) || 'N/A' }}</span></p>
              <p class="text-primary">Your Deviation: <span class="font-semibold">{{ question.user_deviation?.toFixed(2) || 'N/A' }}</span></p>
            </div>
            <div v-else-if="question.type === 'boolean'" class="space-y-2">
              <p class="text-primary">Your Answer: <span class="font-semibold">{{ question.user_answer !== undefined ? (question.user_answer ? 'Yes' : 'No') : 'N/A' }}</span></p>
              <p class="text-primary">Percentage who answered Yes: <span class="font-semibold">{{ question.true_percentage?.toFixed(2) || 'N/A' }}%</span></p>
            </div>
          </div>
        </div>
      </template>
    </div>
    <div v-else class="text-lg text-primary">No results available.</div>
    <ToastView :message="toastMessage" :type="toastType" @hidden="clearToast" />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import api from '@/services/api';
import InlineSvg from 'vue-inline-svg';
import ToastView from '@/components/ToastView.vue';

export default {
  name: 'ResultsView',
  components: {
    InlineSvg,
    ToastView,
  },
  setup() {
    const { t } = useI18n();
    const route = useRoute();
    const results = ref(null);
    const loading = ref(true);
    const error = ref(null);
    const toastMessage = ref('');
    const toastType = ref('');

    const surveyId = computed(() => results.value?.survey_id);
    const userCode = computed(() => route.params.userCode);

    const surveyLink = computed(() => {
      if (surveyId.value) {
        return `/surveys/${surveyId.value}`;
      }
      return '';
    });

    const resultsLink = computed(() => {
      if (surveyId.value && userCode.value) {
        return `/results/${surveyId.value}/${userCode.value}`;
      }
      return '';
    });

    const fetchResults = async () => {
      const { surveyId, userCode } = route.params;
      const fromAnalyze = route.query.fromAnalyze === 'true';

      if (!userCode) {
        error.value = 'User code is missing. Unable to fetch results.';
        loading.value = false;
        return;
      }

      try {
        let response;
        if (fromAnalyze || !surveyId) {
          response = await api.getSurveyResultsByUserCode(userCode);
        } else {
          response = await api.getSurveyResults(surveyId, userCode);
        }
        
        if (response.status === 202) {
          // Handle incomplete results
          results.value = response.data;
        } else {
          // Handle complete results
          results.value = response.data;
        }
      } catch (err) {
        console.error('Error fetching results:', err);
        error.value = 'Failed to load results. Please try again.';
      } finally {
        loading.value = false;
      }
    };

    const copyToClipboard = (text) => {
      navigator.clipboard.writeText(text).then(() => {
        toastMessage.value = t('resultsView.copySuccess');
        toastType.value = 'success';
      }, (err) => {
        console.error('Could not copy text: ', err);
        toastMessage.value = t('resultsView.copyError');
        toastType.value = 'error';
      });
    };

    const clearToast = () => {
      toastMessage.value = '';
      toastType.value = '';
    };

    onMounted(() => {
      fetchResults();
    });

    return {
      results,
      loading,
      error,
      surveyId,
      userCode,
      surveyLink,
      resultsLink,
      copyToClipboard,
      toastMessage,
      toastType,
      clearToast
    };
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;700&display=swap');
</style>