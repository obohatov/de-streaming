FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Установка netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]
