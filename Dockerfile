FROM python:3.13-alpine

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY nottage_client.py .
COPY shopify_client.py .
COPY sync_manager.py .

# Environment variables will be provided by Coolify
ENV PYTHONUNBUFFERED=1

# Run the sync script
CMD ["python", "main.py"]
