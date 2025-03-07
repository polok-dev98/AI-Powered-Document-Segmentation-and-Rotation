# Use Python 3.10.14 slim version as the base image
FROM python:3.10.14-slim

# Set the working directory inside the container
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port your Flask app runs on (default is 5000)
EXPOSE 5001

# Set the command to run the application
CMD ["python", "app.py"]
