import redis
import json

class Memory:
    def __init__(self, agent_name: str):
        self.client = redis.Redis(host='localhost', port=6379, db=0)
        self.key = f"agentos:{agent_name}:history"

    def load(self) -> list:
        data = self.client.get(self.key)
        if data:
            return json.loads(data)
        return []

    def save(self, messages: list):
        self.client.set(self.key, json.dumps(messages))

    def clear(self):
        self.client.delete(self.key)