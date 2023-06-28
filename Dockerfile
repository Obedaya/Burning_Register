# Use a Python base image
FROM python:3.9-slim

# Set environment variables
ENV MONGO_PASSWORD="your_mongo_password"
ENV MONGO_URL="your_mongo_url"
ENV MONGO_DATABASE_NAME="your_mongo_database_name"
ENV PREAUTHMAIL="your_preauthmail"
ENV ADMINUSERS="your_adminusers"

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose the port for Streamlit app
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false", "Home.py"]
