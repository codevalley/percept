# app.py

from statistics import StatisticsError, mean, stdev
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import time
import os
import logging

app = Flask(__name__)

# Add the CORS configuration here
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})


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
                    'response_scale_max': q.get('response_scale_max', MINIMUM_RESPONSES),  # Default value added
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
        app.logger.warning("Invalid request data: 'answers' not found in request")
        return jsonify({'error': 'Invalid request data: answers not provided'}), 400
    
    try:
        # Fetch the survey
        survey = mongo.db.surveys.find_one({'survey_id': survey_id})
        if not survey:
            app.logger.warning(f"Survey not found: {survey_id}")
            return jsonify({'error': 'Survey not found'}), 404
        
        # Validate answers
        valid_questions = {q['id']: q for q in survey['questions']}
        for answer in data['answers']:
            if 'question_id' not in answer or 'answer' not in answer:
                app.logger.warning(f"Invalid answer format: {answer}")
                return jsonify({'error': f"Invalid answer format: {answer}"}), 400
            
            if answer['question_id'] not in valid_questions:
                app.logger.warning(f"Invalid question ID: {answer['question_id']}")
                return jsonify({'error': f"Invalid question ID: {answer['question_id']}"}), 400
            
            question = valid_questions[answer['question_id']]
            if question['response_type'] == 'scale':
                if not isinstance(answer['answer'], (int, float)) or not (1 <= answer['answer'] <= question['response_scale_max']):
                    app.logger.warning(f"Invalid answer for scale question {answer['question_id']}: {answer['answer']}")
                    return jsonify({'error': f"Invalid answer for question {answer['question_id']}: must be between 1 and {question['response_scale_max']}"}), 400
            elif question['response_type'] == 'boolean':
                if not isinstance(answer['answer'], bool):
                    app.logger.warning(f"Invalid answer for boolean question {answer['question_id']}: {answer['answer']}")
                    return jsonify({'error': f"Invalid answer for question {answer['question_id']}: must be a boolean"}), 400
        
        # Store the answers
        user_code = generate_unique_id()  # Generate a new user_code for each submission
        answer_submission = {
            'survey_id': survey_id,
            'user_code': user_code,
            'answers': {str(answer['question_id']): answer['answer'] for answer in data['answers']},
            'submitted_at': generate_unique_id()
        }
        result = mongo.db.answers.insert_one(answer_submission)
        
        # Calculate deviations (placeholder logic - you'll need to implement the actual calculation)
        deviation_from_creator = 0.5  # placeholder
        deviation_from_others = 0.3  # placeholder
        overall_deviation = 0.4  # placeholder
        
        response = jsonify({
            'user_code': user_code,
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
    return process_results(survey_id, user_code)

@app.route('/api/v1/surveys/results', methods=['GET'])
def get_results_by_user_code():
    user_code = request.args.get('user_code')
    if not user_code:
        return jsonify({'error': 'User code is required'}), 400
    
    # Find the survey_id based on the user_code
    answer = mongo.db.answers.find_one({'user_code': int(user_code)})
    if not answer:
        return jsonify({'error': 'No survey found for this user code'}), 404
    
    survey_id = answer['survey_id']
    return process_results(survey_id, user_code)

def process_results(survey_id, user_code):
    logging.info(f"Getting results for survey {survey_id}, user_code {user_code}")
    
    if not user_code:
        logging.warning("User code is missing")
        return jsonify({'error': 'User code is required'}), 400

    survey = mongo.db.surveys.find_one({'survey_id': survey_id})
    if not survey:
        logging.warning(f"Survey {survey_id} not found")
        return jsonify({'error': 'Survey not found'}), 404

    # Check if user is creator
    is_creator = (int(user_code) == survey['user_code'])
    logging.info(f"User is creator: {is_creator}")

    # Get all answers for this survey
    answers = list(mongo.db.answers.find({'survey_id': survey_id}))
    logging.info(f"Found {len(answers)} answers for survey {survey_id}")

    # Check if the user_code exists in the answers
    user_answer = next((a for a in answers if a['user_code'] == int(user_code)), None)
    if not user_answer and not is_creator:
        logging.warning(f"Invalid user code: {user_code}")
        return jsonify({'error': 'Invalid user code'}), 404

    logging.info(f"Creator ID is: {survey['user_code']}")
    
    # Check for minimum responses for creator
    if is_creator and len(answers) < MINIMUM_RESPONSES:
        logging.warning(f"Insufficient data for creator. Only {len(answers)} responses.")
        return jsonify({'error': 'Insufficient data'}), 400

    # Calculate statistics
    results = calculate_survey_statistics(survey, answers, int(user_code), is_creator)

    return jsonify(results), 200

def calculate_survey_statistics(survey, answers, user_code, is_creator):
    logging.info(f"Calculating statistics for survey {survey['survey_id']}, user_code {user_code}, is_creator: {is_creator}")
    
    questions = {q['id']: q for q in survey['questions']}
    results = {
        'survey_id': survey['survey_id'],
        'title': survey['title'],
        'description': survey.get('description', ''),
        'created_at': survey['survey_id'],
        'user_type': 'creator' if is_creator else 'participant',
        'questions': [],
        'overall_statistics': {}
    }

    if is_creator:
        results['total_responses'] = len(answers)

    user_answers = next((a for a in answers if str(a.get('user_code')) == str(user_code)), None)
    creator_answers = {q['id']: q['creator_answer'] for q in survey['questions']}

    logging.info(f"User answers: {user_answers}")
    logging.info(f"Creator answers: {creator_answers}")

    all_deviations = []
    user_deviations = []
    creator_deviations = []

    for q_id, question in questions.items():
        q_answers = [a['answers'][str(q_id)] for a in answers if str(q_id) in a['answers']]
        creator_answer = creator_answers.get(q_id)
        
        if question['response_type'] == 'scale':
            try:
                avg_score = mean(q_answers) if q_answers else creator_answer
                std_dev = stdev(q_answers) if len(q_answers) > 1 else 0
            except StatisticsError:
                avg_score = creator_answer
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
                user_deviation = abs(user_score - avg_score)
                q_stat['user_deviation'] = round(user_deviation, 2)
                user_deviations.append(user_deviation)

                if creator_answer is not None:
                    creator_deviation = abs(user_score - creator_answer)
                    creator_deviations.append(creator_deviation)

            # Calculate deviations for all answers from creator's answer
            if creator_answer is not None:
                all_deviations.extend([abs(ans - creator_answer) for ans in q_answers])
            
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

    # Calculate overall statistics
    if user_deviations or all_deviations:
        results['overall_statistics']['average_deviation_from_aggregate'] = round(mean(user_deviations or all_deviations), 2)
        logging.info(f"Average deviation from aggregate: {results['overall_statistics']['average_deviation_from_aggregate']}")

    if not is_creator and creator_deviations:
        results['overall_statistics']['deviation_from_creator'] = round(mean(creator_deviations), 2)
        logging.info(f"Deviation from creator: {results['overall_statistics']['deviation_from_creator']}")

    if user_answers and len(answers) > 1:
        other_deviations = [
            abs(mean([a['answers'][str(q_id)] for a in answers if str(q_id) in a['answers'] and a != user_answers]) - user_answers['answers'][str(q_id)])
            for q_id in questions if questions[q_id]['response_type'] == 'scale'
        ]
        results['overall_statistics']['deviation_from_others'] = round(mean(other_deviations), 2)
        logging.info(f"Deviation from others: {results['overall_statistics']['deviation_from_others']}")

    if is_creator:
        if all_deviations:
            results['overall_statistics']['overall_deviation'] = round(mean(all_deviations), 2)
            logging.info(f"Overall deviation (creator): {results['overall_statistics']['overall_deviation']}")
    else:
        if 'deviation_from_creator' in results['overall_statistics'] and 'deviation_from_others' in results['overall_statistics']:
            results['overall_statistics']['overall_deviation'] = round(
                (results['overall_statistics']['deviation_from_creator'] + results['overall_statistics']['deviation_from_others']) / 2,
                2
            )
            logging.info(f"Overall deviation (participant): {results['overall_statistics']['overall_deviation']}")

    logging.info(f"Final results: {results}")
    return results

    logging.info(f"Calculating statistics for survey {survey['survey_id']}, user_code {user_code}, is_creator: {is_creator}")
    
    questions = {q['id']: q for q in survey['questions']}
    results = {
        'survey_id': survey['survey_id'],
        'title': survey['title'],
        'description': survey.get('description', ''),
        'created_at': survey['survey_id'],
        'user_type': 'creator' if is_creator else 'participant',
        'questions': [],
        'overall_statistics': {}
    }

    if is_creator:
        results['total_responses'] = len(answers)

    user_answers = next((a for a in answers if str(a.get('user_code')) == str(user_code)), None)
    creator_answers = {q['id']: q['creator_answer'] for q in survey['questions']}  # Get creator answers from survey

    logging.info(f"User answers: {user_answers}")
    logging.info(f"Creator answers: {creator_answers}")

    user_deviations = []
    creator_deviations = []
    all_deviations = []

    for q_id, question in questions.items():
        q_answers = [a['answers'][str(q_id)] for a in answers if str(q_id) in a['answers']]
        creator_answer = creator_answers.get(q_id)
        
        if question['response_type'] == 'scale':
            try:
                avg_score = mean(q_answers) if q_answers else creator_answer
                std_dev = stdev(q_answers) if len(q_answers) > 1 else 0
            except StatisticsError:
                avg_score = creator_answer
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
                user_deviation = abs(user_score - avg_score)
                q_stat['user_deviation'] = round(user_deviation, 2)
                user_deviations.append(user_deviation)

                if creator_answer is not None:
                    creator_deviation = abs(user_score - creator_answer)
                    creator_deviations.append(creator_deviation)

            # Calculate deviations for all answers from creator's answer
            if creator_answer is not None:
                all_deviations.extend([abs(ans - creator_answer) for ans in q_answers])
            
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

     # Calculate overall statistics
    if user_deviations:
        results['overall_statistics']['average_deviation_from_aggregate'] = round(mean(user_deviations), 2)
        logging.info(f"Average deviation from aggregate: {results['overall_statistics']['average_deviation_from_aggregate']}")

    if not is_creator and creator_deviations:
        results['overall_statistics']['deviation_from_creator'] = round(mean(creator_deviations), 2)
        logging.info(f"Deviation from creator: {results['overall_statistics']['deviation_from_creator']}")
    
    if user_deviations and len(answers) > 1:
        other_deviations = [
            abs(mean([a['answers'][str(q_id)] for a in answers if str(q_id) in a['answers'] and a != user_answers]) - user_answers['answers'][str(q_id)])
            for q_id in questions if questions[q_id]['response_type'] == 'scale'
        ]
        results['overall_statistics']['deviation_from_others'] = round(mean(other_deviations), 2)
        logging.info(f"Deviation from others: {results['overall_statistics']['deviation_from_others']}")

    if is_creator:
        if all_deviations:
            results['overall_statistics']['overall_deviation'] = round(mean(all_deviations), 2)
            logging.info(f"Overall deviation (creator): {results['overall_statistics']['overall_deviation']}")
    else:
        if 'deviation_from_creator' in results['overall_statistics'] and 'deviation_from_others' in results['overall_statistics']:
            results['overall_statistics']['overall_deviation'] = round(
                (results['overall_statistics']['deviation_from_creator'] + results['overall_statistics']['deviation_from_others']) / 2,
                2
            )
            logging.info(f"Overall deviation (participant): {results['overall_statistics']['overall_deviation']}")

    logging.info(f"Final results: {results}")
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