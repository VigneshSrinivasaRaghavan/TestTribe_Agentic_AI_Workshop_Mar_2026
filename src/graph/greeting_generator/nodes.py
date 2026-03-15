from datetime import datetime
from .state import GreetingState

def validate_name(state:GreetingState) -> GreetingState:
    nameOutput = state["name"].strip()
    is_valid_value = len(nameOutput) > 0 and nameOutput.isalpha()
    return {"is_valid": is_valid_value}

def generate_greeting(state: GreetingState) -> GreetingState:
    """Generate personalized greeting."""
    name = state["name"]
    greeting = f"Hello, {name}! Welcome to LangGraph!"
    return {"greeting": greeting}

def add_timestamp(state: GreetingState) -> GreetingState:
    """Add current timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"timestamp": timestamp}
