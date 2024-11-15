# Use an official Python image as the base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies, including SQLite
RUN apt-get update && apt-get install -y sqlite3 && apt-get clean

# Copy requirements and install dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .


# Initialize the SQLite database directly in the Dockerfile
RUN rm -f db/hackaton.db && \
    sqlite3 db/hackaton.db < db/migrations/001_create_tables.sql && \
    sqlite3 db/hackaton.db < db/migrations/002_insert_sample_data.sql && \
    echo "Database has been initialized."

# Expose the port FastAPI will run on
EXPOSE 8000
# Run the FastAPI application with `fastapi dev main.py`
CMD ["fastapi", "run", "main.py"]
