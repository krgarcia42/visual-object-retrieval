import unittest
import os
import numpy as np
import redis
from src.vector_db import VectorDB

class TestFAISS(unittest.TestCase):
    def setUp(self):
        # 1. Force a unique file path
        self.test_index_path = "completely_isolated_test.bin"
        
        # 2. Clear Redis entirely to remove 'test_img_1' from the id_map
        self.redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379)
        self.redis_client.flushdb() 
        
        # 3. Delete any leftover local files
        if os.path.exists(self.test_index_path):
            os.remove(self.test_index_path)
            
        # 4. Initialize VectorDB with the unique path
        self.vdb = VectorDB(dimension=128, index_path=self.test_index_path)

    def tearDown(self):
        # Clean up after ourselves
        if os.path.exists(self.test_index_path):
            os.remove(self.test_index_path)
        self.redis_client.flushdb()

    def test_vector_search(self):
        # Vectors must be clearly distinct
        low_vector = [0.1] * 128
        high_vector = [0.9] * 128
        
        # Upsert into a clean environment
        self.vdb.upsert("low_vec", low_vector, {"type": "low"})
        self.vdb.upsert("high_vec", high_vector, {"type": "high"})
        
        # Search
        query = [0.11] * 128
        results = self.vdb.search(query, k=1)
        
        self.assertEqual(len(results), 1)
        actual_id = results[0]["id"]
        
        # This will now pass because flushdb() killed 'test_img_1'
        self.assertEqual(actual_id, "low_vec", f"Expected low_vec but got {actual_id}")

if __name__ == "__main__":
    unittest.main()
