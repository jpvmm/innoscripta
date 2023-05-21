FROM python:3.9-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add metadata to the image to describe that the container is listening on port 8885
EXPOSE 8885

# Copy the current directory (src/) contents into the container at /app
COPY src/ /app
COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#COPY secrets
COPY .env /app

# Run the command to start uvicorn server for FastAPI
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8885"]