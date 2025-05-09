FROM node:16-alpine

WORKDIR /app

# Copy frontend files and build
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm install

COPY frontend/ ./frontend/
RUN cd frontend && npm run build

# Install Python and dependencies
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files (which now includes the built frontend in site/build)
COPY backend/ .

# Make the startup script executable
RUN chmod +x start.sh

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application and seed script
CMD ["./start.sh"]