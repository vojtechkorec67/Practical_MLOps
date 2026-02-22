FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY hello.py .
COPY test_hello.py .

CMD ["python", "hello.py"]
