import json
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9094')

def get_kafka_config(extra_config=None):
    config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    }
    if extra_config:
        config.update(extra_config)
    return config

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

def json_deserializer(data):
    if data is None:
        return None
    try:
        return json.loads(data.decode('utf-8'))
    except Exception as e:
        logger.error(f"Error deserializing message: {e}")
        return None
