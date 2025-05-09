FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/fineparticlesmanagement

COPY docker/backend/src/requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install -r /requirements.txt

COPY app /app

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]