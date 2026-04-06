# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the app code and the openenv.yaml file into the container
COPY ./app /code/app
COPY ./openenv.yaml /code/openenv.yaml

# Expose port 7860 (Hugging Face Spaces requirement)
EXPOSE 7860

# Command to run the FastAPI server on the required port
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]