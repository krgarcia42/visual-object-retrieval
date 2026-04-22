import os
import redis
import json
import logging
from src.schema import create_event

#added logging for robustness
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageBroker:
    def __init__(self):
        #FIX: Reads Redis credentials from environment variables.
        host = os.getenv('REDIS_HOST', 'localhost')
        port = int(os.getenv('REDIS_PORT', 6379))
        password = os.getenv('REDIS_PASSWORD', None)

        self.client = redis.Redis(
            host=host, 
            port=port, 
            password=password, 
            decode_responses=True
        )

    def publish(self, topic, payload):
        event = create_event(topic, payload)
        try:
            self.client.publish(topic, json.dumps(event))
            logger.info(f"Published event {event['event_id']} to {topic}")
            return event
        except redis.ConnectionError as e:
            logger.error(f"Redis Connection Failed: {e}")
            return None
