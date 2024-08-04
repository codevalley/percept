import unittest
import json
from datetime import datetime, timedelta, UTC
from app import app, mongo, id_manager,make_tz_aware, MINIMUM_RESPONSES

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
            ],
            "expiry_date": make_tz_aware(datetime.now(UTC) + timedelta(days=7)).isoformat(),
        }
        
        response = self.client.post('/v1/surveys',
                                    data=json.dumps(self.survey_data),
                                    content_type='application/json')
        self.survey_response = json.loads(response.data)
        
        if 'error' in self.survey_response:
            self.skipTest(f"Survey creation failed: {self.survey_response['error']}")
        
        # Verify that the response contains the expected keys
        expected_keys = ['survey_id', 'share_link', 'user_code', 'questions', 'expiry_date']
        for key in expected_keys:
            self.assertIn(key, self.survey_response, f"Expected key '{key}' not found in response")

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
            resp = self.client.post(f'/v1/surveys/{self.survey_id}/answers',
                                    data=json.dumps(response),
                                    content_type='application/json')
            response_data = json.loads(resp.data)
            self.assertEqual(resp.status_code, 201)
            self.assertIn('user_code', response_data)
            self.participant_codes.append(response_data['user_code'])

    def test_create_survey(self):
        response = self.client.post('/v1/surveys',
                                    data=json.dumps(self.survey_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('survey_id', data)
        self.assertIn('user_code', data)
        self.assertIsInstance(data['survey_id'], str)
        self.assertIsInstance(data['user_code'], str)

    def test_get_survey(self):
        # First, create a new survey
        response = self.client.post('/v1/surveys',
                                    data=json.dumps(self.survey_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        create_data = json.loads(response.data)
        survey_id = create_data['survey_id']

        # Now, try to get the survey we just created
        response = self.client.get(f'/v1/surveys/{survey_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        # Verify the retrieved data
        self.assertEqual(data['title'], self.survey_data['title'])
        self.assertEqual(data['description'], self.survey_data['description'])
        self.assertEqual(len(data['questions']), len(self.survey_data['questions']))
        
        # Check each question
        for i, question in enumerate(data['questions']):
            self.assertEqual(question['text'], self.survey_data['questions'][i]['text'])
            self.assertEqual(question['response_type'], self.survey_data['questions'][i]['response_type'])
            if 'response_scale_max' in self.survey_data['questions'][i]:
                self.assertEqual(question['response_scale_max'], self.survey_data['questions'][i]['response_scale_max'])

    def test_submit_answers(self):
        response_data = {
            "answers": [
                {"question_id": "1", "answer": 3},
                {"question_id": "2", "answer": False},
                {"question_id": "3", "answer": 7},
                {"question_id": "4", "answer": True}
            ]
        }
        response = self.client.post(f'/v1/surveys/{self.survey_id}/answers',
                                    data=json.dumps(response_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('user_code', data)
        self.assertIn('deviation_from_creator', data)
        self.assertIn('deviation_from_others', data)
        self.assertIn('overall_deviation', data)

    def test_submit_answers_invalid_data(self):
        # Test answer out of range for scale question
        invalid_data = {"answers": [{"question_id": "1", "answer": 6}]}  # Max is 5 for this question
        response = self.client.post(f'/v1/surveys/{self.survey_id}/answers',
                                    data=json.dumps(invalid_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test invalid boolean answer
        invalid_data = {"answers": [{"question_id": "2", "answer": "Not a boolean"}]}
        response = self.client.post(f'/v1/surveys/{self.survey_id}/answers',
                                    data=json.dumps(invalid_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test invalid question ID
        invalid_data = {"answers": [{"question_id": "999", "answer": 5}]}
        response = self.client.post(f'/v1/surveys/{self.survey_id}/answers',
                                    data=json.dumps(invalid_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test missing question_id
        invalid_data = {"answers": [{"answer": 5}]}
        response = self.client.post(f'/v1/surveys/{self.survey_id}/answers',
                                    data=json.dumps(invalid_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test missing answer
        invalid_data = {"answers": [{"question_id": "1"}]}
        response = self.client.post(f'/v1/surveys/{self.survey_id}/answers',
                                    data=json.dumps(invalid_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_creator_results(self):
        response = self.client.get(f'/v1/surveys/{self.survey_id}/results?user_code={self.creator_code}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['user_type'], 'creator')
        self.assertEqual(len(data['questions']), 4)
        self.assertEqual(data['total_responses'], 5)
        self.assertIsInstance(data['survey_id'], str)
        
        scale_questions = [q for q in data['questions'] if q['type'] == 'scale']
        for question in scale_questions:
            self.assertIn('distribution', question)
        
        self.assertIn('overall_statistics', data)
        self.assertIn('average_deviation_from_aggregate', data['overall_statistics'])
        self.assertIn('overall_deviation', data['overall_statistics'])


    def test_participant_results(self):
        participant_code = self.participant_codes[0]
        
        response = self.client.get(f'/v1/surveys/{self.survey_id}/results?user_code={participant_code}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['user_type'], 'participant')
        self.assertEqual(len(data['questions']), 4)
        self.assertIsInstance(data['survey_id'], str)
        
        scale_questions = [q for q in data['questions'] if q['type'] == 'scale']
        for question in scale_questions:
            self.assertIn('user_score', question)
            self.assertIn('user_deviation', question)
        
        self.assertIn('overall_statistics', data)
        self.assertIn('average_deviation_from_aggregate', data['overall_statistics'])
        self.assertIn('average_deviation_from_creator', data['overall_statistics'])
        self.assertIn('average_deviation_from_others', data['overall_statistics'])
        self.assertIn('overall_deviation', data['overall_statistics'])


    def test_invalid_user_code(self):
        invalid_code = id_manager.get_id()  # Get a valid format but unused ID
        response = self.client.get(f'/v1/surveys/{self.survey_id}/results?user_code={invalid_code}')
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_survey(self):
        nonexistent_survey_id = id_manager.get_id()  # Get a valid format but unused ID
        response = self.client.get(f'/v1/surveys/{nonexistent_survey_id}/results?user_code={self.creator_code}')
        self.assertEqual(response.status_code, 404)

    def test_get_results_by_user_code(self):
        participant_code = self.participant_codes[0]
        
        response = self.client.get(f'/v1/surveys/results?user_code={participant_code}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['user_type'], 'participant')
        self.assertEqual(len(data['questions']), 4)
        self.assertIsInstance(data['survey_id'], str)
        self.assertIn('overall_statistics', data)
        self.assertIn('average_deviation_from_aggregate', data['overall_statistics'])
        self.assertIn('average_deviation_from_creator', data['overall_statistics'])
        self.assertIn('average_deviation_from_others', data['overall_statistics'])
        self.assertIn('overall_deviation', data['overall_statistics'])


    def test_get_results_by_invalid_user_code(self):
        invalid_code = id_manager.get_id()  # Get a valid format but unused ID
        response = self.client.get(f'/v1/surveys/results?user_code={invalid_code}')
        self.assertEqual(response.status_code, 404)

    def test_id_format(self):
        # Test that generated IDs are strings and match expected format
        survey_id = self.survey_id
        user_code = self.creator_code
        
        self.assertIsInstance(survey_id, str)
        self.assertIsInstance(user_code, str)
        # Add more specific checks if your ID format is known (e.g., regex pattern)

    def test_get_ids(self):
        response = self.client.get('/v1/ids?count=5')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('ids', data)
        self.assertEqual(len(data['ids']), 5)
        for id in data['ids']:
            self.assertIsInstance(id, str)

    def test_check_id_availability(self):
        # Test with an available ID
        available_ids = id_manager.get_ids(count=1)  # Get an ID without marking it as used
        self.assertTrue(len(available_ids) > 0, "Failed to get an available ID")
        available_id = available_ids[0]
        
        response = self.client.get(f'/v1/ids/check?id={available_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['available'])

        # Test with an unavailable ID (the survey_id we created)
        response = self.client.get(f'/v1/ids/check?id={self.survey_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data['available'])

        # Now mark the previously available ID as used
        id_manager.mark_id_as_used(available_id)

        # Check that it's now unavailable
        response = self.client.get(f'/v1/ids/check?id={available_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data['available'])

    def test_survey_expiry(self):
        # Test creating a survey with expiry date
        survey_data = self.survey_data.copy()
        survey_data['expiry_date'] = make_tz_aware(datetime.now() + timedelta(days=1)).isoformat()
        response = self.client.post('/v1/surveys',
                                    data=json.dumps(survey_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        survey_id = json.loads(response.data)['survey_id']

        # Test getting survey before expiry
        response = self.client.get(f'/v1/surveys/{survey_id}')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.data)['expired'])

        # Test getting survey after expiry
        with app.app_context():
            mongo.db.surveys.update_one(
                {'survey_id': survey_id},
                {'$set': {'expiry_date': make_tz_aware(datetime.now() - timedelta(days=1)).isoformat()}}
            )
        response = self.client.get(f'/v1/surveys/{survey_id}')
        self.assertEqual(response.status_code, 410)
        self.assertTrue(json.loads(response.data)['expired'])

    def test_trending_survey(self):
        # Add multiple responses within 24 hours
        for _ in range(5):
            self.add_sample_responses()

        # Check if the survey is trending
        response = self.client.get(f'/v1/surveys/{self.survey_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['is_trending'])

    def test_participant_bucket(self):
        # Test with less than 10 participants
        response = self.client.get(f'/v1/surveys/{self.survey_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['participant_bucket'], '< 10')

        # Add more responses to change the bucket
        for _ in range(10):
            self.add_sample_responses()

        response = self.client.get(f'/v1/surveys/{self.survey_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['participant_bucket'], '10-100')

    def test_survey_results_with_new_fields(self):
        response = self.client.get(f'/v1/surveys/{self.survey_id}/results?user_code={self.creator_code}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('is_trending', data)
        self.assertIn('participant_bucket', data)
        self.assertIn('expiry_date', data)
        self.assertIn('expired', data)
    
    def test_survey_with_no_responses(self):
        # Create a new survey without adding any responses
        response = self.client.post('/v1/surveys',
                                    data=json.dumps(self.survey_data),
                                    content_type='application/json')
        new_survey_id = json.loads(response.data)['survey_id']
        new_creator_code = json.loads(response.data)['user_code']

        # Get results for this survey
        response = self.client.get(f'/v1/surveys/{new_survey_id}/results?user_code={new_creator_code}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'incomplete')
        self.assertEqual(data['current_responses'], 0)
        self.assertEqual(data['minimum_responses'], MINIMUM_RESPONSES)
        self.assertEqual(data['remaining_responses'], MINIMUM_RESPONSES)
        self.assertTrue(data['is_creator'])
        self.assertEqual(data['participant_bucket'], '< 10')
        self.assertFalse(data['is_trending'])

    def test_survey_about_to_expire(self):
        # Create a survey that expires in 5 minutes
        survey_data = self.survey_data.copy()
        survey_data['expiry_date'] = make_tz_aware(datetime.now(UTC) + timedelta(minutes=5)).isoformat()
        response = self.client.post('/v1/surveys',
                                    data=json.dumps(survey_data),
                                    content_type='application/json')
        survey_id = json.loads(response.data)['survey_id']

        # Check the survey
        response = self.client.get(f'/v1/surveys/{survey_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data['expired'])
        # You might want to add an 'expiring_soon' field to your API for this case
        # self.assertTrue(data['expiring_soon'])

if __name__ == '__main__':
    unittest.main()