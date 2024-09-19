FROM python:3.8-slim

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY . .

RUN pip install -r /app/requirements.txt

CMD ["python", "main.py"]