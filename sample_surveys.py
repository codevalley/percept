# populate_sample_data.py

import requests
import json
import random

BASE_URL = "http://localhost:5001/api/v1"

def create_survey():
    """
    Creates a new survey and returns the response.
    """
    survey_data = {
        "title": "Personal assessment",
        "description": "Help us improve my self awareness",
        "questions": [
            {
                "text": "How trustworthy am I?",
                "response_type": "scale",
                "response_scale_max": 5,
                "creator_answer": 4
            },
            {
                "text": "Am I honest most of the times?",
                "response_type": "boolean",
                "creator_answer": True
            },
            {
                "text": "Do I take feedback with open arms?",
                "response_type": "scale",
                "response_scale_max": 10,
                "creator_answer": 8
            },
            {
                "text": "Am I approachable?",
                "response_type": "boolean",
                "creator_answer": False
            }
        ]
    }

    response = requests.post(f"{BASE_URL}/surveys", json=survey_data)
    print("Survey Creation Response:")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def add_answers(survey_id):
    """
    Adds a set of random answers for the given survey ID and returns the response.
    """
    answers = [
        {"question_id": 1, "answer": random.randint(1, 5)},
        {"question_id": 2, "answer": random.choice([True, False])},
        {"question_id": 3, "answer": random.randint(1, 10)},
        {"question_id": 4, "answer": random.choice([True, False])}
    ]

    response = requests.post(f"{BASE_URL}/surveys/{survey_id}/answers", json={"answers": answers})
    print(f"Answer Submission Response for Survey {survey_id}:")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def show_stats(survey_id, user_code):
    """
    Retrieves and displays statistics for the given survey ID and user code.
    """
    response = requests.get(f"{BASE_URL}/surveys/{survey_id}/results?user_code={user_code}")
    print(f"Statistics for Survey {survey_id} (User Code: {user_code}):")
    print(json.dumps(response.json(), indent=2))
    return response.json()

if __name__ == "__main__":
    # Create a new survey
    survey = create_survey()
    survey_id = survey['survey_id']
    creator_code = survey['user_code']

    # Add some random answers
    for _ in range(10):
        answer_response = add_answers(survey_id)

    # Show stats for creator
    creator_stats = show_stats(survey_id, creator_code)

    # Show stats for a participant (using the user_code from the last answer submission)
    print("Last participants stats")
    participant_code = answer_response['user_code']
    participant_stats = show_stats(survey_id, participant_code)
    print(participant_stats)
    
    print("Creator stats")
    creator_stats = show_stats(survey_id, creator_code)
    print(creator_stats)