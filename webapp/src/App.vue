<template>
  <div id="app">
    <Home v-if="currentView === 'home'" @participate="showParticipate" @create="showCreate" />
    <Participate v-if="currentView === 'participate'" @submit-code="handleSurveyCode" />
    <TakeSurvey 
      v-if="currentView === 'takeSurvey'" 
      :surveyId="surveyId" 
      :surveyData="surveyData"
      @survey-completed="handleSurveyCompleted"
      @survey-error="handleSurveyError"
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
import Participate from './components/ParticipateView.vue';
import TakeSurvey from './components/TakeSurvey.vue';
import Create from './components/CreateView.vue';
import Toast from './components/ToastView.vue';

export default {
  name: 'App',
  components: {
    Home,
    Participate,
    TakeSurvey,
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
    showParticipate() {
      this.currentView = 'participate';
    },
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
      // You might want to add a 'results' view here
      // this.currentView = 'results';
      // For now, let's just go back to the home view
      this.showToast('Survey submitted successfully!', 'success');
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
      if (this.toastType === 'success' && this.currentView === 'takeSurvey') {
        this.currentView = 'home';
      }
      this.toastMessage = '';
    }
  }
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>