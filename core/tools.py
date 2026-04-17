from datetime import datetime

def get_current_datetime(input: str = "") -> str:
    now = datetime.now()
    return now.strftime("%A, %B %d, %Y at %I:%M %p")

def calculate(expression: str) -> str:
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

TOOLS = {
    "get_current_datetime": {
        "function": get_current_datetime,
        "description": "Returns the current date and time. Use when user asks about time or date.",
        "parameters": {}
    },
    "calculate": {
        "function": calculate,
        "description": "Evaluates a math expression. Use for any calculations.",
        "parameters": {"expression": "the math expression to evaluate"}
    }
}

def run_tool(name: str, params: dict) -> str:
    if name not in TOOLS:
        return f"Tool '{name}' not found."
    tool = TOOLS[name]
    return tool["function"](**params)