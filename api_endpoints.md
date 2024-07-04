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
        "response_scale_max": "integer (optional, default is 5)",
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

### 4. Get Survey Results by Survey ID

- **Endpoint**: `GET /surveys/{survey_id}/results`
- **Description**: Retrieve survey results for a specific survey
- **Query Parameters**:
  - `user_code`: "long" (required)
- **Response**:
  ```json
  {
    "survey_id": "long",
    "title": "string",
    "description": "string",
    "created_at": "long",
    "user_type": "string",
    "questions": [
      {
        "id": "integer",
        "text": "string",
        "type": "string",
        "scale_max": "integer (for scale questions)",
        "average_score": "float (for scale questions)",
        "standard_deviation": "float (for scale questions)",
        "user_score": "integer or boolean (if applicable)",
        "user_deviation": "float (for scale questions, if applicable)",
        "true_percentage": "float (for boolean questions)",
        "false_percentage": "float (for boolean questions)"
      }
    ],
    "overall_statistics": {
      "average_deviation_from_aggregate": "float",
      "deviation_from_creator": "float (for participants)",
      "deviation_from_others": "float (for participants)",
      "overall_deviation": "float"
    }
  }
  ```

### 5. Get Survey Results by User Code

- **Endpoint**: `GET /surveys/results`
- **Description**: Retrieve survey results for a user across all surveys
- **Query Parameters**:
  - `user_code`: "long" (required)
- **Response**: Same as "Get Survey Results by Survey ID"

## Notes

- Question IDs are simple integers starting from 1 for each survey.
- The `response_type` can be "scale" or "boolean".
- For "scale" type questions, `response_scale_max` specifies the maximum value of the scale. If not provided, it defaults to 5.
- The server returns appropriate HTTP status codes (200 for success, 201 for creation, 400 for bad request, 404 for not found, etc.)
- Error responses include a message explaining the error.
- The `user_type` in the results can be either "creator" or "participant".
- For the creator, some statistics like `deviation_from_creator` are not applicable and may be omitted from the response.