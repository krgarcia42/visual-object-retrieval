import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def send_message(topic, event_id, payload):
  message = {
    "topic": topic,
    "event_id": event_id,
    "payload": payload

  }

  r.publish(topic, json.dumps(message))
  print("sent")

if __name__ == "__main__":
  send_message("image.submitted", "evt_001", {"image_id": "img_01"})
