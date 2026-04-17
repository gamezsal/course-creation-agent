FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir slowapi # Ensure our new rate-limiting lib is here

COPY . .

# Run the ADK app. Cloud Run injects the PORT env var automatically.
CMD ["python", "adk_app.py", ".", "--host", "0.0.0.0"]