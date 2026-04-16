import yaml
from core.llm import LLM
from core.memory import Memory

class AgentRunner:
    def __init__(self, agent_path: str):
        with open(agent_path, "r") as f:
            self.config = yaml.safe_load(f)
        
        self.name = self.config["name"]
        self.system_prompt = self.config["system_prompt"]
        self.llm = LLM(self.config["llm"])
        
        memory_config = self.config.get("memory", {})
        self.memory_enabled = memory_config.get("enabled", False)
        
        if self.memory_enabled:
            self.memory = Memory(self.name)
            self.messages = self.memory.load()
            print(f"📦 Memory loaded — {len(self.messages)} messages restored.")
        else:
            self.messages = []

    def chat(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        response = self.llm.chat(self.system_prompt, self.messages)
        self.messages.append({"role": "assistant", "content": response})
        
        if self.memory_enabled:
            self.memory.save(self.messages)
        
        return response

    def clear_memory(self):
        if self.memory_enabled:
            self.memory.clear()
            self.messages = []
            print("🗑️ Memory cleared.")