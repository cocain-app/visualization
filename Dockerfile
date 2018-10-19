FROM python:3
ENV PYTHONUNBUFFERED 1

# Create directory for app
RUN mkdir /app/
WORKDIR /app/

# Install python dependencies
ADD requirements.txt /app/
RUN pip install -r requirements.txt

# Add files
ADD . /app/

# Open port
EXPOSE 5000

# Run script
SHELL ["/bin/bash", "-c"]
CMD source database.secret.env && flask run --host=0.0.0.0
