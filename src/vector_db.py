import logging

logger = logging.getLogger(__name__)

class VectorDB:
  def __init__(self):
    #simulating vector database
    self.storage = {}

  def upsert(self, vector_id, embedding, metadata):
    #stores vectors and metadata
    self.storage[vector_id] = {
      "embedding": embedding,
      "metadata": metadata,
    }
    logger.info(f"Vector {vector_id} upserted successfully.")
    return True

  def search(self, query_embedding, top_k=5):
    #simulates similarity search
    logger.info(f"Searching for top {top_k} similar vectors.")
    #return dummy results for now
    return list(self.storage.keys())[:top_k]
