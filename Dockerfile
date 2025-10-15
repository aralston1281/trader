# Dockerfile for Options Bot
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY options_bot/ ./options_bot/
COPY config/ ./config/
COPY setup.py .
COPY README.md .

# Install the package
RUN pip install -e .

# Create data and logs directories
RUN mkdir -p data logs

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the scheduler by default
CMD ["python", "-m", "options_bot.runner.scheduler"]

