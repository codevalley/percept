import axios from 'axios';
import { result } from 'lodash';


const API_URL = `${process.env.VUE_APP_API_URL}/v1` || 'http://localhost:5001/v1'; // Update this to your API's URLconsole.log('Router Base URL:', `${process.env.VUE_APP_API_URL}`); // For debugging
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
    result = api.get(`/surveys/${surveyId}`);
    console.log("Get survey: ". result);
    return result;
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