<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-gray-800 mb-6">Survey Results</h1>
    <div v-if="loading" class="text-lg text-gray-600">Loading results...</div>
    <div v-else-if="error" class="text-lg text-red-600">{{ error }}</div>
    <div v-else-if="results">
      <div class="bg-gray-100 p-6 rounded-lg mb-8">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Overall Statistics</h2>
        <p v-if="results.overall_statistics" class="mb-2">
          Average Deviation from Aggregate: {{ results.overall_statistics.average_deviation_from_aggregate?.toFixed(2) || 'N/A' }}
        </p>
        <p v-if="results.overall_statistics.deviation_from_creator !== undefined" class="mb-2">
          Deviation from Creator: {{ results.overall_statistics.deviation_from_creator?.toFixed(2) || 'N/A' }}
        </p>
        <p v-if="results.overall_statistics.deviation_from_others !== undefined" class="mb-2">
          Deviation from Others: {{ results.overall_statistics.deviation_from_others?.toFixed(2) || 'N/A' }}
        </p>
        <p v-if="results.overall_statistics.overall_deviation !== undefined" class="mb-2">
          Overall Deviation: {{ results.overall_statistics.overall_deviation?.toFixed(2) || 'N/A' }}
        </p>
      </div>
      <div v-if="results.questions">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Question Results</h2>
        <div v-for="question in results.questions" :key="question.id" class="bg-white border border-gray-200 p-6 rounded-lg mb-4 shadow-sm">
          <h3 class="text-xl font-medium text-gray-700 mb-3">{{ question.text }}</h3>
          <div v-if="question.type === 'scale'" class="space-y-2">
            <p>Your Answer: <span class="font-semibold">{{ question.user_score || 'N/A' }}</span></p>
            <p>Average Score: <span class="font-semibold">{{ question.average_score?.toFixed(2) || 'N/A' }}</span></p>
            <p>Your Deviation: <span class="font-semibold">{{ question.user_deviation?.toFixed(2) || 'N/A' }}</span></p>
          </div>
          <div v-else-if="question.type === 'boolean'" class="space-y-2">
            <p>Your Answer: <span class="font-semibold">{{ question.user_answer !== undefined ? (question.user_answer ? 'Yes' : 'No') : 'N/A' }}</span></p>
            <p>Percentage who answered Yes: <span class="font-semibold">{{ question.true_percentage?.toFixed(2) || 'N/A' }}%</span></p>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-lg text-gray-600">No results available.</div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'ResultsView',
  props: {
    surveyId: {
      type: String,
      required: true
    },
    userCode: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      results: null,
      loading: true,
      error: null
    };
  },
  mounted() {
    this.fetchResults();
  },
  methods: {
    async fetchResults() {
      try {
        const response = await api.getSurveyResults(this.surveyId, this.userCode);
        this.results = response.data;
        this.loading = false;
      } catch (error) {
        console.error('Error fetching results:', error);
        this.error = 'Failed to load results. Please try again.';
        this.loading = false;
      }
    }
  }
}
</script>