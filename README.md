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

## 📜 License
This project is for educational and portfolio purposes.
