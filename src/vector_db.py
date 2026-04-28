import faiss
import numpy as np
import redis
import os
import json

class VectorDB:
    def __init__(self, dimension=128, index_path="faiss_index.bin"):
        self.dimension = dimension
        self.index_path = index_path
        
        #initialize Redis client
        self.client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=6379,
            decode_responses=True
        )

        # 1. Load existing index from disk or create a new one
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        else:
            self.index = faiss.IndexFlatL2(dimension)

    @property
    def id_map(self):
        """Retrieve the ID map from Redis to stay synced across processes."""
        data = self.client.get("faiss_id_map")
        return json.loads(data) if data else []

    def upsert(self, image_id, vector, metadata):
        # 1. Convert to numpy array
        v = np.array([vector]).astype('float32')
        
        # 2. Add to FAISS index
        self.index.add(v)
        
        # 3. Update the ID map in Redis (so it survives process restarts)
        current_map = self.id_map
        current_map.append(image_id)
        self.client.set("faiss_id_map", json.dumps(current_map))
        
        # 4. Save metadata
        self.client.set(f"meta:{image_id}", json.dumps(metadata))

        # 5. CRITICAL: Persist the FAISS index to disk
        faiss.write_index(self.index, self.index_path)
        return True

    def search(self, query_vector, k=5):
        v = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(v, k)
        
        current_map = self.id_map
        results = []
        for i in indices[0]:
            if i != -1 and i < len(current_map):
                img_id = current_map[i]
                results.append({
                    "id": img_id, 
                    "metadata": self.client.get(f"meta:{img_id}")
                })
        return results
