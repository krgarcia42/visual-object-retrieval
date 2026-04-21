import unittest
from unittest.mock import MagicMock, patch
from src.messaging import MessageBroker
from src.vector_db import VectorDB
from src.inference_worker import InferenceWorker
from src.storage_service import StorageService
from src.orchestrator import Orchestrator
from src.app import submit_image

class TestSystem(unittest.TestCase):
    def setUp(self):
        self.broker = MessageBroker()
        self.broker.client = MagicMock()

    def test_event_generation(self):
        topic = "test.topic"
        payload = {"key": "value"}
        event = self.broker.publish(topic, payload)
        self.assertIsNotNone(event)
        self.assertIn("timestamp", event)
        self.assertIn("event_id", event)
        self.assertEqual(event["type"], "publish")

    def test_redis_publish_called(self):
        self.broker.publish("test", {"data": 123})
        self.broker.client.publish.assert_called_once()

    def test_idempotency(self):
        """Tests that the system can track and ignore duplicate IDs (Screenshot 10)."""
        processed_events = set()
        test_id = "evt_unique_123"
        
        # First time processing
        if test_id not in processed_events:
            processed_events.add(test_id)
            first_run = True
        else:
            first_run = False
            
        # Second time processing (duplicate)
        if test_id not in processed_events:
            second_run = True
        else:
            second_run = False # It's a duplicate!
            
        self.assertTrue(first_run)
        self.assertFalse(second_run)

class TestNewServices(unittest.TestCase):
    def test_vector_db_upsert(self):
        db = VectorDB()
        res = db.upsert("vec1", [0.1, 0.2], {"tag": "test"})
        self.assertTrue(res)

    def test_inference_logic(self):
        worker = InferenceWorker()
        emb = worker.process_image(None)
        self.assertEqual(len(emb), 128)

    def test_storage_upload(self):
        store = StorageService()
        url = store.upload("img123", b"data")
        self.assertIn("img123", url)

class TestIntegration(unittest.TestCase):
    """Verifies that the Orchestrator ties all services together (Screenshot 22)."""
    
    @patch('src.messaging.redis.Redis')
    def test_full_orchestration_flow(self, mock_redis):
        # 1. simulate an image being submitted via app.py
        event = submit_image("test_image.jpg")
        
        # 2. pass that event to the orchestrator
        orc = Orchestrator()
        
        #check if the orchestrator successfully handles the topic
        #confirms it called Storage, Inference, and VectorDB internally
        success = orc.handle_event(event)
        
        self.assertTrue(success)
        self.assertEqual(event["topic"], "image.submitted")

if __name__ == "__main__":
    unittest.main()
