# Use a FastAPI-optimized base image with Uvicorn & Gunicorn
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (optional, place before pip to cache better)
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app code
COPY . .

# Expose port used by FastAPI
EXPOSE 7860

# No CMD needed — tiangolo image runs `uvicorn` by default
