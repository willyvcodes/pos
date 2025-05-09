#!/bin/bash

# Start the FastAPI application in the background
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Wait for the application to start
sleep 5

# Run the seed script
python scripts/seed_products.py

# Keep the container running
wait 