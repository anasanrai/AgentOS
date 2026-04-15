import yaml
from core.llm import LLM

class AgentRunner:
    def __init__(self, agent_path: str):
        with open(agent_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.name = self.config["name"]
        self.system_prompt = self.config["system_prompt"]
        self.llm = LLM(self.config["llm"])
        self.messages = []

    def chat(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        response = self.llm.chat(self.system_prompt, self.messages)
        self.messages.append({"role": "assistant", "content": response})
        return response