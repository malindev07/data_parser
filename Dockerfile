FROM python:3.12
LABEL authors="Vladimir"
WORKDIR /app
COPY workers /app/workers
COPY /api /app/api
COPY requirements.txt .
COPY main.py .
COPY logger.py .
COPY db /app/db
RUN pip install -r requirements.txt

CMD uvicorn main:app --host=0.0.0.0 --port=8000
