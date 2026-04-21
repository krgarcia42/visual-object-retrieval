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
    #main logic for coordinating services
    topic = event.get("topic")
    payload = event.get("payload")

    if topic == "image.submitted":
      # 1. Upload
      url = self.storage.upload(event['event_id'], payload['image_path'])
      # 2. Inference (Detection)
      raw_objects = self.worker.detect_objects(payload['image_path'])
      # 3. Labeling
      clean_labels = self.labeler.generate_labels(raw_objects)
      # 4. Save to Vector DB with labels in metadata
      embedding = self.worker.process_image(payload['image_path'])
      self.db.upsert(event['event_id'], embedding, {"url": url, "labels": clean_labels})

      return True
    return False
