<template>
  <div id="app">
    <Home 
      v-if="currentView === 'home'" 
      @create="showCreate" 
      @submit-code="handleSurveyCode"
    />
    <TakeSurvey 
      v-if="currentView === 'takeSurvey'" 
      :surveyId="surveyId" 
      :surveyData="surveyData"
      @survey-completed="handleSurveyCompleted"
      @survey-error="handleSurveyError"
    />
    <ResultsView
      v-if="currentView === 'results'"
      :surveyId="surveyId"
      :userCode="userCode"
    />
    <Create v-if="currentView === 'create'" />
    <Toast 
      :message="toastMessage" 
      :type="toastType" 
      :duration="3000"
      @hidden="handleToastHidden"
    />
  </div>
</template>

<script>
import Home from './components/HomeView.vue';
import TakeSurvey from './components/TakeSurvey.vue';
import ResultsView from './components/ResultsView.vue';
import Create from './components/CreateView.vue';
import Toast from './components/ToastView.vue';

export default {
  name: 'App',
  components: {
    Home,
    TakeSurvey,
    ResultsView,
    Create,
    Toast
  },
  data() {
    return {
      currentView: 'home',
      surveyId: null,
      surveyData: null,
      userCode: null,
      toastMessage: '',
      toastType: 'success'
    }
  },
  methods: {
    showCreate() {
      this.currentView = 'create';
    },
    handleSurveyCode({ surveyId, surveyData }) {
      console.log('Received survey data:', surveyId, surveyData);
      this.surveyId = surveyId;
      this.surveyData = surveyData;
      if (this.surveyId && this.surveyData) {
        console.log('Changing view to takeSurvey');
        this.currentView = 'takeSurvey';
      } else {
        console.error('Invalid survey data received');
        this.showToast('Error: Invalid survey data', 'error');
      }
    },
    handleSurveyCompleted(data) {
      console.log('Survey completed:', data);
      this.userCode = data.user_code;
      this.showToast('Survey submitted successfully!', 'success');
      this.currentView = 'results';
    },
    handleSurveyError(errorMessage) {
      this.showToast(errorMessage, 'error');
    },
    showToast(message, type = 'success') {
      console.log('Showing toast:', message, type);
      this.toastMessage = message;
      this.toastType = type;
    },
    handleToastHidden() {
      this.toastMessage = '';
    }
  }
}
</script>

<style>
#app {
  font-family: 'IBM Plex Sans', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>