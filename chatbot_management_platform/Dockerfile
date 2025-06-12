# backend/Dockerfile
FROM python:3.9-slim

# 安装必要的系统工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the backend code
COPY .. /

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the backend port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]