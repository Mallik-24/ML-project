# Base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the necessary files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the Flask server will run
EXPOSE 5000

# Set the entrypoint command
ENTRYPOINT ["python", "server.py"]

