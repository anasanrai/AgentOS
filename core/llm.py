import anthropic
from dotenv import load_dotenv

load_dotenv()

class LLM:
    def __init__(self, config: dict):
        self.client = anthropic.Anthropic()
        self.model = config.get("model", "claude-sonnet-4-20250514")
        self.max_tokens = config.get("max_tokens", 1000)

    def chat(self, system_prompt: str, messages: list) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system_prompt,
            messages=messages
        )
        return response.content[0].text