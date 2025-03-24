FROM python:3.9-slim

WORKDIR /app
COPY . /app/
COPY .env /app/.env
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
