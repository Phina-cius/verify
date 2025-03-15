# Use the official Python slim image as the base
FROM python:3.13.0-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libzbar0 \  # Install the zbar shared library
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy and install Python dependencies
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the application code
COPY . /app

# Expose the port your app runs on
EXPOSE 8000

# Start the application with Gunicorn
ENTRYPOINT ["gunicorn", "core.wsgi", "-b", "0.0.0.0:8000"]