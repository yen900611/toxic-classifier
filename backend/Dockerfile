# 1. Base Image: Use a lightweight Python version
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy dependencies first (for better caching)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code
# This copies your 'app' folder (with the .pkl model) into the container
COPY . .

# 6. Expose the port (FastAPI defaults to 8000)
EXPOSE 8000

# 7. Command to run the application
# Note: 0.0.0.0 is required for Docker to listen outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]