# Use an official Python image as the base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Copy the .env file (make sure it's not in .dockerignore)
COPY .env .env

# Initialize the SQLite database using reset.sh
RUN chmod +x db/reset.sh && ./db/reset.sh

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI application with `fastapi dev main.py`
CMD ["fastapi", "run", "main.py"]
