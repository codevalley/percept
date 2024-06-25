# app.py

from statistics import StatisticsError, mean, stdev
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import time
import os
import logging

app = Flask(__name__)

# Constants
MINIMUM_RESPONSES = 5

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# MongoDB configuration
if app.testing:
    app.config["MONGO_URI"] = "mongodb://localhost:27017/backfeed_test"
else:
    app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost:27017/percept")
mongo = PyMongo(app)

def generate_unique_id():
    return int(time.time() * 1000)

@app.route('/')
def home():
    return "Welcome to the Percept API", 200

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
                    'id': i + 1,  # Simple incrementing ID
                    'text': q['text'],
                    'response_type': q['response_type'],
                    'response_scale_max': q.get('response_scale_max'),
                    'creator_answer': q['creator_answer']
                } for i, q in enumerate(data['questions'])
            ],
            'user_code': generate_unique_id()
        }
        result = mongo.db.surveys.insert_one(survey)
        app.logger.debug(f"Survey created with ID: {survey['survey_id']}")
        
        response = jsonify({
            'survey_id': survey['survey_id'],
            'share_link': f"/surveys/{survey['survey_id']}",
            'user_code': survey['user_code'],
            'questions': [{'id': q['id'], 'text': q['text']} for q in survey['questions']]  # Return question IDs
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

@app.route('/api/v1/surveys/<int:survey_id>/answers', methods=['POST'])
def submit_answers(survey_id):
    app.logger.debug(f"Received POST request to submit answers for survey ID: {survey_id}")
    data = request.json
    app.logger.debug(f"Request data: {data}")
    
    if not data or 'answers' not in data:
        app.logger.warning("Invalid request data")
        return jsonify({'error': 'Invalid request data'}), 400
    
    try:
        # Fetch the survey
        survey = mongo.db.surveys.find_one({'survey_id': survey_id})
        if not survey:
            return jsonify({'error': 'Survey not found'}), 404
        
        # Validate answers
        valid_question_ids = {q['id'] for q in survey['questions']}
        for answer in data['answers']:
            if answer['question_id'] not in valid_question_ids:
                return jsonify({'error': f"Invalid question ID: {answer['question_id']}"}), 400
        
        # Store the answers
        user_code = generate_unique_id()  # Generate a new user_code for each submission
        answer_submission = {
            'survey_id': survey_id,
            'user_code': user_code,  # Store the user_code explicitly
            'answers': {str(answer['question_id']): answer['answer'] for answer in data['answers']},  # Store answers as a dictionary
            'submitted_at': generate_unique_id()
        }
        result = mongo.db.answers.insert_one(answer_submission)
        
        # Calculate deviations (placeholder logic - you'll need to implement the actual calculation)
        deviation_from_creator = 0.5  # placeholder
        deviation_from_others = 0.3  # placeholder
        overall_deviation = 0.4  # placeholder
        
        response = jsonify({
            'user_code': user_code,  # Return the new user_code to the client
            'deviation_from_creator': deviation_from_creator,
            'deviation_from_others': deviation_from_others,
            'overall_deviation': overall_deviation
        })
        app.logger.debug(f"Sending response: {response.get_data(as_text=True)}")
        return response, 201
    except Exception as e:
        app.logger.error(f"Error submitting answers: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    
@app.route('/api/v1/surveys/<int:survey_id>/results', methods=['GET'])
def get_survey_results(survey_id):
    user_code = request.args.get('user_code')
    if not user_code:
        return jsonify({'error': 'User code is required'}), 400

    survey = mongo.db.surveys.find_one({'survey_id': survey_id})
    if not survey:
        return jsonify({'error': 'Survey not found'}), 404

    # Check if user is creator
    is_creator = (int(user_code) == survey['user_code'])

    # Get all answers for this survey
    answers = list(mongo.db.answers.find({'survey_id': survey_id}))

    # Check for minimum responses for creator
    if is_creator and len(answers) < MINIMUM_RESPONSES:
        return jsonify({'error': 'Insufficient data'}), 400

    # Calculate statistics
    results = calculate_survey_statistics(survey, answers, int(user_code), is_creator)

    return jsonify(results), 200

def calculate_survey_statistics(survey, answers, user_code, is_creator):
    questions = {q['id']: q for q in survey['questions']}
    results = {
        'survey_id': survey['survey_id'],
        'title': survey['title'],
        'description': survey.get('description', ''),
        'created_at': survey['survey_id'],  # Using survey_id as a timestamp
        'user_type': 'creator' if is_creator else 'participant',
        'questions': [],
        'overall_statistics': {}
    }

    if is_creator:
        results['total_responses'] = len(answers)

    question_stats = {}
    user_answers = next((a for a in answers if str(a.get('user_code')) == str(user_code)), None)

    for q_id, question in questions.items():
        q_answers = [a['answers'][str(q_id)] for a in answers if str(q_id) in a['answers']]
        
        if question['response_type'] == 'scale':
            try:
                avg_score = mean(q_answers) if q_answers else 0
                std_dev = stdev(q_answers) if len(q_answers) > 1 else 0
            except StatisticsError:
                avg_score = 0
                std_dev = 0
            
            q_stat = {
                'id': q_id,
                'text': question['text'],
                'type': 'scale',
                'scale_max': question['response_scale_max'],
                'average_score': round(avg_score, 2),
                'standard_deviation': round(std_dev, 2)
            }
            
            if is_creator:
                q_stat['distribution'] = {score: q_answers.count(score) for score in range(1, question['response_scale_max'] + 1)}
            
            if user_answers and str(q_id) in user_answers['answers']:
                user_score = user_answers['answers'][str(q_id)]
                q_stat['user_score'] = user_score
                q_stat['user_deviation'] = round(abs(user_score - avg_score), 2)
            
        elif question['response_type'] == 'boolean':
            true_count = sum(q_answers)
            total_count = len(q_answers)
            
            q_stat = {
                'id': q_id,
                'text': question['text'],
                'type': 'boolean',
                'true_percentage': round(true_count / total_count * 100, 2) if total_count > 0 else 0,
                'false_percentage': round((total_count - true_count) / total_count * 100, 2) if total_count > 0 else 0
            }
            
            if user_answers and str(q_id) in user_answers['answers']:
                q_stat['user_answer'] = user_answers['answers'][str(q_id)]

        results['questions'].append(q_stat)
        question_stats[q_id] = q_stat

    # Calculate overall statistics
    scale_questions = [q for q in results['questions'] if q['type'] == 'scale']
    if scale_questions:
        user_deviations = [q['user_deviation'] for q in scale_questions if 'user_deviation' in q]
        results['overall_statistics'] = {
            'average_deviation_from_aggregate': round(mean(user_deviations), 2) if user_deviations else 0,
            'highest_rated_question': max(scale_questions, key=lambda q: q['average_score']),
            'lowest_rated_question': min(scale_questions, key=lambda q: q['average_score']),
            'highest_deviation_question': max(scale_questions, key=lambda q: q['standard_deviation']),
            'lowest_deviation_question': min(scale_questions, key=lambda q: q['standard_deviation'])
        }

    return results


    questions = {q['id']: q for q in survey['questions']}
    results = {
        'survey_id': survey['survey_id'],
        'title': survey['title'],
        'description': survey.get('description', ''),
        'created_at': survey['survey_id'],  # Using survey_id as a timestamp
        'user_type': 'creator' if is_creator else 'participant',
        'questions': [],
        'overall_statistics': {}
    }

    if is_creator:
        results['total_responses'] = len(answers)

    question_stats = {}
    user_answers = next((a for a in answers if a.get('user_code') == user_code), None)

    for q_id, question in questions.items():
        q_answers = [a['answers'][str(q_id)] for a in answers if str(q_id) in a['answers']]
        
        if question['response_type'] == 'scale':
            try:
                avg_score = mean(q_answers) if q_answers else 0
                std_dev = stdev(q_answers) if len(q_answers) > 1 else 0
            except StatisticsError:
                avg_score = 0
                std_dev = 0
            
            q_stat = {
                'id': q_id,
                'text': question['text'],
                'type': 'scale',
                'scale_max': question['response_scale_max'],
                'average_score': round(avg_score, 2),
                'standard_deviation': round(std_dev, 2)
            }
            
            if is_creator:
                q_stat['distribution'] = {score: q_answers.count(score) for score in range(1, question['response_scale_max'] + 1)}
            
            if user_answers and str(q_id) in user_answers['answers']:
                user_score = user_answers['answers'][str(q_id)]
                q_stat['user_score'] = user_score
                q_stat['user_deviation'] = round(abs(user_score - avg_score), 2)
            
        elif question['response_type'] == 'boolean':
            true_count = sum(q_answers)
            total_count = len(q_answers)
            
            q_stat = {
                'id': q_id,
                'text': question['text'],
                'type': 'boolean',
                'true_percentage': round(true_count / total_count * 100, 2) if total_count > 0 else 0,
                'false_percentage': round((total_count - true_count) / total_count * 100, 2) if total_count > 0 else 0
            }
            
            if user_answers and str(q_id) in user_answers['answers']:
                q_stat['user_answer'] = user_answers['answers'][str(q_id)]

        results['questions'].append(q_stat)
        question_stats[q_id] = q_stat

    # Calculate overall statistics
    scale_questions = [q for q in results['questions'] if q['type'] == 'scale']
    if scale_questions:
        user_deviations = [q['user_deviation'] for q in scale_questions if 'user_deviation' in q]
        results['overall_statistics'] = {
            'average_deviation_from_aggregate': round(mean(user_deviations), 2) if user_deviations else 0,
            'highest_rated_question': max(scale_questions, key=lambda q: q['average_score']),
            'lowest_rated_question': min(scale_questions, key=lambda q: q['average_score']),
            'highest_deviation_question': max(scale_questions, key=lambda q: q['standard_deviation']),
            'lowest_deviation_question': min(scale_questions, key=lambda q: q['standard_deviation'])
        }

    return results

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