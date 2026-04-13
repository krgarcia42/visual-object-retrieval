import uuid
import time

def create_event(topic, payload):
  #fix: added missing imports (uuid & time) and included required fields (type & timestamp)
  return {
    "type": "publish",
    "topic": topic,
    "event_id": str(uuid.uuid4()), #generate unique ID
    "payload": payload,
    "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()) # ISO 8601 format
  }
