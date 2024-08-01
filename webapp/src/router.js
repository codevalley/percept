import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/components/HomeView.vue'
import CreateView from '@/components/CreateView.vue'
import TakeSurvey from '@/components/TakeSurvey.vue'
import ResultsView from '@/components/ResultsView.vue'
import NotFound from './components/NotFound.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/new',
    name: 'Create',
    component: CreateView
  },
  {
    path: '/:surveyId',  // This ensures surveyId must be a number
    name: 'TakeSurvey',
    component: TakeSurvey,
    props: route => ({ 
      surveyId: route.params.surveyId ? route.params.surveyId : null,
      surveyData: null  // We'll pass null for surveyData by default
    }),
  },
  {
    path: '/u/:userCode',
    name: 'Results',
    component: ResultsView,
    props: true
  },
  {
    path: '/u/:surveyId/:userCode',
    name: 'SurveyResults',
    component: ResultsView,
    props: true
  },{
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound  // Create a NotFound component for 404 errors
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router