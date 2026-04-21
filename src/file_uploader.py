import logging
import os

logger = logging.getLogger(__name__)

# used LLM to generate this
class FileUploader:
  def __init__(self, allowed_extensions=None):
        self.allowed_extensions = allowed_extensions or {'.jpg', '.jpeg', '.png'}

  def validate_and_upload(self, file_path, storage_service):
      """Checks if the file is valid before sending to storage."""
      ext = os.path.splitext(file_path)[1].lower()
        
      if ext not in self.allowed_extensions:
          logger.error(f"Invalid file type: {ext}")
          return None
        
      # If valid, use the storage service to 'upload' it
      logger.info(f"File {file_path} validated. Uploading...")
      return storage_service.upload(os.path.basename(file_path), b"simulated_data")
