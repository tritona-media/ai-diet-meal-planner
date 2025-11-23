# Base image
FROM python:3.12-slim

# Set the working directory to /app
WORKDIR /app

# Copy requirements.txt from the project root
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the contents of the 'src' folder into /app/src
COPY ["src/", "src"]

# Expose the port
EXPOSE 8000

# Run the application (main.py is now directly inside /app)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]