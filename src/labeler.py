import logging

logger = logging.getLogger(__name__)

#used LLM to generate ImageLabeler
class ImageLabeler:
    def __init__(self):
        self.min_confidence = 0.5

    def generate_labels(self, detection_results):
        """Converts raw model output into clean searchable labels."""
        # In a real app, this would filter by confidence score
        labels = [res.capitalize() for res in detection_results]
        logger.info(f"Generated labels: {labels}")
        return labels
