# OrderMesh: Distributed Order Processing System

OrderMesh is a production-grade, resume-ready distributed order processing system built with **Apache Kafka (KRaft mode)** and **Python**. It demonstrates a robust event-driven microservices architecture designed for high throughput, fault tolerance, and observability.

## 🚀 Key Features

- **Event-Driven Architecture**: Uses Kafka as the central nervous system for asynchronous message passing between services.
- **Microservices Design**: Includes specialized services for Order Tracking, Inventory Management, and Real-time Analytics.
- **High Throughput**: Capable of processing **~1000 orders/sec** (~86M orders/day) on local hardware.
- **Kafka KRaft Mode**: Modern Kafka deployment without the dependency on Zookeeper.
- **At-Least-Once Delivery**: Implements manual offset commits in the Inventory Service to ensure no message is lost.
- **Dead Letter Queue (DLQ)**: Automatically routes failed orders or malformed messages to a separate topic for debugging and recovery.
- **Horizontal Scalability**: Topics configured with multiple partitions (6 for orders) to support consumer scaling and rebalancing.
- **Containerized Implementation**: Fully orchestrated using Docker Compose for easy deployment and simulation.

## 🏗 System Architecture

The system consists of the following components:

1.  **Order Producer**: Simulates high-volume order traffic.
2.  **Order Tracker**: Monitors the lifecycle and status of every order.
3.  **Inventory Service**: Validates stock availability, uses manual commits, and routes to DLQ on failure.
4.  **Analytics Service**: Computes real-time metrics (TPS, total volume) without impacting business logic.
5.  **DLQ Logger**: Dedicated consumer for monitoring and logging system failures.

## 🛠 Tech Stack

- **Language**: Python 3.11
- **Messaging**: Apache Kafka (Confluent cp-kafka:7.8.6)
- **Kafka Client**: `confluent-kafka` (Python)
- **Orchestration**: Docker, Docker Compose
- **Serialization**: JSON

## 🏃 Getting Started

### Prerequisites
- Docker & Docker Desktop
- Python 3.11+ (for local development)

### Setup & Run
1.  Clone the repository:
    ```bash
    git clone https://github.com/NakulMantri/OrderMesh.git
    cd OrderMesh
    ```
2.  Run the system simulation:
    ```bash
    ./scripts/simulate_test.sh
    ```
    This script initializes the Kafka cluster, creates topics, builds and starts all microservices, and runs a failure simulation.

3.  Monitor logs:
    ```bash
    docker-compose logs -f
    ```

## 📊 Verification & Metrics

During load testing, the **Analytics Service** reported the following performance:
- **Baseline Throughput**: ~990 - 1000 messages/second.
- **Rebalancing**: Verified by stopping/starting consumer instances; Kafka successfully redistributed partitions across the remaining healthy members of the consumer group.
- **DLQ Recovery**: Failed inventory checks are immediately visible in the `dlq-logger` logs.

### Proof of Work: Live System Logs
The logs below demonstrate the system catching inventory validation failures and automatically routing them to the Dead Letter Queue for observability:

```text
inventory-1   | 2026-01-30 06:18:42,038 - __main__ - ERROR - Inventory validation failed for order 54ab231c-37bb-4ca2-9342-3f896ec41492, routing to DLQ
dlq-logger-1  | 2026-01-30 06:18:42,038 - __main__ - CRITICAL - DLQ ALERT: Received failed order event: {'order_id': '54ab231c-37bb-4ca2-9342-3f896ec41492', 'user_id': 'user_941', 'items': [{'product_id': 'prod_7', 'quantity': 2}], 'total_amount': 343.04, 'timestamp': 1769753922.0145404, 'failure_reason': 'OUT_OF_STOCK_SIMULATED'}
inventory-1   | 2026-01-30 06:18:42,039 - __main__ - ERROR - Inventory validation failed for order 55aaa9c0-7a53-47e5-8f84-c02130783740, routing to DLQ
dlq-logger-1  | 2026-01-30 06:18:42,039 - __main__ - CRITICAL - DLQ ALERT: Received failed order event: {'order_id': '55aaa9c0-7a53-47e5-8f84-c02130783740', 'user_id': 'user_666', 'items': [{'product_id': 'prod_35', 'quantity': 1}], 'total_amount': 171.04, 'timestamp': 1769753922.0136235, 'failure_reason': 'OUT_OF_STOCK_SIMULATED'}
inventory-1   | 2026-01-30 06:18:44,076 - __main__ - ERROR - Inventory validation failed for order 38e39a5c-007a-438f-b3ce-33868df75401, routing to DLQ
dlq-logger-1  | 2026-01-30 06:18:44,076 - __main__ - CRITICAL - DLQ ALERT: Received failed order event: {'order_id': '38e39a5c-007a-438f-b3ce-33868df75401', 'user_id': 'user_797', 'items': [{'product_id': 'prod_89', 'quantity': 1}], 'total_amount': 195.14, 'timestamp': 1769753924.050372, 'failure_reason': 'OUT_OF_STOCK_SIMULATED'}
```

## 📜 License
This project is for educational and portfolio purposes.
