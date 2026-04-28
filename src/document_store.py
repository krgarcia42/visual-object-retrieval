import redis
import json
import os

class DocumentStore:
    def __init__(self):
        self.client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=6379,
            decode_responses=True
        )

    def save_document(self, image_id, data):
        #stores a nested dictionary as a JSON 'Document'
        key = f"image_doc:{image_id}"
        self.client.set(key, json.dumps(data))
        return key

    def get_document(self, image_id):
        data = self.client.get(f"image_doc:{image_id}")
        return json.loads(data) if data else None
