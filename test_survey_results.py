import unittest
import json
from app import app, mongo

class TestSurveyResults(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['MONGO_URI'] = "mongodb://localhost:27017/backfeed_test"
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            mongo.db.surveys.delete_many({})
            mongo.db.answers.delete_many({})

    def setUp(self):
        with app.app_context():
            mongo.db.surveys.delete_many({})
            mongo.db.answers.delete_many({})
        
        self.survey_data = {
            "title": "Customer Satisfaction Survey",
            "description": "Help us improve our service",
            "questions": [
                {
                    "text": "How satisfied are you with our product?",
                    "response_type": "scale",
                    "response_scale_max": 5,
                    "creator_answer": 4
                },
                {
                    "text": "Would you recommend our product to others?",
                    "response_type": "boolean",
                    "creator_answer": True
                },
                {
                    "text": "How likely are you to purchase again?",
                    "response_type": "scale",
                    "response_scale_max": 10,
                    "creator_answer": 8
                },
                {
                    "text": "Did you find our customer support helpful?",
                    "response_type": "boolean",
                    "creator_answer": True
                }
            ]
        }
        
        response = self.client.post('/api/v1/surveys',
                                    data=json.dumps(self.survey_data),
                                    content_type='application/json')
        self.survey_response = json.loads(response.data)
        self.survey_id = self.survey_response['survey_id']
        self.creator_code = self.survey_response['user_code']
        
        self.add_sample_responses()

    def add_sample_responses(self):
        responses = [
            {"answers": [{"question_id": 1, "answer": 4}, {"question_id": 2, "answer": True},
                         {"question_id": 3, "answer": 7}, {"question_id": 4, "answer": True}]},
            {"answers": [{"question_id": 1, "answer": 5}, {"question_id": 2, "answer": True},
                         {"question_id": 3, "answer": 9}, {"question_id": 4, "answer": True}]},
            {"answers": [{"question_id": 1, "answer": 3}, {"question_id": 2, "answer": False},
                         {"question_id": 3, "answer": 6}, {"question_id": 4, "answer": False}]},
            {"answers": [{"question_id": 1, "answer": 4}, {"question_id": 2, "answer": True},
                         {"question_id": 3, "answer": 8}, {"question_id": 4, "answer": True}]},
            {"answers": [{"question_id": 1, "answer": 2}, {"question_id": 2, "answer": False},
                         {"question_id": 3, "answer": 5}, {"question_id": 4, "answer": True}]}
        ]
        
        self.participant_codes = []
        for response in responses:
            resp = self.client.post(f'/api/v1/surveys/{self.survey_id}/answers',
                                    data=json.dumps(response),
                                    content_type='application/json')
            self.participant_codes.append(json.loads(resp.data)['user_code'])

    def test_creator_results(self):
        response = self.client.get(f'/api/v1/surveys/{self.survey_id}/results?user_code={self.creator_code}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['user_type'], 'creator')
        self.assertEqual(len(data['questions']), 4)
        self.assertEqual(data['total_responses'], 5)
        
        scale_questions = [q for q in data['questions'] if q['type'] == 'scale']
        for question in scale_questions:
            self.assertIn('distribution', question)
        
        self.assertIn('overall_statistics', data)
        self.assertIn('highest_rated_question', data['overall_statistics'])
        self.assertIn('lowest_rated_question', data['overall_statistics'])

    def test_participant_results(self):
        participant_code = self.participant_codes[0]
        
        response = self.client.get(f'/api/v1/surveys/{self.survey_id}/results?user_code={participant_code}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['user_type'], 'participant')
        self.assertEqual(len(data['questions']), 4)
        self.assertNotIn('total_responses', data)
        
        scale_questions = [q for q in data['questions'] if q['type'] == 'scale']
        for question in scale_questions:
            self.assertIn('user_score', question)
            self.assertIn('user_deviation', question)
        
        self.assertIn('overall_statistics', data)
        self.assertIn('average_deviation_from_aggregate', data['overall_statistics'])

    def test_invalid_user_code(self):
        response = self.client.get(f'/api/v1/surveys/{self.survey_id}/results?user_code=999999')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['user_type'], 'participant')
        self.assertNotIn('total_responses', data)

    def test_nonexistent_survey(self):
        response = self.client.get(f'/api/v1/surveys/999999/results?user_code={self.creator_code}')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()