import faiss
import numpy as np
import redis
import os
import json

class VectorDB:
    def __init__(self, dimension=128):
        self.dimension = dimension
        #initialize a flat FAISS index
        self.index = faiss.IndexFlatL2(dimension)
        #use Redis to map the FAISS index position to the actual Image ID
        self.client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=6379,
            decode_responses=True
        )
        self.id_map = [] # To keep track of which index belongs to which ID

    def upsert(self, image_id, vector, metadata):
        # 1. Convert list to a float32 numpy array
        v = np.array([vector]).astype('float32')
        
        # 2. Add to FAISS index
        self.index.add(v)
        self.id_map.append(image_id)
        
        # 3. Store the metadata in Redis for retrieval later
        self.client.set(f"meta:{image_id}", json.dumps(metadata))
        return True

    def search(self, query_vector, k=5):
        """Finds the top K most similar images."""
        v = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(v, k)
        
        results = []
        for i in indices[0]:
            if i != -1: # FAISS returns -1 if no match found
                img_id = self.id_map[i]
                results.append({"id": img_id, "metadata": self.client.get(f"meta:{img_id}")})
        return results
