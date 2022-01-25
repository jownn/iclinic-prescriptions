# Pull base image
FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

RUN pip install pipenv
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system --dev

COPY . /app/

EXPOSE 8000