FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

CMD if [ "$FLASK_ENV" = "Prod" ]; then gunicorn -w 4 main:app; else python main.py; fi
