import logging
from confluent_kafka import Consumer, KafkaError
from common.kafka_utils import get_kafka_config, json_deserializer

logger = logging.getLogger(__name__)

def run_dlq_consumer():
    conf = get_kafka_config({
        'group.id': 'dlq-logger-group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True
    })

    consumer = Consumer(conf)
    consumer.subscribe(['orders-dlq'])

    logger.info("DLQ Logger Service started. Monitoring 'orders-dlq' topic...")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                logger.error(f"DLQ Consumer error: {msg.error()}")
                continue

            failed_event = json_deserializer(msg.value())
            logger.critical(f"DLQ ALERT: Received failed order event: {failed_event}")

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_dlq_consumer()
