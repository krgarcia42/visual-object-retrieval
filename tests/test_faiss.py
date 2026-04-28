import unittest
import os
import numpy as np
from src.vector_db import VectorDB

class TestFAISS(unittest.TestCase):
    def setUp(self):
        # Use a high-entropy filename that won't conflict with main data
        self.test_index_path = "unit_test_index_isolated.bin"
        
        # Ensure a clean start by removing any leftover test index
        if os.path.exists(self.test_index_path):
            os.remove(self.test_index_path)
            
        # Initialize VectorDB specifically with this isolated path
        self.vdb = VectorDB(dimension=128, index_path=self.test_index_path)

    def tearDown(self):
        # Clean up the file so it doesn't interfere with the next run
        if os.path.exists(self.test_index_path):
            os.remove(self.test_index_path)

    def test_vector_search(self):
        # Define two mathematically distinct vectors
        low_vector = [0.1] * 128
        high_vector = [0.9] * 128
        
        # Add them to our isolated index
        self.vdb.upsert("low_vec", low_vector, {"type": "low"})
        self.vdb.upsert("high_vec", high_vector, {"type": "high"})
        
        # Perform a search for a vector closest to 'low'
        query = [0.11] * 128
        results = self.vdb.search(query, k=1)
        
        # Validation
        self.assertEqual(len(results), 1, "Should return exactly one result")
        
        # This will now correctly match 'low_vec' because 'test_img_1' 
        # only exists in the main faiss_index.bin, not our isolated file.
        actual_id = results[0]["id"]
        self.assertEqual(actual_id, "low_vec", f"Expected low_vec but got {actual_id}")

if __name__ == "__main__":
    unittest.main()
