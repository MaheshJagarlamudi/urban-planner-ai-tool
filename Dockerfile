    # Use an official Python runtime as a parent image
    FROM python:3.11-slim

    # Set the working directory in the container
    WORKDIR /code

    # Copy the requirements file into the container
    COPY ./requirements.txt /code/requirements.txt

    # Install any needed packages specified in requirements.txt
    RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

    # Copy the rest of your application code into the container
    COPY . /code/

    # Run your app.py when the container launches
    # Hugging Face Spaces expect the app to run on port 7860
    CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]