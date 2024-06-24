# setup_db.py

from pymongo import MongoClient
import time

def generate_unique_id():
    return int(time.time() * 1000)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['backfeed']

# Clear existing data
db.surveys.delete_many({})

# Insert a sample survey
sample_survey = {
    'survey_id': generate_unique_id(),
    'title': 'Sample Feedback Survey',
    'description': 'A sample survey for testing purposes',
    'questions': [
        {
            'id': generate_unique_id(),
            'text': 'How would you rate your overall experience?',
            'response_type': 'scale',
            'response_scale_max': 5,
            'creator_answer': 4
        },
        {
            'id': generate_unique_id(),
            'text': 'Did you find the service helpful?',
            'response_type': 'boolean',
            'creator_answer': True
        }
    ],
    'user_code': generate_unique_id()
}

result = db.surveys.insert_one(sample_survey)

print(f"Sample survey inserted with ID: {result.inserted_id}")
print(f"Survey ID: {sample_survey['survey_id']}")
print(f"User Code: {sample_survey['user_code']}")

client.close()