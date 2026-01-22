FROM python:3.13-alpine

# Set working directory
WORKDIR /app

# Install curl for health checks and scheduled tasks
RUN apk add --no-cache curl

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY utils/ ./utils/

# Environment variables will be provided by Coolify
ENV PYTHONUNBUFFERED=1

# Expose Flask port
EXPOSE 8000

# Run with Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "300", "app:app"]
