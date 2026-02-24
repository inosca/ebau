FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir flask requests gunicorn

COPY app.py .

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
