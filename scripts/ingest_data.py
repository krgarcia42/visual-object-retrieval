import logging
import sys
import os
import json
import uuid
from datetime import datetime
import redis

#ensure script can find src folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.image_data import IMAGE_DATASET

#logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_ingestion():
    # 1. Connect to Redis (The Message Broker)
    try:
        client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            password=os.getenv("REDIS_PASSWORD", None),
            decode_responses=True
        )
        #test connection
        client.ping()
    except Exception as e:
        logger.error(f"Could not connect to Redis: {e}")
        return

    logger.info("Starting Pub-Sub ingestion of 10 photos...")

    for item in IMAGE_DATASET:
        # 2. Construct the Event Object
        # This matches the 'event' structure your Orchestrator expects
        event_id = str(uuid.uuid4())
        event_payload = {
            "event_id": event_id,
            "topic": "image.submitted",
            "timestamp": datetime.now().isoformat(),
            "payload": {
                "image_path": item['path']
            }
        }

        # 3. Publish to the 'image.submitted' channel
        try:
            #convert the dictionary to a JSON string for Redis
            client.publish("image.submitted", json.dumps(event_payload))
            logger.info(f"Published event {event_id} for: {item['path']}")
        except Exception as e:
            logger.error(f"Failed to publish {item['path']}: {e}")

    logger.info("Ingestion Complete. All events broadcasted via Pub-Sub.")

if __name__ == "__main__":
    run_ingestion()
