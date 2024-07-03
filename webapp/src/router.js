import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/components/HomeView.vue'
import CreateView from '@/components/CreateView.vue'
import TakeSurvey from '@/components/TakeSurvey.vue'
import ResultsView from '@/components/ResultsView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/create',
    name: 'Create',
    component: CreateView
  },
  {
    path: '/participate/:surveyId',
    name: 'TakeSurvey',
    component: TakeSurvey,
    props: true
  },
  {
    path: '/results/:surveyId/:userCode',
    name: 'Results',
    component: ResultsView,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router