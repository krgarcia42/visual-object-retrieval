import redis
import json
from src.schema import create_event

r = redis.Redis(host='localhost', port=6379, db=0)
class MessageBroker:
  def publish(self, topic, payload):
    event = create_event(topic, payload)

    r.publish(topic, json.dumps(event))
    print("sent")
