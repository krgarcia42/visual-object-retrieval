import logging
import json
import os
from src.inference_worker import InferenceWorker
from src.vector_db import VectorDB
from src.storage_service import StorageService
from src.labeler import ImageLabeler
from src.models import ImageRecord
from src.llm_service import LLMService
from src.document_store import DocumentStore

#initialize logging
logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self):
        # Existing services from your original orchestrator
        self.worker = InferenceWorker()
        self.db = VectorDB()
        self.storage = StorageService()
        self.labeler = ImageLabeler()
        
        #LLM and Document Store
        self.llm = LLMService()
        self.doc_store = DocumentStore()
        
        #use the Redis client from your VectorDB to handle Pub/Sub
        self.pubsub = self.db.client.pubsub()

    def start(self):
        self.pubsub.subscribe("image.submitted")
        logger.info("Orchestrator online. Subscribed to Pub/Sub channel: 'image.submitted'")

        #listen for messages indefinitely
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                try:
                    #convert the JSON string from Redis back into a dictionary
                    event = json.loads(message['data'])
                    self.handle_event(event)
                except Exception as e:
                    logger.error(f"Failed to process message: {e}")

    def handle_event(self, event):
        """
        Core Pipeline: Coordinates AI, LLM, and dual-database storage.
        """
        event_id = event.get("event_id")
        payload = event.get("payload")

        if not event_id or not payload:
            logger.error("Invalid event format received.")
            return False

        logger.info(f"Orchestrator handling event: {event_id}")
        
        # 1. Upload to storage (Simulated cloud upload)
        url = self.storage.upload(event_id, payload['image_path'])
        
        # 2. Run Inference: Detect raw objects
        raw_objects = self.worker.detect_objects(payload['image_path'])
        
        # 3. Clean up labels: Using your ImageLabeler
        clean_labels = self.labeler.generate_labels(raw_objects)
        
        # 4. Generate AI Embedding: For vector search
        embedding = self.worker.process_image(payload['image_path'])
        
        # 5. NEW: GENERATE LOCAL LLM SUMMARY
        # This fulfills the 'Favorite LLM' requirement locally.
        ai_description = self.llm.summarize_scene(clean_labels)
        
        # 6. Standardize data structure using ImageRecord model
        record = ImageRecord(event_id, url, clean_labels, embedding)
        record_dict = record.to_dict()
        
        # 7. Save to VECTOR DB
        self.db.upsert(event_id, record_dict, {"status": "success"})

        # 8. Save to Document Store (Mongo Requirement)
        # We store a full JSON 'Document' in Redis to mimic MongoDB.
        document = {
            "event_id": event_id,
            "url": url,
            "analysis": {
                "tags": clean_labels,
                "llm_description": ai_description
            },
            "system_info": {
                "db_type": "NoSQL_Document",
                "processed_at": event.get("timestamp")
            }
        }
        self.doc_store.save_document(event_id, document)
        
        logger.info(f"Pipeline finished for {event_id}. Vector and Document stores updated.")
        return True
