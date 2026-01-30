import logging
import random
import time
from confluent_kafka import Consumer, Producer, KafkaError
from common.kafka_utils import get_kafka_config, json_deserializer, json_serializer

logger = logging.getLogger(__name__)

def run_inventory():
    # Consumer config with manual commits
    consumer_conf = get_kafka_config({
        'group.id': 'inventory-group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False  # CRITICAL for manual management
    })

    # Producer for DLQ
    producer_conf = get_kafka_config({
        'client.id': 'inventory-dlq-producer'
    })

    consumer = Consumer(consumer_conf)
    dlq_producer = Producer(producer_conf)
    
    consumer.subscribe(['orders'])
    
    logger.info("Inventory Service started (Manual Offsets & DLQ implementation)...")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                logger.error(f"Consumer error: {msg.error()}")
                continue

            order = json_deserializer(msg.value())
            if not order:
                # Malformed message -> DLQ
                logger.warning(f"Malformed message at offset {msg.offset()}, sending to DLQ")
                dlq_producer.produce('orders-dlq', value=msg.value())
                consumer.commit(message=msg)
                continue

            # Simulate inventory validation logic
            # 5% chance of failure to demonstrate DLQ
            success = random.random() > 0.05
            
            if success:
                # Process the order (e.g., decrement stock)
                # ...
                
                # Commit offset ONLY after successful processing
                consumer.commit(message=msg)
            else:
                logger.error(f"Inventory validation failed for order {order['order_id']}, routing to DLQ")
                order['failure_reason'] = 'OUT_OF_STOCK_SIMULATED'
                dlq_producer.produce('orders-dlq', value=json_serializer(order))
                dlq_producer.flush()
                # Commit offset so we don't get stuck in a loop, but message is in DLQ
                consumer.commit(message=msg)

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        dlq_producer.flush()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_inventory()
