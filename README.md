# Percept API

Percept is a web application designed to help individuals improve their self-awareness by collecting anonymous feedback from their peers. This repository contains the backend API implemented using Flask and MongoDB.

## Features

- Create surveys with customizable questions
- Collect anonymous responses
- Calculate deviations and aggregated results
- Export survey data

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- MongoDB

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/codevalley/percept.git
   cd percept
   ```

2. Set up a virtual environment (optional but recommended):
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up MongoDB:
   - Install MongoDB on your system if you haven't already
   - Start the MongoDB service:
     ```
     brew services start mongodb-community  # On macOS with Homebrew
     # or
     sudo systemctl start mongod  # On most Linux systems
     ```

5. Create a `.env` file in the project root and add your MongoDB URI:
   ```
   MONGO_URI=mongodb://localhost:27017/percept
   ```

6. Run the application:
   ```
   python app.py
   ```

The API will be available at `http://localhost:5001`.


## Using the API

Here are some example curl commands to interact with the API:

Note for Windows users: These commands are designed to work in Git Bash. If you're using Windows Command Prompt or PowerShell, you may need to adjust the quotes or use a different method to send JSON data.

1. Create a new survey:
   ```bash
   curl -X POST http://localhost:5001/api/v1/surveys \
        -H "Content-Type: application/json" \
        -d '{
          "title": "My Survey",
          "questions": [
            {
              "text": "How do you feel?",
              "response_type": "scale",
              "response_scale_max": 5,
              "creator_answer": 4
            }
          ]
        }'
   ```
   Response:
   ```json
   {
     "survey_id": 1719295638748,
     "share_link": "/surveys/1719295638748",
     "user_code": 1719295638749,
     "questions": [
       {"id": 1, "text": "How do you feel?"}
     ]
   }
   ```

2. Retrieve a survey (replace {survey_id} with the ID from the create response):
   ```bash
   curl -X GET http://localhost:5001/api/v1/surveys/{survey_id}
   ```

3. Submit answers to a survey:
   ```bash
   curl -X POST http://localhost:5001/api/v1/surveys/{survey_id}/answers \
        -H "Content-Type: application/json" \
        -d '{
          "answers": [
            {
              "question_id": 1,
              "answer": 4
            }
          ]
        }'
   ```

Replace `{survey_id}` with the actual survey ID from your created survey.


## API Endpoints

For detailed API documentation, refer to the [API_ENDPOINTS.md](API_ENDPOINTS.md) file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.