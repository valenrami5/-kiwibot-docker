FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
COPY kiwibot_test.py ./
COPY .env ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "kiwibot_test.py"]