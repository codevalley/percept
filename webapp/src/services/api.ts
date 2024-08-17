import axios, { AxiosInstance, AxiosResponse } from 'axios';

const isDevelopment = process.env.VUE_APP_ENV === 'development';
const API_URL = isDevelopment ? '/v1' : `${process.env.VUE_APP_API_URL}/v1`;

const api: AxiosInstance = axios.create({
    baseURL: API_URL,
    headers: {
      'Content-Type': 'application/json',
    }
});

interface SurveyData {
  // Define the structure of your survey data here
  // For example:
  title: string;
  description?: string;
  questions: Array<{
    text: string;
    type: string;
    // Add other question properties
  }>;
  // Add other survey properties
}

interface AnswerData {
  // Define the structure of your answer data here
  // For example:
  answers: Array<{
    question_id: number;
    answer: string | number | boolean;
  }>;
}

export default {
  // Create a new survey
  createSurvey(surveyData: SurveyData): Promise<AxiosResponse> {
    return api.post(`/surveys`, surveyData);
  },

  // Get a survey by ID
  getSurvey(surveyId: string): Promise<AxiosResponse> {
    return api.get(`/surveys/${surveyId}`);
  },

  // Submit answers for a survey
  submitAnswers(surveyId: string, answers: AnswerData): Promise<AxiosResponse> {
    return api.post(`/surveys/${surveyId}/answers`, answers);
  },

  // Get survey results
  getSurveyResults(surveyId: string, userCode: string): Promise<AxiosResponse> {
    return api.get(`/surveys/${surveyId}/results`, { params: { user_code: userCode } });
  },

  // Get survey results by user code
  getSurveyResultsByUserCode(userCode: string): Promise<AxiosResponse> {
    return api.get(`/surveys/results`, { params: { user_code: userCode } });
  },

  // Get IDs
  getIds(count: number, preferred?: string): Promise<AxiosResponse> {
    return api.get(`/ids`, { params: { count, id: preferred } });
  },

  // Check ID availability
  checkIdAvailability(id: string): Promise<AxiosResponse> {
    return api.get(`/ids/check`, { params: { id } });
  }
};