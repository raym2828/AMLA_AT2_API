FROM python:3.11.4-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --timeout=120

COPY . /app

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0"]