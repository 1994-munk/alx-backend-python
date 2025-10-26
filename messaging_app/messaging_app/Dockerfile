# Use an official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy dependency file and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
