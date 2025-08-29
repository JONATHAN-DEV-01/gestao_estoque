
FROM python:3.11-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY run.py .
COPY src ./src


EXPOSE 5000

CMD ["gunicorn", "--bind=0.0.0.0:5000", "run:app"]