import logging
from src.inference_worker import InferenceWorker
from src.vector_db import VectorDB
from src.storage_service import StorageService
from src.labeler import ImageLabeler

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self):
        self.worker = InferenceWorker()
        self.db = VectorDB()
        self.storage = StorageService()
        self.labeler = ImageLabeler()

    def handle_event(self, event):
        #Main logic for coordinating services
        topic = event.get("topic")
        payload = event.get("payload")

        if topic == "image.submitted":
            logger.info(f"Orchestrator handling event: {event['event_id']}")
            
            # 1. Upload to storage
            url = self.storage.upload(event['event_id'], payload['image_path'])
            
            # 2. Run inference to detect objects
            raw_objects = self.worker.detect_objects(payload['image_path'])
            
            # 3. Clean up the labels
            clean_labels = self.labeler.generate_labels(raw_objects)
            
            # 4. Generate the AI embedding
            embedding = self.worker.process_image(payload['image_path'])
            
            # 5. Use ImageRecord model to standardize data structure
            #gathers everything into one clean dictionary
            record = ImageRecord(event['event_id'], url, clean_labels, embedding)
            
            # 6. Save record and embedding to the Vector DB
            self.db.upsert(event['event_id'], record.to_dict(), {"status": "success"})

            return True
        return False
