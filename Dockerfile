FROM python:3.13.0-slim-bullseye

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies and upgrade pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --upgrade pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

# Copy application code
COPY . /app

# Start the application with Gunicorn
ENTRYPOINT ["gunicorn", "core.wsgi", "-b", "0.0.0.0:8000"]
