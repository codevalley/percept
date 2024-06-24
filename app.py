# app.py

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import time
import os
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# MongoDB configuration
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost:27017/backfeed")
mongo = PyMongo(app)

def generate_unique_id():
    return int(time.time() * 1000)

@app.route('/')
def home():
    return "Welcome to the Backfeed API", 200

@app.route('/api/v1/surveys', methods=['POST'])
def create_survey():
    app.logger.debug("Received POST request to /api/v1/surveys")
    data = request.json
    app.logger.debug(f"Request data: {data}")
    
    if not data or 'title' not in data or 'questions' not in data:
        app.logger.warning("Invalid request data")
        return jsonify({'error': 'Invalid request data'}), 400
    
    try:
        survey = {
            'survey_id': generate_unique_id(),
            'title': data['title'],
            'description': data.get('description', ''),
            'questions': [
                {
                    'id': generate_unique_id(),
                    'text': q['text'],
                    'response_type': q['response_type'],
                    'response_scale_max': q.get('response_scale_max'),
                    'creator_answer': q['creator_answer']
                } for q in data['questions']
            ],
            'user_code': generate_unique_id()
        }
        result = mongo.db.surveys.insert_one(survey)
        app.logger.debug(f"Survey created with ID: {survey['survey_id']}")
        
        response = jsonify({
            'survey_id': survey['survey_id'],
            'share_link': f"/surveys/{survey['survey_id']}",
            'user_code': survey['user_code']
        })
        app.logger.debug(f"Sending response: {response.get_data(as_text=True)}")
        return response, 201
    except Exception as e:
        app.logger.error(f"Error creating survey: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/v1/surveys/<int:survey_id>', methods=['GET'])
def get_survey(survey_id):
    app.logger.debug(f"Received GET request for survey ID: {survey_id}")
    survey = mongo.db.surveys.find_one({'survey_id': survey_id})
    if not survey:
        app.logger.warning(f"Survey not found: {survey_id}")
        return jsonify({'error': 'Survey not found'}), 404
    
    app.logger.debug(f"Found survey: {survey}")
    return jsonify({
        'title': survey['title'],
        'description': survey.get('description', ''),
        'questions': [
            {
                'id': q['id'],
                'text': q['text'],
                'response_type': q['response_type'],
                'response_scale_max': q.get('response_scale_max')
            } for q in survey['questions']
        ]
    })
    
@app.errorhandler(404)
def not_found(error):
    app.logger.warning(f"404 error: {request.url}")
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"500 error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.logger.info("Starting the Flask application")
    app.logger.info(f"Registered routes: {app.url_map}")
    app.run(debug=True, host='0.0.0.0', port=5001)