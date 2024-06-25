<template>
  <div id="app">
    <Home v-if="currentView === 'home'" @participate="showParticipate" @create="showCreate" />
    <Participate v-if="currentView === 'participate'" @submit-code="handleSurveyCode" />
    <TakeSurvey v-if="currentView === 'takeSurvey'" :surveyCode="surveyCode" />
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
      surveyCode: ''
    }
  },
  methods: {
    showParticipate() {
      this.currentView = 'participate';
    },
    showCreate() {
      this.currentView = 'create';
    },
    handleSurveyCode(code) {
      this.surveyCode = code;
      this.currentView = 'takeSurvey';
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