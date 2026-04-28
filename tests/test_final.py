import unittest
import time
import redis
import json
import os
from src.document_store import DocumentStore

class TestSystem(unittest.TestCase):
    def test_end_to_end_logic(self):
        redis_host = os.getenv("REDIS_HOST", "localhost")
        client = redis.Redis(host=redis_host, port=6379, decode_responses=True)
        store = DocumentStore()
        
        #use the filename that the DEBUG logs prove is actually working
        test_filename = "test_image.jpg"
        test_event = {
            "payload": {"image_path": f"data/{test_filename}"}
        }
        
        # 1. Test Pub/Sub: Publish the event
        client.publish("image.submitted", json.dumps(test_event))
        
        # 2. Polling Retry Logic
        doc = None
        max_retries = 5
        for i in range(max_retries):
            doc = store.get_document(test_filename)
            if doc:
                break
            print(f"Waiting for Orchestrator to index {test_filename}... (Attempt {i+1}/{max_retries})")
            time.sleep(1)
        
        # 3. Validation
        if doc is None:
            all_keys = client.keys("*")
            print(f"DEBUG: Search failed. Current keys in Redis: {all_keys}")

        self.assertIsNotNone(doc, f"Document for {test_filename} was never found in Redis.")
        self.assertIn("description", doc)
        
        print(f"Success: Pub/Sub and Document DB Verified for {test_filename}!")

if __name__ == "__main__":
    unittest.main()
