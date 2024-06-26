<template>
  <div class="results-view">
    <h1>Survey Results</h1>
    <div v-if="loading">Loading results...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else-if="results">
      <div class="overall-stats">
        <h2>Overall Statistics</h2>
        <p v-if="results.overall_statistics">
          Average Deviation from Aggregate: {{ results.overall_statistics.average_deviation_from_aggregate?.toFixed(2) || 'N/A' }}
        </p>
        <p v-if="results.overall_statistics.deviation_from_creator !== undefined">Deviation from Creator: {{ results.overall_statistics.deviation_from_creator?.toFixed(2) || 'N/A' }}</p>
        <p v-if="results.overall_statistics.deviation_from_others !== undefined">Deviation from Others: {{ results.overall_statistics.deviation_from_others?.toFixed(2) || 'N/A' }}</p>
        <p v-if="results.overall_statistics.overall_deviation !== undefined">Overall Deviation: {{ results.overall_statistics.overall_deviation?.toFixed(2) || 'N/A' }}</p>
      </div>
      <div class="questions" v-if="results.questions">
        <h2>Question Results</h2>
        <div v-for="question in results.questions" :key="question.id" class="question-result">
          <h3>{{ question.text }}</h3>
          <p v-if="question.type === 'scale'">
            Your Answer: {{ question.user_score || 'N/A' }}
            <br>
            Average Score: {{ question.average_score?.toFixed(2) || 'N/A' }}
            <br>
            Your Deviation: {{ question.user_deviation?.toFixed(2) || 'N/A' }}
          </p>
          <p v-else-if="question.type === 'boolean'">
            Your Answer: {{ question.user_answer !== undefined ? (question.user_answer ? 'Yes' : 'No') : 'N/A' }}
            <br>
            Percentage who answered Yes: {{ question.true_percentage?.toFixed(2) || 'N/A' }}%
          </p>
        </div>
      </div>
    </div>
    <div v-else>No results available.</div>
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

<style scoped>
.results-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.overall-stats {
  background-color: #f0f0f0;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.question-result {
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 8px;
}

h1, h2 {
  color: #333;
}

h3 {
  color: #555;
}
</style>