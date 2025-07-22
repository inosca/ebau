FROM python:3.10-slim

WORKDIR /app

COPY app.py .

RUN pip install flask

EXPOSE 9000

ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=9000"]
