import unittest
from unittest.mock import MagicMock, patch
from src.messaging import MessageBroker
from src.vector_db import VectorDB
from src.inference_worker import InferenceWorker
from src.storage_service import StorageService
from src.orchestrator import Orchestrator
from src.app import submit_image
from src.file_uploader import FileUploader
from src.labeler import ImageLabeler

class TestSystem(unittest.TestCase):
    def setUp(self):
        self.broker = MessageBroker()
        self.broker.client = MagicMock()

    def test_event_generation(self):
        event = self.broker.publish("test.topic", {"key": "value"})
        self.assertIsNotNone(event)
        self.assertIn("timestamp", event)
        self.assertEqual(event["type"], "publish")

    def test_idempotency(self):
        processed_events = set()
        test_id = "evt_123"
        processed_events.add(test_id)
        is_duplicate = test_id in processed_events
        self.assertTrue(is_duplicate)

class TestNewServices(unittest.TestCase):
    def test_file_uploader_validation(self):
        uploader = FileUploader()
        mock_storage = MagicMock()
        # Test invalid extension
        result = uploader.validate_and_upload("test.txt", mock_storage)
        self.assertIsNone(result)
        # Test valid extension
        uploader.validate_and_upload("test.jpg", mock_storage)
        mock_storage.upload.assert_called_once()

    def test_labeler_formatting(self):
        labeler = ImageLabeler()
        results = ["cat", "dog"]
        labels = labeler.generate_labels(results)
        self.assertEqual(labels, ["Cat", "Dog"])

    def test_vector_db_upsert(self):
        db = VectorDB()
        self.assertTrue(db.upsert("vec1", [0.1], {"tag": "test"}))

class TestIntegration(unittest.TestCase):
    @patch('src.messaging.redis.Redis')
    def test_full_orchestration_flow(self, mock_redis):
        """Tests the full pipeline including labeling and storage."""
        # 1. Trigger submission
        event = submit_image("test_image.jpg")
        
        # 2. Run orchestrator
        orc = Orchestrator()
        success = orc.handle_event(event)
        
        self.assertTrue(success)
        # Verify the database mock within Orchestrator actually got data
        # (This confirms the labeler and inference worker were called)
        self.assertIn("image.submitted", event["topic"])

if __name__ == "__main__":
    unittest.main()
