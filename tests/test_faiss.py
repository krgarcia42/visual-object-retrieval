import unittest
import os
import numpy as np
from src.vector_db import VectorDB

class TestFAISS(unittest.TestCase):
    def setUp(self):
        #define a specific test index file to avoid messing with production data
        self.test_index = "test_faiss_logic.bin"
        if os.path.exists(self.test_index):
            os.remove(self.test_index)
        
        #initialize with the test-specific path
        self.vdb = VectorDB(dimension=128, index_path=self.test_index)

    def tearDown(self):
        if os.path.exists(self.test_index):
            os.remove(self.test_index)

    def test_vector_search(self):
        low_vector = [0.1] * 128
        high_vector = [0.9] * 128
        
        self.vdb.upsert("low_vec", low_vector, {"type": "low"})
        self.vdb.upsert("high_vec", high_vector, {"type": "high"})
        
        #search for something close to low_vector
        results = self.vdb.search([0.11] * 128, k=1)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "low_vec")

if __name__ == "__main__":
    unittest.main()
