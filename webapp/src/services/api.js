import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:5001/api/v1'; // Update this to your API's URL

const api = axios.create({
    baseURL: API_URL,
    headers: {
      'Content-Type': 'application/json',
    }
  });

export default {
  // Create a new survey
  createSurvey(surveyData) {
    return api.post(`/surveys`, surveyData);
  },

  // Get a survey by ID
  getSurvey(surveyId) {
    return api.get(`/surveys/${surveyId}`);
  },

  // Submit answers for a survey
  submitAnswers(surveyId, answers) {
    return api.post(`/surveys/${surveyId}/answers`, answers);
  },

  // Get survey results
  getSurveyResults(surveyId, userCode) {
    return api.get(`/surveys/${surveyId}/results`, { params: { user_code: userCode } });
  },

  // Get survey results by user code
  getSurveyResultsByUserCode(userCode) {
    return api.get(`/surveys/results`, { params: { user_code: userCode } });
  },

  // Get IDs
  getIds(count, preferred) {
    return api.get(`/ids`, { params: { count, id: preferred } });
  },

  // Check ID availability
  checkIdAvailability(id) {
    return api.get(`/ids/check`, { params: { id } });
  }
};