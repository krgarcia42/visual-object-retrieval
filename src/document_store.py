import redis
import json
import os

class DocumentStore:
    def __init__(self):
        #connect to existing Redis instance
        self.client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=6379,
            decode_responses=True
        )

    def save_image_document(self, image_id, document):
        """Stores a nested dictionary as a JSON 'Document' in Redis."""
        key = f"image_doc:{image_id}"
        #simulates a Mongo document save
        self.client.set(key, json.dumps(document))
        return key
