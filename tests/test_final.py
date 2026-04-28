import unittest
import time
import redis
import json
from src.document_store import DocumentStore

class TestSystem(unittest.TestCase):
    def test_end_to_end_logic(self):
        client = redis.Redis(host='localhost', port=6379)
        store = DocumentStore()
        
        # 1. Test Pub/Sub: Publish a dummy event
        test_event = {
            "payload": {"image_path": "forest_test.jpg"}
        }
        client.publish("image.submitted", json.dumps(test_event))
        
        # 2. Wait for the background orchestrator to process
        time.sleep(1)
        
        # 3. Test Document DB: Verify the document was created
        doc = store.get_document("forest_test.jpg")
        self.assertIsNotNone(doc)
        self.assertIn("description", doc)
        print("Pub/Sub and Document DB Verified!")

if __name__ == "__main__":
    unittest.main()
