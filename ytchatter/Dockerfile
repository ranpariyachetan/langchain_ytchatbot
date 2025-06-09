# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app.py /app
COPY ./ytchatter.py /app
COPY ./requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8501

# Define environment variable for Streamlit
ENV STREAMLIT_SERVER_PORT=8501

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py"]