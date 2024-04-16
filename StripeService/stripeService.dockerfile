# Use an official Python runtime as the base image
FROM python:3-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY stripeService_requirements.txt ./

# Install the Python dependencies
RUN python -m pip install --no-cache-dir -r stripeService_requirements.txt

COPY ./stripeService.py .

CMD [ "python", "stripeService.py" ]