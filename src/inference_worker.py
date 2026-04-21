import logging
import random

logger = logging.getLogger(__name__)

class InferenceWorker:
  def process_image(self, image_data):
        #simulates running model to get embedding
        logger.info("Processing image through AI model...")
        #simulate 128-dimensional vector
        embedding = [random.uniform(-1, 1) for _ in range(128)]
        return embedding

  def detect_objects(self, image_data):
      #simulates object detection
      labels = ["cat", "dog", "car", "person"]
      detected = random.sample(labels, 2)
      logger.info(f"Objects detected: {detected}")
      return detected
