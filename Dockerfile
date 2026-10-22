# Use a lightweight official Python image to reduce attack surface
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY src/ ./src/

# Security Sandbox: Create a non-root user and logs directory
RUN useradd -m honeypot_user && \
    mkdir -p logs && \
    chown -R honeypot_user:honeypot_user /app

# Switch to the restricted user
USER honeypot_user

# Expose the port the honeypot will listen on
EXPOSE 8080

# Command to execute the sensor
CMD ["python", "-u", "src/app.py"]