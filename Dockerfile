<<<<<<< HEAD
# Stage 1: Build dependencies
FROM python:3.6.9 as builder
=======
# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster
>>>>>>> parent of fec9be0 (fix)

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Stage 2: Runtime image
FROM python:3.6.9

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.6/site-packages/ /usr/local/lib/python3.6/site-packages/
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER root

# During debugging, this entry point will be overridden.
CMD ["sh", "run.sh"]
