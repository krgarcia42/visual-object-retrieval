import unittest
import os
import numpy as np
from src.vector_db import VectorDB

class TestFAISS(unittest.TestCase):
    def setUp(self):
        # Use a unique index file specifically for this test class
        self.test_index_path = "temp_test_faiss.bin"
        if os.path.exists(self.test_index_path):
            os.remove(self.test_index_path)
            
        # Initialize VectorDB with the isolated test path
        self.vdb = VectorDB(dimension=128, index_path=self.test_index_path)

    def tearDown(self):
        # Clean up the temporary file after tests finish
        if os.path.exists(self.test_index_path):
            os.remove(self.test_index_path)

    def test_vector_search(self):
        # Create distinct dummy vectors
        low_vector = [0.1] * 128
        high_vector = [0.9] * 128
        
        self.vdb.upsert("low_vec", low_vector, {"type": "low"})
        self.vdb.upsert("high_vec", high_vector, {"type": "high"})
        
        # Search for a vector very close to the 'low' one
        query = [0.11] * 128
        results = self.vdb.search(query, k=1)
        
        self.assertEqual(len(results), 1)
        # Now this will pass because 'test_img_1' isn't in this isolated index
        self.assertEqual(results[0]["id"], "low_vec")

if __name__ == "__main__":
    unittest.main()
