FROM python:3.11-slim

WORKDIR /service

COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt gunicorn

COPY app ./app
COPY backend ./backend

ENV PYTHONUNBUFFERED=1 \
    PADDLE_OCR_DEVICE=cpu \
    APP_RUNTIME_DIR=/service/.runtime_home

WORKDIR /service/backend
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--timeout", "180", "app:app"]
