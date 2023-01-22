FROM python:3.9-slim
ENV PYTHONBUFFERED True
EXPOSE 8080
WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
COPY transactions_dashboard.py .
RUN pip3 install -r requirements.txt
ENTRYPOINT ["streamlit", "run", "transactions_dashboard.py", "--server.port=8080", "--server.address=0.0.0.0"]