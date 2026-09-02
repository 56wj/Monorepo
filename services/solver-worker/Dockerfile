FROM docker.1ms.run/library/python:3.8.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 9108
CMD ["python", "worker.py"]
