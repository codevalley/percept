# app.py

import datetime
from statistics import StatisticsError, mean, stdev
import time
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import os
import logging
from id_manager import IDManager
from pymongo.errors import ConnectionFailure
from snowflake import Snowflake53


app = Flask(__name__)

# Add the CORS configuration here
allowed_origins = [
    "http://localhost",
    "http://localhost:8080",
    os.environ.get("APP_URL", "https://i.nyn.me")
]
CORS(app, resources={
    r"/v1/*": {"origins": allowed_origins},
    r"/api/v1/*": {"origins": allowed_origins}
})
#CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

api_prefix = os.getenv('API_PREFIX', '')  # Default to empty string if not set

# Initialize the generator with a random number 
snowflake = Snowflake53(1,1)

# Constants
MINIMUM_RESPONSES = 5
ID_SUGGESTIONS = 5
INITIAL_ID_RESERVE = 50  # Number of IDs to generate initially
DEFAULT_EXPIRY = datetime.timedelta(days=5)  # New constant for default expiry
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

def make_tz_aware(dt):
    if isinstance(dt, str):
        dt = datetime.datetime.fromisoformat(dt)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=datetime.UTC)
    return dt


def initialize_db(max_retries=5, delay=5):
    for attempt in range(max_retries):
        try:
            # The ismaster command is cheap and does not require auth.
            mongo.db.command('ismaster')
            logging.info("Successfully connected to MongoDB")
            return True
        except ConnectionFailure:
            if attempt < max_retries - 1:
                logging.error(f"Failed to connect to MongoDB. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error("Failed to connect to MongoDB after maximum retries")
                return False


def generate_unique_id():
    return snowflake.generate()

# Initialize the ID reserve
with app.app_context():
    if initialize_db():
        try:
            id_manager.initialize_reserve(INITIAL_ID_RESERVE)
            app.logger.info(f"Initialized ID reserve with {INITIAL_ID_RESERVE} IDs")
        except Exception as e:
            app.logger.error(f"Failed to initialize ID reserve: {str(e)}")
    else:
        app.logger.error("Failed to initialize database connection")

@app.before_first_request
def startup_logger():
    app.logger.info("Application started. Testing MongoDB connection...")
    try:
        # Perform a simple operation to test the connection
        mongo.db.command('ping')
        app.logger.info("MongoDB connection successful")
    except Exception as e:
        app.logger.error(f"MongoDB connection failed: {str(e)}")

@app.route(f'{api_prefix}/')
def home():
    return "Welcome to the Percept API", 200

def get_participant_bucket(count):
    if count < 10:
        return "< 10"
    elif 10 <= count < 100:
        return "10-100"
    elif 100 <= count < 1000:
        return "100-1000"
    else:
        return "1000+"

@app.route(f'{api_prefix}/v1/ids/check', methods=['GET'])
def check_id():
    id_to_check = request.args.get('id')
    if not id_to_check:
        return jsonify({'error': 'No ID provided'}), 400

    if not id_manager.is_valid_id_format(id_to_check):
        return jsonify({
            'id': id_to_check,
            'available': False,
            'error': 'Invalid ID format. ID must be at least 5 characters long and contain only letters, numbers, and hyphens.'
        }), 400

    available = id_manager.is_id_available(id_to_check)
    return jsonify({
        'id': id_to_check,
        'available': available
    })
    
@app.route(f'{api_prefix}/v1/ids', methods=['GET'])
def get_ids():
    preferred = request.args.get('id')
    count = int(request.args.get('count', ID_SUGGESTIONS))

    ids = id_manager.get_ids(count, preferred)

    return jsonify({
        'ids': ids
    })
       
@app.route(f'{api_prefix}/v1/surveys', methods=['POST'])
def create_survey():
    app.logger.debug("Received POST request to /api/v1/surveys")
    data = request.json
    app.logger.debug(f"Request data: {data}")
    if 'survey_id' not in data :
        data['survey_id'] = id_manager.get_ids()[0]
        app.logger.debug("Creating surveryID: "+data['survey_id'])
    
    if 'user_code' not in data :
        data['user_code'] = id_manager.get_ids()[0]
        app.logger.debug("Creating userCode: "+data['user_code'])

    if not data or 'title' not in data or 'questions' not in data or 'user_code' not in data:
        app.logger.warning("Invalid request data")
        return jsonify({'error': 'Invalid request data'}), 400
    
    try:
        survey_id = data['survey_id']
        user_code = data['user_code']
    
        # Check if the IDs are available
        if not id_manager.is_id_available(survey_id):
            app.logger.warning(f"Requested survey ID is not available: survey_id={survey_id}")
            return jsonify({'error': 'Requested survey ID is not available'}), 400
        
        if not id_manager.is_id_available(user_code):
            app.logger.warning(f"Requested user code is not available: user_code={user_code}")
            return jsonify({'error': 'Requested user code is not available'}), 400

        # Handle expiry date
        expiry_date = data.get('expiry')
        if expiry_date:
            expiry_date = make_tz_aware(datetime.datetime.fromisoformat(expiry_date))
        else:
            expiry_date = make_tz_aware(datetime.datetime.now(datetime.UTC) + DEFAULT_EXPIRY)

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
            'user_code': user_code,
            'expiry_date': expiry_date
        }
        
        # Insert the survey into the database
        result = mongo.db.surveys.insert_one(survey)
        
        if result.inserted_id:
            app.logger.debug(f"Survey created with ID: {survey_id}")
            
            # Mark the IDs as used only after successful insertion
            id_manager.mark_id_as_used(survey_id)
            id_manager.mark_id_as_used(user_code)
            
            response = jsonify({
                'survey_id': survey_id,
                'share_link': f"/participate/{survey_id}",
                'user_code': user_code,
                'questions': [{'id': q['id'], 'text': q['text']} for q in survey['questions']],
                'expiry_date': expiry_date.isoformat()
            })
            app.logger.debug(f"Sending response: {response.get_data(as_text=True)}")
            return response, 201
        else:
            app.logger.error("Failed to insert survey into database")
            return jsonify({'error': 'Failed to create survey'}), 500
    
    except Exception as e:
        app.logger.error(f"Error creating survey: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route(f'{api_prefix}/v1/surveys/<string:survey_id>', methods=['GET'])
def get_survey(survey_id):
    app.logger.debug(f"Received GET request for survey ID: {survey_id}")
    survey = mongo.db.surveys.find_one({'survey_id': survey_id})
    if not survey:
        app.logger.warning(f"Survey not found: {survey_id}")
        return jsonify({'error': 'Survey not found'}), 404
    
    # Check if the survey has expired
    expiry_date = make_tz_aware(survey.get('expiry_date', datetime.datetime.now(datetime.UTC) + DEFAULT_EXPIRY))
    is_expired = expiry_date < datetime.datetime.now(datetime.UTC)
    
    if is_expired:
        return jsonify({'error': 'Survey has expired', 'expired': True}), 410
    
    # Remove the _id field from the survey dict
    survey.pop('_id', None)
    
    # Calculate trending status
    twenty_four_hours_ago = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=24)
    recent_answers = mongo.db.answers.find_one({
        'survey_id': survey_id,
        'submitted_at': {'$gte': twenty_four_hours_ago}
    })
    is_trending = bool(recent_answers)
    
    # Calculate participant bucket
    total_answers = mongo.db.answers.count_documents({'survey_id': survey_id})
    participant_bucket = get_participant_bucket(total_answers)
    
    app.logger.debug(f"Found survey: {survey}")
    return jsonify({
        'survey_id': survey['survey_id'],
        'title': survey['title'],
        'description': survey.get('description', ''),
        'questions': [
            {
                'id': q['id'],
                'text': q['text'],
                'response_type': q['response_type'],
                'response_scale_max': q.get('response_scale_max')
            } for q in survey['questions']
        ],
        'is_trending': is_trending,
        'participant_bucket': participant_bucket,
        'expiry_date': expiry_date.isoformat(),
        'expired': is_expired
    })

@app.route(f'{api_prefix}/v1/surveys/<string:survey_id>/answers', methods=['POST'])
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
        valid_questions = {str(q['id']): q for q in survey['questions']}  # Convert to string
        for answer in data['answers']:
            if 'question_id' not in answer or 'answer' not in answer:
                app.logger.warning(f"Invalid answer format: {answer}")
                return jsonify({'error': f"Invalid answer format: {answer}"}), 400
            
            question_id = str(answer['question_id'])  # Convert to string
            if question_id not in valid_questions:
                app.logger.warning(f"Invalid question ID: {question_id}")
                return jsonify({'error': f"Invalid question ID: {question_id}"}), 400
            
            question = valid_questions[question_id]
            if question['response_type'] == 'scale':
                if not isinstance(answer['answer'], (int, float)) or not (1 <= answer['answer'] <= question['response_scale_max']):
                    app.logger.warning(f"Invalid answer for scale question {question_id}: {answer['answer']}")
                    return jsonify({'error': f"Invalid answer for question {question_id}: must be between 1 and {question['response_scale_max']}"}), 400
            elif question['response_type'] == 'boolean':
                if not isinstance(answer['answer'], bool):
                    app.logger.warning(f"Invalid answer for boolean question {question_id}: {answer['answer']}")
                    return jsonify({'error': f"Invalid answer for question {question_id}: must be a boolean"}), 400
        
        # Use provided user_code, if not, generate a new one
        user_code = data.get('user_code', id_manager.get_id())
        answer_submission = {
            'survey_id': survey_id,
            'user_code': user_code,
            'answers': {str(answer['question_id']): answer['answer'] for answer in data['answers']},
            'submitted_at': datetime.datetime.now(datetime.UTC)
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
    
@app.route(f'{api_prefix}/v1/surveys/<string:survey_id>/results', methods=['GET'])
def get_survey_results(survey_id):
    user_code = request.args.get('user_code')
    return process_results(survey_id, user_code)

@app.route(f'{api_prefix}/v1/surveys/results', methods=['GET'])
def get_results_by_user_code():
    user_code = request.args.get('user_code')
    if not user_code:
        return jsonify({'error': 'User code is required'}), 400
    
    # Try to find the survey based on the user_code (for creators)
    survey = mongo.db.surveys.find_one({'user_code': user_code})
    if survey:
        return process_results(survey['survey_id'], user_code)
    
    # If not found in surveys, look in answers (for participants)
    answer = mongo.db.answers.find_one({'user_code': user_code})
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
    is_creator = (user_code == survey['user_code'])
    logging.info(f"User is creator: {is_creator}")

    # Get all answers for this survey
    answers = list(mongo.db.answers.find({'survey_id': survey_id}))
    logging.info(f"Found {len(answers)} answers for survey {survey_id}")

    # Check if the user_code exists in the answers
    user_answer = next((a for a in answers if a['user_code'] == user_code), None)
    if not user_answer and not is_creator:
        logging.warning(f"Invalid user code: {user_code}")
        return jsonify({'error': 'Invalid user code'}), 404

    logging.info(f"Creator ID is: {survey['user_code']}")
    
    current_responses = len(answers)
    now_time = datetime.datetime.now(datetime.UTC)
    # Calculate trending status
    twenty_four_hours_ago = now_time - datetime.timedelta(hours=24)
    recent_answers = mongo.db.answers.find_one({
        'survey_id': survey_id,
        'submitted_at': {'$gte': twenty_four_hours_ago}
    })
    
    # Calculate participant bucket
    total_answers = len(answers)
    is_trending = bool(recent_answers)
    participant_bucket = get_participant_bucket(total_answers)

    # Check expiry
    expiry_date = make_tz_aware(survey.get('expiry_date', now_time + DEFAULT_EXPIRY))
    is_expired = expiry_date < now_time

    # Check for minimum responses for creator
    if current_responses < MINIMUM_RESPONSES:
        if is_creator:
            response = {
                'status': 'incomplete',
                'current_responses': current_responses,
                'total_responses': current_responses,
                'minimum_responses': MINIMUM_RESPONSES,
                'remaining_responses': MINIMUM_RESPONSES - current_responses,
                'is_creator': True,
                'user_code': user_code,
                'survey_id': survey_id,
                'is_trending': is_trending,
                'participant_bucket': participant_bucket,
                'expiry_date': expiry_date.isoformat(),
                'expired': is_expired
            }
            return jsonify(response), 200
        else:
            response = {
                'status': 'incomplete',
                'is_creator': False,
                'is_trending': is_trending,
                'participant_bucket': participant_bucket,
                'expiry_date': expiry_date.isoformat(),
                'expired': is_expired
            }
            return jsonify(response), 202

    # Calculate statistics
    results = calculate_survey_statistics(survey, answers, user_code, is_creator)
    results['is_trending'] = is_trending
    results['participant_bucket'] = participant_bucket
    results['expiry_date'] = expiry_date.isoformat()
    results['expired'] = is_expired
    
    return jsonify(results), 200

def calculate_survey_statistics(survey, answers, user_code, is_creator):
    logging.info(f"<O>Calculating statistics for survey {survey['survey_id']}, user_code {user_code}, is_creator: {is_creator}")
    
    questions = {q['id']: q for q in survey['questions']}
    now_time = datetime.datetime.now(datetime.UTC)
    results = {
        'survey_id': survey['survey_id'],
        'title': survey['title'],
        'description': survey.get('description', ''),
        'created_at': survey['survey_id'],
        'user_type': 'creator' if is_creator else 'participant',
        'questions': [],
        'overall_statistics': {},
        'expiry_date': make_tz_aware(survey.get('expiry_date', now_time + DEFAULT_EXPIRY)).isoformat(),
        'expired': make_tz_aware(survey.get('expiry_date', now_time + DEFAULT_EXPIRY)) < now_time
    }

    if is_creator:
        results['total_responses'] = len(answers)
        user_answers = {q['id']: q['creator_answer'] for q in survey['questions']}
    else:
        user_answers = next((a['answers'] for a in answers if str(a.get('user_code')) == str(user_code)), None)

    creator_answers = {q['id']: q['creator_answer'] for q in survey['questions']}
    logging.info(f"<O>User answers: {user_answers}")
    logging.info(f"<O>Creator answers: {creator_answers}")

    all_deviations = []
    creator_deviations = []
    user_deviations = []
    other_deviations = []
    aggregate_deviations = []

    for q_id, question in questions.items():
        q_answers = [a['answers'][str(q_id)] for a in answers if str(q_id) in a['answers']]
        creator_answer = creator_answers.get(q_id)
        avg_score = mean(q_answers) if q_answers else None
        
        if question['response_type'] == 'scale':
            try:
                std_dev = stdev(q_answers) if len(q_answers) > 1 else 0
            except StatisticsError:
                std_dev = 0
            
            q_stat = {
                'id': q_id,
                'text': question['text'],
                'type': 'scale',
                'scale_max': question['response_scale_max'],
                'average_score': round(avg_score, 2) if avg_score is not None else None,
                'standard_deviation': round(std_dev, 2)
            }
            
            if is_creator:
                q_stat['distribution'] = {score: q_answers.count(score) for score in range(1, question['response_scale_max'] + 1)}
            
            if user_answers and str(q_id) in user_answers:
                user_score = user_answers[str(q_id)]
                q_stat['user_score'] = user_score
                user_deviation = abs(user_score - avg_score) if avg_score is not None else 0
                q_stat['user_deviation'] = round(user_deviation, 2)
                user_deviations.append(user_deviation)

                if creator_answer is not None:
                    creator_deviation = abs(user_score - creator_answer)
                    q_stat['deviation_from_creator'] = round(creator_deviation, 2)
                    creator_deviations.append(creator_deviation)

                # Exclude current user's answer to calculate deviation from others
                other_answers = [a for a in q_answers if a != user_score]
                if other_answers:
                    other_avg = mean(other_answers)
                    other_deviation = abs(user_score - other_avg)
                    q_stat['deviation_from_others'] = round(other_deviation, 2)
                    other_deviations.append(other_deviation)

            # Calculate deviations for all answers from creator's answer
            if creator_answer is not None:
                question_deviations = [abs(ans - creator_answer) for ans in q_answers]
                all_deviations.extend(question_deviations)
                aggregate_deviations.append(mean(question_deviations))
            
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
            
            if user_answers and str(q_id) in user_answers:
                q_stat['user_answer'] = user_answers[str(q_id)]

        results['questions'].append(q_stat)

    # Calculate overall statistics
    if user_deviations:
        results['overall_statistics']['average_deviation_from_aggregate'] = round(mean(user_deviations), 2)

    if other_deviations:
        results['overall_statistics']['average_deviation_from_others'] = round(mean(other_deviations), 2)

    if creator_deviations:
        results['overall_statistics']['average_deviation_from_creator'] = round(mean(creator_deviations), 2)

    if all_deviations:
        results['overall_statistics']['overall_deviation'] = round(mean(all_deviations), 2)

    if aggregate_deviations:
        results['overall_statistics']['average_deviation_from_aggregate'] = round(mean(aggregate_deviations), 2)

    logging.info(f"<O>Final results: {results}")
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
    app.run(debug=False, host='0.0.0.0', port=5001)