import unittest
from src.messaging import MessageBroker

class TestSystem(unittest.TestCase):
  def test_logic(self):
    broker = MessageBroker()
    result = broker.publish("test", {"data": "info"})
    self.assertIsNotNone(result)

  def test_timestamp(self):
    from src.schema import create_event
    event = create_event("test", {})
    self.assertIn("timestamp", event)
