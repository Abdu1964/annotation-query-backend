FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

ARG APP_PORT

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/public

EXPOSE $APP_PORT

CMD uvicorn app.main:socket_app --host 0.0.0.0 --port $APP_PORT
