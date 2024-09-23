
FROM python:3.11.4

WORKDIR /app

COPY requirements.txt .

# # Install build dependencies
# RUN apk add --no-cache gcc musl-dev g++ libffi-dev cmake make

RUN pip install -r requirements.txt

COPY . /app

CMD ["streamlit", "run", "app.py"]