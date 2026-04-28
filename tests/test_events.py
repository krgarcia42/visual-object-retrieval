import unittest
import os
import json
from unittest.mock import MagicMock, patch
from src.vector_db import VectorDB
from src.inference_worker import InferenceWorker
from src.orchestrator import Orchestrator
from src.document_store import DocumentStore

# We assume these are helper classes you've built
# If they are in different files, adjust the imports accordingly
from src.file_uploader import FileUploader
from src.labeler import ImageLabeler

class TestUnits(unittest.TestCase):
    """
    UNIT TESTS: These use Mocks. 
    They do not require a running Redis server.
    """
    def test_idempotency_logic(self):
        """Simulates idempotency check to prevent duplicate processing"""
        processed_events = set()
        test_id = "evt_123"
        processed_events.add(test_id)
        
        # Logic check: if we try to add it again, we should detect it
        is_duplicate = test_id in processed_events
        self.assertTrue(is_duplicate)

    def test_file_uploader_validation(self):
        """Checks file extension filtering logic"""
        uploader = FileUploader()
        mock_storage = MagicMock()
        
        # Should return None/False for invalid extension
        self.assertIsNone(uploader.validate_and_upload("test.txt", mock_storage))
        
        # Should trigger 'upload' for valid extension
        uploader.validate_and_upload("test.jpg", mock_storage)
        self.assertTrue(mock_storage.upload.called)

    def test_labeler_formatting(self):
        """Checks that labels are properly cleaned/capitalized"""
        labeler = ImageLabeler()
        labels = labeler.generate_labels(["cat", "person"])
        self.assertEqual(labels, ["Cat", "Person"])

class TestDatabase(unittest.TestCase):
    """
    DATABASE TESTS: These require the environment to handle FAISS/Redis.
    """
    def test_vector_db_upsert(self):
        """Tests that FAISS accepts vectors and maps them to IDs"""
        # dimension=128 matches your InferenceWorker
        db = VectorDB(dimension=128)
        vector = [0.1] * 128
        success = db.upsert("test_img_1", vector, {"tag": "unit_test"})
        self.assertTrue(success)
        self.assertEqual(db.index.ntotal, 1)

class TestIntegration(unittest.TestCase):
    """
    INTEGRATION TESTS: These use the real Redis flow.
    """
    def setUp(self):
        self.orch = Orchestrator()
        self.doc_store = DocumentStore()

    def test_full_orchestration_flow(self):
        """
        Tests the end-to-end flow from event pickup to storage.
        """
        # 1. Create a dummy event
        test_event = {
            "event_id": "test_sync_123",
            "topic": "image.submitted",
            "payload": {"image_path": "test_image.jpg"}
        }

        # 2. Directly call process_pipeline (bypassing the pubsub loop for the test)
        self.orch.process_pipeline(test_event)
        
        # 3. Verify Document Store (Redis) has the data
        doc = self.doc_store.client.get("image_doc:test_image.jpg")
        self.assertIsNotNone(doc)
        
        # 4. Verify FAISS has the vector
        self.assertGreaterEqual(self.orch.vector_db.index.ntotal, 1)

if __name__ == "__main__":
    unittest.main()
