import time
import uuid
import random
import logging
from confluent_kafka import Producer
from common.kafka_utils import get_kafka_config, json_serializer

logger = logging.getLogger(__name__)

def delivery_report(err, msg):
    if err is not None:
        logger.error(f'Message delivery failed: {err}')
    # For high throughput, we don't log every success here

def generate_order():
    return {
        'order_id': str(uuid.uuid4()),
        'user_id': f'user_{random.randint(1, 1000)}',
        'items': [
            {'product_id': f'prod_{random.randint(1, 100)}', 'quantity': random.randint(1, 5)}
        ],
        'total_amount': round(random.uniform(10.0, 500.0), 2),
        'timestamp': time.time()
    }

def run_producer(topic='orders', messages_per_second=1000):
    conf = get_kafka_config({
        'client.id': 'order-producer',
        'queue.buffering.max.messages': 1000000,
        'linger.ms': 10,
        'batch.size': 64 * 1024,
        'compression.type': 'snappy'
    })
    
    producer = Producer(conf)
    logger.info(f"Starting producer, sending to topic: {topic}")

    count = 0
    start_time = time.time()
    
    try:
        while True:
            order = generate_order()
            producer.produce(
                topic, 
                key=order['order_id'], 
                value=json_serializer(order), 
                callback=delivery_report
            )
            count += 1
            
            # Poll for delivery reports
            if count % 1000 == 0:
                producer.poll(0)
                elapsed = time.time() - start_time
                if elapsed > 0:
                    logger.info(f"Sent {count} messages. Current rate: {count/elapsed:.2f} msg/sec")

            # Simple throttling to stay around the target rate
            # In a real stress test, we might remove this
            if count % messages_per_second == 0:
                time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Producer stopping...")
    finally:
        producer.flush()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_producer()
