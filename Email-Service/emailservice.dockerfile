# Use the official Python base image
FROM python:3-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY ./emailservice_requirements.txt ./EmailService.py ./confirmEmailTemplate.html ./
# Install the Python dependencies
RUN python -m pip install --no-cache-dir -r emailservice_requirements.txt

# Set the command to run the application
CMD ["python", "EmailService.py"]

