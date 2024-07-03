// src/services/api.js

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
    return api.get(`${API_URL}/surveys/${surveyId}/results?user_code=${userCode}`);
  },
  getSurveyResultsByUserCode(userCode) {
    return api.get(`${API_URL}/surveys/results?user_code=${userCode}`);
  },
};