FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY planning_agent ./planning_agent
COPY knowledge ./knowledge
EXPOSE 8200
CMD ["uvicorn", "planning_agent.api:app", "--host", "0.0.0.0", "--port", "8200"]
