FROM python:3.13-alpine

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py nottage_client.py shopify_client.py sync_manager.py ./

# Use environment variables for configuration
ENV PYTHONUNBUFFERED=1

# Run the sync script
CMD ["python", "main.py"]
