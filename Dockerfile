FROM python:3.11-slim
LABEL maintainer="Tanima Mishra"
LABEL project="Expense Tracker - DevOps Portfolio"
LABEL version="1.0.0"
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
