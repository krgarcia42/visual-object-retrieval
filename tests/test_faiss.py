import unittest
import os
import numpy as np
import redis
import json
from src.vector_db import VectorDB

class TestFAISS(unittest.TestCase):
    def setUp(self):
        self.test_index_path = "unit_test_index.bin"
        self.redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True)
        
        #clean only the keys/files this specific test uses
        self.redis_client.delete("faiss_id_map")
        if os.path.exists(self.test_index_path):
            os.remove(self.test_index_path)
            
        self.vdb = VectorDB(dimension=128, index_path=self.test_index_path)

    def test_vector_search(self):
        #insert known test vectors
        self.vdb.upsert("low_vec", [0.1]*128, {"type": "low"})
        self.vdb.upsert("high_vec", [0.9]*128, {"type": "high"})
        
        #search for a query close to 'low'
        results = self.vdb.search([0.11]*128, k=1)
        
        self.assertEqual(len(results), 1)
        #identity check: This will pass because we cleared 'faiss_id_map' in setUp
        self.assertEqual(results[0]["id"], "low_vec")

    def tearDown(self):
        if os.path.exists(self.test_index_path):
            os.remove(self.test_index_path)

if __name__ == "__main__":
    unittest.main()
