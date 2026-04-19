import argparse
from core.orchestrator import Orchestrator

def main():
    parser = argparse.ArgumentParser(description="AgentOS Multi-Agent System")
    parser.add_argument("--task", required=True, help="Task to delegate to agents")
    args = parser.parse_args()

    orchestrator = Orchestrator()
    result = orchestrator.run(args.task)

    print("\n" + "="*60)
    print("FINAL RESULT")
    print("="*60)
    print(result["final"])
    print("="*60 + "\n")

if __name__ == "__main__":
    main()