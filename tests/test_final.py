import unittest
import time
import redis
import json
import os
from src.document_store import DocumentStore

class TestSystem(unittest.TestCase):
    def test_end_to_end_logic(self):
        # Use environment variables for Redis host to ensure CI/CD compatibility
        redis_host = os.getenv("REDIS_HOST", "localhost")
        client = redis.Redis(host=redis_host, port=6379, decode_responses=True)
        store = DocumentStore()
        
        test_filename = "forest_test.jpg"
        test_event = {
            "payload": {"image_path": f"data/{test_filename}"}
        }
        
        # 1. Test Pub/Sub: Publish the event
        client.publish("image.submitted", json.dumps(test_event))
        
        # 2. Polling Retry Logic (Robust way to wait for async background workers)
        doc = None
        max_retries = 5
        for i in range(max_retries):
            # We try to get the document using the filename
            doc = store.get_document(test_filename)
            if doc:
                break
            print(f"Waiting for Orchestrator... (Attempt {i+1}/{max_retries})")
            time.sleep(1) # Wait 1 second before retrying
        
        # 3. Validation
        if doc is None:
            # Debugging aid: Print all keys currently in Redis to see what actually got saved
            all_keys = client.keys("*")
            print(f"DEBUG: Search failed. Current keys in Redis: {all_keys}")

        self.assertIsNotNone(doc, f"Document for {test_filename} was never created in Redis.")
        self.assertIn("description", doc)
        self.assertIn("tags", doc)
        
        print(f"Success: Pub/Sub and Document DB Verified for {test_filename}!")

if __name__ == "__main__":
    unittest.main()
