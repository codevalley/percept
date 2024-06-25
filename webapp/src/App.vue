<template>
  <div id="app">
    <Home v-if="currentView === 'home'" @participate="showParticipate" @create="showCreate" />
    <Participate v-if="currentView === 'participate'" @submit-code="handleSurveyCode" />
    <TakeSurvey 
      v-if="currentView === 'takeSurvey'" 
      :surveyId="surveyId" 
      :surveyData="surveyData"
      @survey-completed="handleSurveyCompleted"
    />
    <Create v-if="currentView === 'create'" />
  </div>
</template>

<script>
import Home from './components/HomeView.vue';
import Participate from './components/ParticipateView.vue';
import TakeSurvey from './components/TakeSurvey.vue';
import Create from './components/CreateView.vue';

export default {
  name: 'App',
  components: {
    Home,
    Participate,
    TakeSurvey,
    Create
  },
  data() {
    return {
      currentView: 'home',
      surveyId: null,
      surveyData: null,
      userCode: null
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
        // Handle error - maybe show an error message to the user
      }
    },
    handleSurveyCompleted(data) {
      console.log('Survey completed:', data);
      this.userCode = data.user_code;
      // You might want to add a 'results' view here
      // this.currentView = 'results';
      // For now, let's just go back to the home view
      this.currentView = 'home';
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