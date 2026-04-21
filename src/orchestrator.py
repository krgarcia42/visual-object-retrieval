import logging
from src.inference_worker import InferenceWorker
from src.vector_db import VectorDB
from src.storage_service import StorageService

logger = logging.getLogger(__name__)

class Orchestrator:
  def __init__(self):
    self.worker = InferenceWorker()
    self.db = VectorDB()
    self.storage = StorageService()

  def handle_event(self, event):
    #main logic for coordinating services
    topic = event.get("topic")
    payload = event.get("payload")

    if topic = "image.submitted":
      logger.info("Orchestrator: Handling image submission...")
      # 1. store the image
      url = self.storage.upload(event['event_id'], payload['image_path'])
      # 2. run inference
      embedding = self.worker.process_image(payload['image_path'])
      # 3. save to vector DB
      self.db.upsert(event['event_id'], embedding, {"url": url})

      return True
    return False
