# Use an official Python runtime as the base image
FROM python:3-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./createAuction_requirements.txt ./amqp_connection.py ./createAuction.py ./

# Install the Python dependencies
RUN python -m pip install --no-cache-dir -r createAuction_requirements.txt


# Set the command to run when the container starts
CMD ["python", "createAuction.py"]