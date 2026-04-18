from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.runner import AgentRunner
import os
import glob

app = FastAPI(
    title="AgentOS API",
    description="Run AI agents from YAML via HTTP",
    version="1.0.0"
)

# Store active agents in memory
agents = {}

class ChatRequest(BaseModel):
    message: str
    agent: str = "assistant"

class ChatResponse(BaseModel):
    agent: str
    message: str
    response: str

def get_or_create_agent(agent_name: str) -> AgentRunner:
    if agent_name not in agents:
        path = f"agents/{agent_name}.yaml"
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
        agents[agent_name] = AgentRunner(path)
    return agents[agent_name]

@app.get("/health")
def health():
    return {
        "status": "online",
        "version": "1.0.0",
        "active_agents": list(agents.keys())
    }

@app.get("/agents")
def list_agents():
    yaml_files = glob.glob("agents/*.yaml")
    available = [os.path.basename(f).replace(".yaml", "") for f in yaml_files]
    return {
        "available": available,
        "active": list(agents.keys())
    }

@app.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:
    agent = get_or_create_agent(request.agent)
    response = agent.chat(request.message)
    return ChatResponse(
        agent=request.agent,
        message=request.message,
        response=response
    )

@app.post("/agents/{agent_name}/clear")
def clear_memory(agent_name: str):
    agent = get_or_create_agent(agent_name)
    agent.clear_memory()
    return {"status": "cleared", "agent": agent_name}