<template>
  <div class="font-['IBM_Plex_Sans'] max-w-full sm:max-w-3xl mx-auto px-4 py-6 sm:py-8">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between  sm:mb-2">
      <h1 class="text-2xl sm:text-3xl font-bold text-primary sm:mb-1">Survey Results</h1>
      
      <div class="flex flex-wrap items-center gap-2">
        <SurveyExpiryChip 
          v-if="results"
          :expiry-date="results.expiry_date"
          :is-expired="results.expired"
        />
        <SurveyChips 
          v-if="results"
          :is-trending="results.is_trending"
          :participant-bucket="results.participant_bucket"
          class="mt-2 mb-2 sm:mb-0 sm:mt-0"
        />
      </div>
    </div>

    <div v-if="loading" class="text-lg text-primary">Loading results...</div>
    <div v-else-if="error" class="text-lg text-accent">{{ error }}</div>
    <div v-else-if="results">
      <!-- Always show LinkShareSection for both creators and participants -->
      <LinkShareSection 
        v-if="results.is_creator || !isExpired"
        :showSurveyLink="results.is_creator && !isExpired"
        :showResultsLink="true"
        :surveyCode="surveyCode"
        :resultsCode="userCode"
        :surveyLinkLabel="results.is_creator ? 'Review link' : 'Your review link'"
        :resultsLinkLabel="results.is_creator ? 'Result link' : 'Your results link'"
        :surveyLinkDescription="'Share it with your friends for feedback'"
        :resultsLinkDescription="results.is_creator ? 'Bookmark and come here later to see results' : 'Bookmark this link to view your results later'"
        :baseUrl="baseUrl"
        @copy-success="handleCopySuccess"
        @copy-error="handleCopyError"
      />
      <div class="mb-6"></div>
      <div v-if="results.status === 'incomplete'" class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4 text-sm sm:text-base">
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
      <template v-else>
        <div class="bg-neutral-100 p-4 sm:p-6 rounded-lg mb-6 sm:mb-8">
          <h2 class="text-xl sm:text-2xl font-semibold text-primary mb-3 sm:mb-4">Overall Statistics</h2>
          <!-- Overall Statistics -->
          <template v-if="results.user_type === 'creator'">
            <p v-if="typeof results.overall_statistics.overall_deviation === 'number'" class="mb-2 text-primary text-sm sm:text-base">
              Overall Deviation: {{ results.overall_statistics.overall_deviation.toFixed(2) }}
            </p>
            <p v-if="typeof results.overall_statistics.average_deviation_from_aggregate === 'number'" class="mb-2 text-primary text-sm sm:text-base">
              Average Deviation from Aggregate: {{ results.overall_statistics.average_deviation_from_aggregate.toFixed(2) }}
            </p>
          </template>
          <template v-else>
            <p v-if="typeof results.overall_statistics.average_deviation_from_aggregate === 'number'" class="mb-2 text-primary text-sm sm:text-base">
              Average Deviation from Aggregate: {{ results.overall_statistics.average_deviation_from_aggregate.toFixed(2) }}
            </p>
            <p v-if="typeof results.overall_statistics.average_deviation_from_creator === 'number'" class="mb-2 text-primary text-sm sm:text-base">
              Average Deviation from Creator: {{ results.overall_statistics.average_deviation_from_creator.toFixed(2) }}
            </p>
            <p v-if="typeof results.overall_statistics.average_deviation_from_others === 'number'" class="mb-2 text-primary text-sm sm:text-base">
              Average Deviation from Others: {{ results.overall_statistics.average_deviation_from_others.toFixed(2) }}
            </p>
            <p v-if="typeof results.overall_statistics.overall_deviation === 'number'" class="mb-2 text-primary text-sm sm:text-base">
              Overall Deviation: {{ results.overall_statistics.overall_deviation.toFixed(2) }}
            </p>
          </template>
        </div>
        <div v-if="results.questions">
          <h2 class="text-xl sm:text-2xl font-semibold text-primary mb-3 sm:mb-4">Question Results</h2>
          <div v-for="question in results.questions" :key="question.id" class="bg-white border border-neutral-200 p-4 sm:p-6 rounded-lg mb-4 shadow-sm">
            <h3 class="text-lg sm:text-xl font-medium text-primary mb-2 sm:mb-3">{{ question.text }}</h3>
            <div v-if="question.type === 'scale'">
              <!-- For creators, show distribution and average without user-specific scores -->
              <template v-if="results.user_type === 'creator'">
                <p class="text-primary">Average Score: <span class="font-semibold">{{ typeof question.average_score === 'number' ? question.average_score.toFixed(2) : 'N/A' }}</span></p>
                <p class="text-primary">Standard Deviation: <span class="font-semibold">{{ typeof question.standard_deviation === 'number' ? question.standard_deviation.toFixed(2) : 'N/A' }}</span></p>
                <div v-if="question.distribution">
                  <p class="text-primary" v-for="(count, score) in question.distribution" :key="score">
                    {{ score }}: {{ count }} responses
                  </p>
                </div>
              </template>
              <!-- For participants, show their score, average and their deviation -->
              <template v-else>
                <p class="text-primary">Your Answer: <span class="font-semibold">{{ question.user_score || 'N/A' }}</span></p>
                <p class="text-primary">Average Score: <span class="font-semibold">{{ typeof question.average_score === 'number' ? question.average_score.toFixed(2) : 'N/A' }}</span></p>
                <p class="text-primary">Your Deviation from Average: <span class="font-semibold">{{ typeof question.user_deviation === 'number' ? question.user_deviation.toFixed(2) : 'N/A' }}</span></p>
                <p class="text-primary">Your Deviation from Creator: <span class="font-semibold">{{ typeof question.deviation_from_creator === 'number' ? question.deviation_from_creator.toFixed(2) : 'N/A' }}</span></p>
                <p class="text-primary">Your Deviation from Others: <span class="font-semibold">{{ typeof question.deviation_from_others === 'number' ? question.deviation_from_others.toFixed(2) : 'N/A' }}</span></p>
              </template>
            </div>
            <div v-else-if="question.type === 'boolean'">
              <!-- Show percentages for both creator and participant -->
              <p class="text-primary">Percentage who answered Yes: <span class="font-semibold">{{ typeof question.true_percentage === 'number' ? question.true_percentage.toFixed(2) : 'N/A' }}%</span></p>
              <p class="text-primary">Percentage who answered No: <span class="font-semibold">{{ typeof question.false_percentage === 'number' ? question.false_percentage.toFixed(2) : 'N/A' }}%</span></p>
              <p v-if="results.user_type === 'participant'" class="text-primary">Your Answer: <span class="font-semibold">{{ question.user_answer ? 'Yes' : 'No' }}</span></p>
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
//import InlineSvg from 'vue-inline-svg';
import ToastView from '@/components/ToastView.vue';
import SurveyChips from '@/components/SurveyChips.vue';
import SurveyExpiryChip from '@/components/SurveyExpiryChip.vue';
import LinkShareSection from '@/components/ShareView.vue'

export default {
  name: 'ResultsView',
  components: {
    
    ToastView,
    SurveyChips,
    SurveyExpiryChip,
    LinkShareSection,
  },
  setup() {
    const { t } = useI18n();
    const route = useRoute();
    const results = ref(null);
    const loading = ref(true);
    const error = ref(null);
    const toastMessage = ref('');
    const toastType = ref('');

    const userCode = computed(() => route.params.userCode || (results.value?.user_code ?? ''));
    const surveyCode = computed(() => results.value?.survey_id ?? '');
    const isExpired = computed(() => results.value?.expired ?? false);
    const baseUrl = computed(() => process.env.VUE_APP_BASE_URL || '');
    
    const handleError = (err) => {
      console.error('Error fetching results:', err);
      if (err.response) {
        switch (err.response.status) {
          case 404:
            error.value = 'Survey or user not found. Please check your IDs and try again.';
            break;
          case 403:
            error.value = 'You do not have permission to view these results.';
            break;
          case 202:
            error.value = 'Not enough responses available to show stats.';
            break;
          default:
            error.value = 'An error occurred while fetching results. Please try again later.';
        }
      } else if (err.request) {
        error.value = 'Unable to reach the server. Please check your internet connection and try again.';
      } else {
        error.value = 'An unexpected error occurred. Please try again.';
      }
    };

    const fetchResults = async () => {
      if (!userCode.value) {
        error.value = 'User code is missing. Unable to fetch results.';
        loading.value = false;
        return;
      }

      try {
        const response = await api.getSurveyResultsByUserCode(userCode.value);
        if (response && response.data) {
          results.value = response.data;
          console.log('Successfully fetched data:', results.value);
        } else {
          throw new Error('Invalid API response');
        }
      } catch (err) {
        console.error('Fetch error:', err);
        handleError(err);
      } finally {
        loading.value = false;
      }
    };

    const clearToast = () => {
      toastMessage.value = '';
      toastType.value = '';
    };

    const handleCopySuccess = () => {
      toastMessage.value = t('copySuccess');
      toastType.value = 'success';
    };

    const handleCopyError = () => {
      toastMessage.value = t('copyError');
      toastType.value = 'error';
    };
    onMounted(() => {
      console.log('Component mounted. Fetching results...');
      fetchResults();
    });

    return {
      results,
      loading,
      error,
      userCode,
      surveyCode,
      //copyToClipboard,
      toastMessage,
      toastType,
      //openAndCopy,
      clearToast,
      handleCopyError,
      handleCopySuccess,
      isExpired,
      baseUrl,
    };
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;700&display=swap');
</style>
