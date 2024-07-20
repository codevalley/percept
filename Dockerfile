# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download NLTK data files
RUN python -m nltk.downloader words vader_lexicon wordnet

# Copy the rest of the application code
COPY . .

# Expose port 5001 and specify the command to run the app
EXPOSE 5001
CMD ["gunicorn", "-b", "0.0.0.0:5001", "app:app"]
