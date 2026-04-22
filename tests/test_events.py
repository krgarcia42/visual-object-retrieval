import unittest
import os
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
        # We mock the client for unit tests to avoid hitting the cloud every time
        self.broker.client = MagicMock()

    def test_event_generation(self):
        """Verifies event schema contains all required fields"""
        event = self.broker.publish("test.topic", {"key": "value"})
        self.assertIsNotNone(event)
        self.assertIn("timestamp", event)
        self.assertIn("event_id", event)
        self.assertEqual(event["type"], "publish")

    def test_idempotency(self):
        """Simulates idempotency check to prevent duplicate processing"""
        processed_events = set()
        test_id = "evt_123"
        processed_events.add(test_id)
        is_duplicate = test_id in processed_events
        self.assertTrue(is_duplicate)

class TestNewServices(unittest.TestCase):
    def test_file_uploader_validation(self):
        """Checks file extension filtering"""
        uploader = FileUploader()
        mock_storage = MagicMock()
        # Should fail for .txt
        self.assertIsNone(uploader.validate_and_upload("test.txt", mock_storage))
        # Should pass for .jpg
        uploader.validate_and_upload("test.jpg", mock_storage)
        mock_storage.upload.assert_called_once()

    def test_labeler_formatting(self):
        """Checks that labels are properly capitalized"""
        labeler = ImageLabeler()
        labels = labeler.generate_labels(["cat", "person"])
        self.assertEqual(labels, ["Cat", "Person"])

    def test_vector_db_upsert(self):
        """Tests database entry logic"""
        db = VectorDB()
        self.assertTrue(db.upsert("vec1", [0.1], {"tag": "test"}))

class TestIntegration(unittest.TestCase):
    def test_full_orchestration_flow(self):
        """
        Tests the end-to-end flow.
        This will use REDIS_HOST from environment/secrets.
        """
        # 1. Trigger submission through app.py
        event = submit_image("test_image.jpg")
        self.assertIsNotNone(event)

        # 2. Run orchestrator to coordinate services
        orc = Orchestrator()
        success = orc.handle_event(event)
        
        self.assertTrue(success)
        self.assertEqual(event["topic"], "image.submitted")

if __name__ == "__main__":
    unittest.main()
