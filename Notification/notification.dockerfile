# Use the official Python base image
FROM python:3-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY ./notification_requirements.txt ./Notification.py  ./
# Install the Python dependencies
RUN python -m pip install --no-cache-dir -r notification_requirements.txt

# Set the command to run the application
CMD ["python", "Notification.py"]
