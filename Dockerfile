FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install wget for the wait-for script
RUN apt-get update && apt-get install -y wget

# Download wait-for script
RUN wget -O /usr/local/bin/wait-for https://raw.githubusercontent.com/eficode/wait-for/master/wait-for
RUN chmod +x /usr/local/bin/wait-for

# Pre-download NLTK data files
# -d option may have other consequences. testing for now
RUN python -m nltk.downloader -d /workspace/nltk_data words vader_lexicon wordnet

# Copy the rest of the application code
COPY . .

# Expose port 5001
EXPOSE 5001
CMD ["gunicorn", "-b", "0.0.0.0:5001","--timeout", "240", "app:app"]
