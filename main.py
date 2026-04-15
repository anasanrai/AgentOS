import argparse
from core.runner import AgentRunner

def main():
    parser = argparse.ArgumentParser(description="AgentOS - Run AI agents from YAML")
    parser.add_argument("--agent", required=True, help="Path to agent YAML file")
    args = parser.parse_args()

    agent = AgentRunner(args.agent)
    
    print(f"\n🤖 Agent '{agent.name}' is ready. Type 'exit' to quit.\n")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye.")
            break
        if not user_input:
            continue
        response = agent.chat(user_input)
        print(f"\nAgent: {response}\n")

if __name__ == "__main__":
    main()