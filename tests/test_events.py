import unittest
from unittest.mock import MagicMock,patch
from src.messaging import MessageBroker

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

if __name__ == "__main__":
  unittest.main()
