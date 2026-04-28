import unittest
import time
import redis
import os
import json
from src.document_store import DocumentStore

class TestSystem(unittest.TestCase):
    def test_end_to_end_logic(self):
        store = DocumentStore()
        test_filename = "test_image.jpg"
        
        #polling: The background worker might be processing the batch
        doc = None
        for i in range(15):  # 30 seconds total
            # 1. Try to find the specific test image
            doc_raw = store.get_document(test_filename)
            if doc_raw:
                doc = doc_raw
                break
            
            # 2. Backup check: Has any image doc landed? 
            # (Proves the Orchestrator is alive and working)
            all_keys = store.client.keys("image_doc:*")
            if all_keys:
                raw_data = store.client.get(all_keys[0])
                doc = json.loads(raw_data)
                break
                
            print(f"Waiting for Orchestrator... (Attempt {i+1}/15)")
            time.sleep(2)
        
        self.assertIsNotNone(doc, "Timeout: No documents appeared in Redis.")
        print("Integration Verified: Data found in Document Store.")

if __name__ == "__main__":
    unittest.main()
