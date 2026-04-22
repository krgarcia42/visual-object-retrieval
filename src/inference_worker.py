import logging
import random
from src.image_data import IMAGE_DATASET

logger = logging.getLogger(__name__)

class InferenceWorker:
    def process_image(self, image_path):
        #simulates running model to get 128-dimensional embedding
        logger.info(f"Generating embedding for {image_path}...")
        #generates random numbers for vectors
        embedding = [random.uniform(-1, 1) for _ in range(128)]
        return embedding

    def detect_objects(self, image_path):
        #simulates object detection
        #matches the hard-coded boxes and labels from dataset
        #finds the image in hard-coded dataset
        image_info = next((item for item in IMAGE_DATASET if item["path"] == image_path), None)
        
        if image_info:
            detected = image_info["labels"]
            boxes = image_info["boxes"]
            logger.info(f"Analysis Completed for {image_path}: Found {detected} at {boxes}")
            return detected
        
        #fallback for images not in hard-coded set
        fallback_labels = ["unknown"]
        logger.info(f"Objects detected: {fallback_labels}")
        return fallback_labels
