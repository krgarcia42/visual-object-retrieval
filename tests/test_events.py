import unittest
from src.messaging_service import send_message

class TestEvents(unittest.TestCase):
  def test_send_message(self):
    result = send_message("test.topic", "123", {"data": "test"})
    self.assertIsNone(result)
