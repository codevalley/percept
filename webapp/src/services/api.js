import axios from 'axios';

const API_URL = 'http://localhost:5001/api/v1'; // Update this to your API's URL

const api = axios.create({
    baseURL: API_URL,
    headers: {
      'Content-Type': 'application/json',
    }
  });

export default {
  // Create a new survey
  createSurvey(surveyData) {
    return api.post(`${API_URL}/surveys`, surveyData);
  },

  // Get a survey by ID
  getSurvey(surveyId) {
    return api.get(`${API_URL}/surveys/${surveyId}`);
  },

  // Submit answers for a survey
  submitAnswers(surveyId, answers) {
    return api.post(`${API_URL}/surveys/${surveyId}/answers`, answers);
  },

  // Get survey results
  getSurveyResults(surveyId, userCode) {
    return api.get(`${API_URL}/surveys/${surveyId}/results`, { params: { user_code: userCode } });
  },

  // Get survey results by user code
  getSurveyResultsByUserCode(userCode) {
    return api.get(`${API_URL}/surveys/results`, { params: { user_code: userCode } });
  },

  // Get IDs
  getIds(count, preferred) {
    return api.get('${API_URL}/ids', { params: { count, id: preferred } });
  },

  // Check ID availability
  checkIdAvailability(id) {
    return api.get('${API_URL}/ids/check', { params: { id } });
  }
};