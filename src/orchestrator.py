import json
import logging
from src.inference_worker import InferenceWorker
from src.llm_service import LLMService
from src.document_store import DocumentStore

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self):
        self.worker = InferenceWorker()
        self.llm = LLMService()
        self.doc_store = DocumentStore()
        self.pubsub = self.doc_store.client.pubsub()

    def start(self):
        """The 'Subscriber' logic of the Pub/Sub system."""
        self.pubsub.subscribe("image.submitted")
        logger.info("Orchestrator online... Listening for events.")

        for message in self.pubsub.listen():
            if message['type'] == 'message':
                event = json.loads(message['data'])
                self.process_pipeline(event)

    def process_pipeline(self, event):
        path = event['payload']['image_path']
        # 1. Simulate Image Processing
        labels = self.worker.detect_objects(path)
        vector = self.worker.process_image(path)
        
        # 2. Simulate LLM
        description = self.llm.summarize_scene(labels)

        # 3. Store as a NoSQL Document
        doc = {
            "path": path,
            "tags": labels,
            "description": description,
            "embedding_snippet": vector[:5]
        }
        self.doc_store.save_document(path.split("/")[-1], doc)
        logger.info(f"Pipeline finished for {path}")
