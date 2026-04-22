import logging
import sys
import os

#ensure script can find src folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app import submit_image
from src.image_data import IMAGE_DATASET

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_ingestion():
  logger.info("Starting analysis and upload of 10 photos...")

  for item in IMAGE_DATASET:
    logger.info(f"Processing photo: {item['path']}...")
    #submit image path to pipeline
    event = submit_image(item['path'])

    if event:
      logger.info(f"Successfully analyzed and uploaded: {item['path']}")
    else:
      logger.error(f"Failed to process: {item['path']}")

  logger.info("Ingestion Complete. 10/10 photos processed.")

if __name__ == "__main__"
    run_ingestion()
