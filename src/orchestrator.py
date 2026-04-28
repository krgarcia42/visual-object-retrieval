import json
import logging
from src.inference_worker import InferenceWorker
from src.llm_service import LLMService
from src.document_store import DocumentStore
from src.vector_db import VectorDB

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self):
        self.worker = InferenceWorker()
        self.llm = LLMService()
        self.doc_store = DocumentStore()
        #initialize the FAISS Vector Database
        self.vector_db = VectorDB(dimension=128) 
        
        #access Redis client through doc_store for Pub/Sub
        self.pubsub = self.doc_store.client.pubsub()

    def start(self):
        #subscriber logic of the Pub/Sub system
        self.pubsub.subscribe("image.submitted")
        logger.info("Orchestrator online... Listening for events.")

        for message in self.pubsub.listen():
            if message['type'] == 'message':
                try:
                    event = json.loads(message['data'])
                    self.process_pipeline(event)
                except Exception as e:
                    logger.error(f"Error processing message: {e}")

    def process_pipeline(self, event):
        path = event['payload']['image_path']
        image_id = path.split("/")[-1]

        # 1. Simulate Image Processing (Labels & Embeddings)
        labels = self.worker.detect_objects(path)
        vector = self.worker.process_image(path)
        
        # 2. Simulate LLM (Generative Summary)
        description = self.llm.summarize_scene(labels)

        # 3. Store as a NoSQL Document (Redis-as-Mongo)
        doc = {
            "path": path,
            "tags": labels,
            "description": description,
            "embedding_snippet": vector[:5]
        }
        self.doc_store.save_document(image_id, doc)

        # 4. Index the embedding in FAISS (Embedding DB)
        #store the labels/description as metadata within the vector index
        self.vector_db.upsert(
            image_id=image_id, 
            vector=vector, 
            metadata={"labels": labels, "description": description}
        )

        logger.info(f"Pipeline finished for {path}. Indexed in FAISS and stored in Document DB.")
