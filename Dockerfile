FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]