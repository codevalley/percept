# app.py

from statistics import StatisticsError, mean, stdev
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from petname import generate
import os
import logging
from id_manager import IDManager

from snowflake import Snowflake53


app = Flask(__name__)

# Add the CORS configuration here
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

# Initialize the generator with a random number 
snowflake = Snowflake53(1,1)

# Constants
MINIMUM_RESPONSES = 5
ID_SUGGESTIONS = 5
INITIAL_ID_RESERVE = 100  # Number of IDs to generate initially
# Set up logging
logging.basicConfig(level=logging.DEBUG)

# MongoDB configuration
if app.testing:
    app.config["MONGO_URI"] = "mongodb://localhost:27017/backfeed_test"
else:
    app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost:27017/percept")
mongo = PyMongo(app)

# Initialize IDManager
id_manager = IDManager(mongo.db)

def generate_unique_id():
    return snowflake.generate()

# Initialize the ID reserve
with app.app_context():
    id_manager.initialize_reserve(INITIAL_ID_RESERVE)
    app.logger.info(f"Initialized ID reserve with {INITIAL_ID_RESERVE} IDs")

@app.route('/')
def home():
    return "Welcome to the Percept API", 200

@app.route('/api/v1/ids/check', methods=['GET'])
def check_id():
    id_to_check = request.args.get('id')
    if not id_to_check:
        return jsonify({'error': 'No ID provided'}), 400

    available = id_manager.is_id_available(id_to_check)
    return jsonify({
        'id': id_to_check,
        'available': available
    })

@app.route('/api/v1/ids', methods=['GET'])
def get_ids():
    preferred = request.args.get('id')
    count = int(request.args.get('count', ID_SUGGESTIONS))

    ids = id_manager.get_ids(count, preferred)

    return jsonify({
        'ids': ids
    })
       
@app.route('/api/v1/surveys', methods=['POST'])
def create_survey():
    app.logger.debug("Received POST request to /api/v1/surveys")
    data = request.json
    app.logger.debug(f"Request data: {data}")
    
    if not data or 'title' not in data or 'questions' not in data:
        app.logger.warning("Invalid request data")
        return jsonify({'error': 'Invalid request data'}), 400
    
    try:
        survey_id = id_manager.get_id()
        user_code = id_manager.get_id()
        survey = {
            'survey_id': survey_id,
            'title': data['title'],
            'description': data.get('description', ''),
            'questions': [
                {
                    'id': i + 1,
                    'text': q['text'],
                    'response_type': q['response_type'],
                    'response_scale_max': q.get('response_scale_max', MINIMUM_RESPONSES),
                    'creator_answer': q['creator_answer']
                } for i, q in enumerate(data['questions'])
            ],
            'user_code': user_code
        }
        result = mongo.db.surveys.insert_one(survey)
        app.logger.debug(f"Survey created with ID: {survey_id}")
        
        # Mark the IDs as used
        id_manager.mark_id_as_used(survey_id)
        id_manager.mark_id_as_used(user_code)
        
        response = jsonify({
            'survey_id': survey_id,
            'share_link': f"/surveys/{survey_id}",
            'user_code': user_code,
            'questions': [{'id': q['id'], 'text': q['text']} for q in survey['questions']]
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

@app.route('/api/v1/surveys/<string:survey_id>/answers', methods=['POST'])
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
        user_code = id_manager.get_id()
        answer_submission = {
            'survey_id': survey_id,
            'user_code': user_code,
            'answers': {str(answer['question_id']): answer['answer'] for answer in data['answers']},
            'submitted_at': snowflake.generate()
        }
        result = mongo.db.answers.insert_one(answer_submission)
        
        # Mark the user_code as used
        id_manager.mark_id_as_used(user_code)
        
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
    
    # Try to find the survey based on the user_code (for creators)
    survey = mongo.db.surveys.find_one({'user_code': int(user_code)})
    if survey:
        return process_results(survey['survey_id'], user_code)
    
    # If not found in surveys, look in answers (for participants)
    answer = mongo.db.answers.find_one({'user_code': int(user_code)})
    if answer:
        return process_results(answer['survey_id'], user_code)
    
    return jsonify({'error': 'No survey found for this user code'}), 404
    
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
    
    current_responses = len(answers)
    # Check for minimum responses for creator
    if current_responses < MINIMUM_RESPONSES:
        if is_creator:
            response = {
                'status': 'incomplete',
                'current_responses': current_responses,
                'minimum_responses': MINIMUM_RESPONSES,
                'remaining_responses': MINIMUM_RESPONSES - current_responses,
                'is_creator': True
            }
        else:
            response = {
                'status': 'incomplete',
                'is_creator': False
            }
        
        return jsonify(response), 202

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