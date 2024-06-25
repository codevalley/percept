# Percept API Endpoints

## Base URL: `/api/v1`

### 1. Create Survey

- **Endpoint**: `POST /surveys`
- **Description**: Create a new survey
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string (optional)",
    "questions": [
      {
        "text": "string",
        "response_type": "string",
        "response_scale_max": "integer (required for 'scale' type)",
        "creator_answer": "integer or boolean"
      }
    ]
  }
  ```
- **Response**:
  ```json
  {
    "survey_id": "long",
    "share_link": "string",
    "user_code": "long",
    "questions": [
      {
        "id": "integer",
        "text": "string"
      }
    ]
  }
  ```

### 2. Get Survey

- **Endpoint**: `GET /surveys/{survey_id}`
- **Description**: Retrieve survey details
- **Response**:
  ```json
  {
    "title": "string",
    "description": "string",
    "questions": [
      {
        "id": "integer",
        "text": "string",
        "response_type": "string",
        "response_scale_max": "integer (only for 'scale' type)"
      }
    ]
  }
  ```

### 3. Submit Survey Answers

- **Endpoint**: `POST /surveys/{survey_id}/answers`
- **Description**: Submit answers for a survey
- **Request Body**:
  ```json
  {
    "answers": [
      {
        "question_id": "integer",
        "answer": "integer or boolean"
      }
    ]
  }
  ```
- **Response**:
  ```json
  {
    "user_code": "long",
    "deviation_from_creator": "float",
    "deviation_from_others": "float",
    "overall_deviation": "float"
  }
  ```

## Notes

- Question IDs are simple integers starting from 1 for each survey.
- The `response_type` can be "scale" or "boolean".
- For "scale" type questions, `response_scale_max` specifies the maximum value of the scale.
- The server returns appropriate HTTP status codes (200 for success, 201 for creation, 400 for bad request, 404 for not found, etc.)
- Error responses include a message explaining the error.