# Use an official Python base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy only requirements file for dependency install
COPY requirements.txt ./

# Install dependencies using uv
RUN pip install -r requirements.txt

# Install curl
RUN apt-get update && apt-get install -y curl

# Copy the rest of the code
COPY . .

# Expose the default FastAPI port
EXPOSE 8000

# Command for production (overridden by docker-compose for dev)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
