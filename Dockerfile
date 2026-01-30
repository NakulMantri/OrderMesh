FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir confluent-kafka

# Copy application code
COPY common/ ./common/
COPY producer/ ./producer/
COPY services/ ./services/

ENV PYTHONPATH=/app
ENV KAFKA_BOOTSTRAP_SERVERS=kafka:9092

# Default command can be overridden by docker-compose
CMD ["python", "producer/producer.py"]
