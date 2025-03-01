FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 9007

CMD ["python", "main.py"]