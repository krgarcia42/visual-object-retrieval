import logging
from src.messaging import MessageBroker

logger = logging.getLogger(__name__)

def submit_image(image_path):
  #entry point for image submission
  logger.info(f"New image submission received: {image_path})

  broker = MessageBroker()
  payload = {"image_path": image_path, "status": "pending"}

  #triggers image submitted event
  event = broker.publish("image.submitted", payload)
  return event
