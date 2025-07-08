# Use official Python 3.10 base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.enableCORS=false"]
