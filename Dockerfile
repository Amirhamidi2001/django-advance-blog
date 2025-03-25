# Use the official Python runtime image
FROM python:3.10

# Set the working directory to the project root
WORKDIR /app

# Set environment variables 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Copy requirements.txt to install dependencies
COPY requirements.txt /app/

# Upgrade pip and install dependencies
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Run Django’s development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
