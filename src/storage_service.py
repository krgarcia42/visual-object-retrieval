import logging

logger = logging.getLogger(__name__)

class StorageService:
  def __init__(self):
    self.buckets = {"raw-images": {}}

  def upload(self, file_id, data):
    #simulates uploading file
    self.buckets["raw-images"][file_id] = data
    logger.info(f"File {file_id} uploaded to storage.")
    return f"https://storage.provider/{file_id}"
