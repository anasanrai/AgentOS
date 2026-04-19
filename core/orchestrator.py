import re
from core.runner import AgentRunner

class Orchestrator:
    def __init__(self):
        self.manager = AgentRunner("agents/manager.yaml")
        self.agents = {
            "researcher": AgentRunner("agents/researcher.yaml"),
            "coder": AgentRunner("agents/coder.yaml"),
            "writer": AgentRunner("agents/writer.yaml")
        }

    def run(self, task: str) -> dict:
        print(f"\n🧠 Manager analyzing task...")
        plan_response = self.manager.chat(task)
        print(f"\n📋 Plan:\n{plan_response}\n")

        instructions = self._parse_plan(plan_response)
        results = {}

        for agent_name, instruction in instructions.items():
            if instruction.upper() == "SKIP":
                continue

            print(f"\n⚡ {agent_name.capitalize()} working...")
            
            # Give each agent the original task + its specific instruction
            # + any results from previous agents for context
            context = f"Original task: {task}\n\nYour specific job: {instruction}"
            
            if results:
                context += "\n\nContext from other agents:\n"
                for name, result in results.items():
                    context += f"\n--- {name.upper()} OUTPUT ---\n{result}\n"

            result = self.agents[agent_name].chat(context)
            results[agent_name] = result
            print(f"✅ {agent_name.capitalize()} done.")

        # Manager combines everything
        print(f"\n🔗 Manager combining results...")
        combine_prompt = f"""
Original task: {task}

Results from specialists:
{self._format_results(results)}

Now combine these into one final, cohesive response for the user.
Be concise. Don't repeat everything — synthesize the key points.
"""
        final = self.manager.chat(combine_prompt)
        return {
            "plan": plan_response,
            "specialist_outputs": results,
            "final": final
        }

    def _parse_plan(self, plan: str) -> dict:
        instructions = {}
        for agent in ["researcher", "coder", "writer"]:
            pattern = rf"{agent.upper()}:\s*(.+?)(?=\n[A-Z]+:|$)"
            match = re.search(pattern, plan, re.IGNORECASE | re.DOTALL)
            if match:
                instructions[agent] = match.group(1).strip()
        return instructions

    def _format_results(self, results: dict) -> str:
        output = ""
        for name, result in results.items():
            output += f"\n--- {name.upper()} ---\n{result}\n"
        return output