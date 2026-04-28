import unittest
import numpy as np
from src.vector_db import VectorDB

class TestFAISS(unittest.TestCase):
    def test_vector_search(self):
        db = VectorDB(dimension=128)
        
        # Create two slightly different vectors
        vec1 = [0.1] * 128
        vec2 = [0.9] * 128
        
        db.upsert("low_vec", vec1, {"type": "low"})
        db.upsert("high_vec", vec2, {"type": "high"})
        
        # Search using a vector close to vec1
        query = [0.11] * 128
        results = db.search(query, k=1)
        
        self.assertEqual(results[0]["id"], "low_vec")
        print("FAISS Vector Search successful")

if __name__ == "__main__":
    unittest.main()
