# Base image
FROM python:3.10-slim

# setting the working directory
WORKDIR /app

# copy all the files into containers
COPY . .

# Installing dependencies
RUN pip install flask

# copy application code into container
COPY . .

# Exposing port
EXPOSE 5001

# command to run the app
CMD ["python", "app.py"]

