# Use a lightweight Python 3.9 image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency file (requirements.txt) first
COPY requirements.txt .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . .

# Expose port 80 for Elastic Beanstalk
EXPOSE 80

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=80", "--server.address=0.0.0.0"]

