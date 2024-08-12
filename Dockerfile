# 1. Use a base image
FROM python:3.12-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app/src

# 4. Copy the requirements file to the container
COPY requirements.txt /app/

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# 6. Copy the entire project into the container
COPY src/ /app/src/

# 7. Expose the port FastAPI will run on
EXPOSE 8000

# 8. Command to run the FastAPI app with Gunicorn and Uvicorn workers
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000", "--workers", "4"]