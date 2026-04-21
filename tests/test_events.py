import unittest
from unittest.mock import MagicMock,patch
from src.messaging import MessageBroker
from src.vector_db import VectorDB
from src.inference_worker import InferenceWorker
from src.storage_service import StorageService

class TestSystem(unittest.TestCase):
  def setUp(self):
    self.broker = MessageBroker()
    #fix: mocking Redis client so tests pass in actions
    self.broker.client = MagicMock()

  def test_event_generation(self):
    #verifies returned event contains all required keys
    topic = "test.topic"
    payload = {"key": "value"}

    event = self.broker.publish(topic, payload)

    #check for fields
    self.assertIsNotNone(event)
    self.assertIn("timestamp", event)
    self.assertIn("event_id", event)
    self.assertEqual(event["type"], "publish")

  def test_redis_publish_called(self):
    #verifies broker actually calls the redis publish method
    self.broker.publish("test", {"data": 123})
    self.broker.client.publish.assert_called_once()

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


if __name__ == "__main__":
  unittest.main()
