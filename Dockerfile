# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.6.9

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
RUN echo "Before installing requirements"
COPY requirements.txt .
RUN echo "Installing requirements"
RUN python -m pip install -r requirements.txt
RUN echo "After installing requirements"

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
#USER root

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["sh", "run.sh"]