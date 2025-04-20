FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY src/ ./src/

# Set environment variables
ENV PYTHONPATH=/app
ENV TWITCH_SERVER=irc.chat.twitch.tv
ENV TWITCH_PORT=6667
ENV MONGODB_HOST=mongodb
ENV MONGODB_PORT=27017
ENV MONGODB_DATABASE=twitch

# The channel name will be passed as an environment variable when running the container
CMD ["python", "-m", "src.bot"] 