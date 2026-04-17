import yaml
from core.llm import LLM
from core.memory import Memory
from core.tools import TOOLS, run_tool
import json
import re

class AgentRunner:
    def __init__(self, agent_path: str):
        with open(agent_path, "r") as f:
            self.config = yaml.safe_load(f)
        
        self.name = self.config["name"]
        self.system_prompt = self.config["system_prompt"]
        self.llm = LLM(self.config["llm"])
        
        memory_config = self.config.get("memory", {})
        self.memory_enabled = memory_config.get("enabled", False)
        
        tools_config = self.config.get("tools", {})
        self.tools_enabled = tools_config.get("enabled", False)
        self.available_tools = tools_config.get("available", [])
        
        if self.memory_enabled:
            self.memory = Memory(self.name)
            self.messages = self.memory.load()
            print(f"📦 Memory loaded — {len(self.messages)} messages restored.")
        else:
            self.messages = []

    def chat(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        response = self.llm.chat(self.system_prompt, self.messages)
        
        if self.tools_enabled and "TOOL:" in response:
            response = self._handle_tool(response)
        
        self.messages.append({"role": "assistant", "content": response})
        
        if self.memory_enabled:
            self.memory.save(self.messages)
        
        return response

    def _handle_tool(self, response: str) -> str:
        try:
            tool_match = re.search(r"TOOL:\s*(\w+)", response)
            params_match = re.search(r"PARAMS:\s*(\{.*\})", response)
            
            if not tool_match:
                return response
            
            tool_name = tool_match.group(1)
            params = json.loads(params_match.group(1)) if params_match else {}
            
            if tool_name not in self.available_tools:
                return f"Tool '{tool_name}' is not available."
            
            print(f"🔧 Using tool: {tool_name}")
            tool_result = run_tool(tool_name, params)
            
            follow_up = self.llm.chat(
                self.system_prompt,
                self.messages + [
                    {"role": "assistant", "content": response},
                    {"role": "user", "content": f"[Tool result for {tool_name}]: {tool_result}. Now respond naturally to the user without showing the TOOL or PARAMS lines."}
                ]
            )
            return follow_up
            
        except Exception as e:
            return f"Tool error: {str(e)}"

    def clear_memory(self):
        if self.memory_enabled:
            self.memory.clear()
            self.messages = []
            print("🗑️ Memory cleared.")