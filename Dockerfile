# Use an official NVIDIA CUDA image with Python as the base.
# This includes all the necessary GPU libraries inside the container.
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# Install Python and set up the application environment
RUN apt-get update && \
    apt-get install -y python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
