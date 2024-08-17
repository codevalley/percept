import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '@/components/HomeView.vue'
import CreateView from '@/components/CreateView.vue'
import TakeSurvey from '@/components/TakeSurvey.vue'
import ResultsView from '@/components/ResultsView.vue'
import NotFound from './components/NotFound.vue'

const routes: Array<RouteRecordRaw> = [
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
    path: '/:surveyId',
    name: 'TakeSurvey',
    component: TakeSurvey,
    props: (route) => ({ 
      surveyId: route.params.surveyId ? route.params.surveyId as string : null,
      surveyData: null
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
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router