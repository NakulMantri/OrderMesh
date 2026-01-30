import logging
import time
from confluent_kafka import Consumer, KafkaError
from common.kafka_utils import get_kafka_config, json_deserializer

logger = logging.getLogger(__name__)

class MetricsCalculator:
    def __init__(self):
        self.total_orders = 0
        self.start_time = time.time()
        self.last_report_time = time.time()
        self.last_report_count = 0

    def record_order(self):
        self.total_orders += 1
        
    def report(self):
        now = time.time()
        if now - self.last_report_time >= 5.0:  # Report every 5 seconds
            elapsed = now - self.last_report_time
            count = self.total_orders - self.last_report_count
            throughput = count / elapsed
            total_elapsed = now - self.start_time
            avg_throughput = self.total_orders / total_elapsed
            
            logger.info(f"METRICS: Total={self.total_orders}, Recent TPS={throughput:.2f}, Avg TPS={avg_throughput:.2f}")
            
            self.last_report_time = now
            self.last_report_count = self.total_orders

def run_analytics():
    conf = get_kafka_config({
        'group.id': 'analytics-group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True,
        'fetch.min.bytes': 100000,
        'linger.ms': 100
    })

    consumer = Consumer(conf)
    consumer.subscribe(['orders'])
    metrics = MetricsCalculator()

    logger.info("Analytics Service started...")

    try:
        while True:
            msg = consumer.poll(0.1)
            if msg is None:
                metrics.report()
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logger.error(f"Consumer error: {msg.error()}")
                    break

            metrics.record_order()
            metrics.report()

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_analytics()
