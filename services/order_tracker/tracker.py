import logging
import time
from confluent_kafka import Consumer, KafkaError
from common.kafka_utils import get_kafka_config, json_deserializer

logger = logging.getLogger(__name__)

def run_tracker():
    conf = get_kafka_config({
        'group.id': 'order-tracker-group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True
    })

    consumer = Consumer(conf)
    consumer.subscribe(['orders'])

    logger.info("Order Tracker Service started...")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logger.error(f"Consumer error: {msg.error()}")
                    break

            order = json_deserializer(msg.value())
            if order:
                # In a real system, this would update a database
                # For this demo, we'll log summary every 1000 orders
                pass

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_tracker()
