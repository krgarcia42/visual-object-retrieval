import logging
import random
from src.image_data import IMAGE_DATASET

logger = logging.getLogger(__name__)

class InferenceWorker:
    def process_image(self, image_path):
        #simulates running a model to get a 128-dimensional embedding
        logger.info(f"Generating embedding for {image_path}...")
        #generates random numbers to simulate high-dimensional AI vectors
        embedding = [random.uniform(-1, 1) for _ in range(128)]
        return embedding

    def detect_objects(self, image_path):
        #simulates object detection by looking up labels in our hard-coded dataset
        #finds the image in our IMAGE_DATASET to ensure deterministic results
        image_info = next((item for item in IMAGE_DATASET if item["path"] == image_path), None)
        
        if image_info:
            detected = image_info["labels"]
            logger.info(f"Analysis Completed for {image_path}: Found {detected}")
            return detected
        
        fallback_labels = ["object", "visual_element"]
        logger.info(f"Warning: {image_path} not in dataset. Using fallback: {fallback_labels}")
        return fallback_labels
