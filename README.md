[![codecov](https://codecov.io/gh/codevalley/percept/branch/main/graph/badge.svg?token=YOUR_CODECOV_TOKEN)](https://codecov.io/gh/codevalley/percept)
# Backwave

Backwave is a web application designed to help individuals improve their self-awareness by collecting anonymous feedback from their peers. This repository contains both the backend API implemented using Flask and MongoDB, and the frontend implemented in Vue.js.

## Features

- Create surveys with customizable questions
- Collect anonymous responses
- Calculate deviations and aggregated results
- Export survey data

## Prerequisites

- Docker
- Docker Compose

## Setup and Running the Application

1. Clone the repository:
   ```
   git clone https://github.com/codevalley/percept.git
   cd percept
   ```

2. Create a `.env` file in the project root and add your MongoDB URI:
   ```
   MONGO_URI=mongodb://mongo:27017/percept
   ```

3. Build and start the Docker containers:
   ```
   docker-compose up --build
   ```

   This command will build the images for the backend, frontend, and set up the MongoDB database. It will then start all the services.

4. The application will be available at:
   - Frontend: http://localhost
   - Backend API: http://localhost/api

## Development Workflow

### Making Changes

1. Backend changes:
   - Modify the Flask app files as needed.
   - Rebuild and restart the containers:
     ```
     docker-compose down
     docker-compose up --build
     ```

2. Frontend changes:
   - Modify the Vue.js app files in the `webapp` directory.
   - Rebuild and restart the containers:
     ```
     docker-compose down
     docker-compose up --build
     ```

3. To run the containers in detached mode:
   ```
   docker-compose up -d
   ```

4. To view logs:
   ```
   docker-compose logs
   ```
   Or for a specific service:
   ```
   docker-compose logs backend
   ```

### Running Tests

To run the unit tests:

```
docker-compose run --rm backend python -m unittest test_survey_results.py
```

## Using the API

Here are some example curl commands to interact with the API:

1. Create a new survey:
   ```bash
   curl -X POST http://localhost/api/v1/surveys \
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
   curl -X GET http://localhost/api/v1/surveys/{survey_id}
   ```

3. Submit answers to a survey:
   ```bash
   curl -X POST http://localhost/api/v1/surveys/{survey_id}/answers \
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

For detailed API documentation, refer to the [api_endpoints.md](api_endpoints.md) file.

## Setting up Environment Variables in DigitalOcean App Platform

After creating your app in DigitalOcean App Platform:

1. Go to the App Platform dashboard and select your app.
2. Click on the "Settings" tab.
3. Scroll down to the "Environment Variables" section.
4. Click "Edit" and then "Add Variable".
5. Add a new variable:
   - Key: MONGO_URI
   - Value: Your MongoDB connection string (e.g., mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority)
6. Click "Save".

The ${backend.INTERNAL_URL} and ${backend.PORT} variables are automatically set by DigitalOcean App Platform, so you don't need to configure them manually.

## Troubleshooting

1. If you encounter CORS issues:
   - Check the CORS configuration in `app.py` and ensure it matches your frontend URL.
   - Verify that the Nginx configuration in `nginx.conf` is correctly set up to handle CORS headers.

2. If services fail to start:
   - Check the Docker logs for each service:
     ```
     docker-compose logs [service_name]
     ```
   - Ensure all required environment variables are set in the `.env` file.

3. If changes are not reflecting:
   - Ensure you've rebuilt the Docker images after making changes:
     ```
     docker-compose down
     docker-compose up --build
     ```

4. If you're experiencing database connection issues:
   - Verify that the MongoDB container is running:
     ```
     docker-compose ps
     ```
   - Check the MongoDB logs:
     ```
     docker-compose logs mongo
     ```
   - Ensure the `MONGO_URI` in the `.env` file is correct.

5. To reset the entire setup:
   ```
   docker-compose down -v
   docker-compose up --build
   ```
   Note: This will remove all data in the MongoDB volume.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
