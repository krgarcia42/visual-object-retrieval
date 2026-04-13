import redis
import json
import logging
from src.schema import create_event

#added logging for robustness
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageBroker:
    def __init__(self, host='localhost', port=6379):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)
        # (decode_responses=True) makes it so we don't have to manually decode bytes

    def publish(self, topic, payload):
        #fix: added error handling for Redis connection issues
        event = create_event(topic, payload)
        
        try:
            #sends to Redis in a real environment
            self.client.publish(topic, json.dumps(event))
            logger.info(f"Published event {event['event_id']} to {topic}")
            return event
        except redis.ConnectionError as e:
            #log the error instead of crashing
            logger.error(f"Could not connect to Redis: {e}")
            return None
