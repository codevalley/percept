# Percept API

Percept is a web application designed to help individuals improve their self-awareness by collecting anonymous feedback from their peers. This repository contains the backend API implemented using Flask and MongoDB.

## Features

- Create surveys with customizable questions
- Collect anonymous responses
- Calculate deviations and aggregated results
- Export survey data

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/codevalley/percept.git
   cd percept
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up MongoDB:
   - Install MongoDB on your system
   - Start the MongoDB service

4. Run the application:
   ```
   python app.py
   ```

The API will be available at `http://localhost:5001`.

## API Endpoints

- `POST /api/v1/surveys`: Create a new survey
- `GET /api/v1/surveys/{survey_id}`: Retrieve a specific survey
- `POST /api/v1/surveys/{survey_id}/answers`: Submit answers to a survey

For detailed API documentation, refer to the [API_ENDPOINTS.md](API_ENDPOINTS.md) file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.