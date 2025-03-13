# Use the official Python image with version 3.8+
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt