from langgraph.graph import StateGraph, END
from .state import GreetingState
from .nodes import validate_name, generate_greeting, add_timestamp

def build_graph():
    # Create Graph
    workflow = StateGraph(GreetingState)
    
    # Add Nodes
    workflow.add_node("validate_name", validate_name)
    workflow.add_node("generate_greeting", generate_greeting)
    workflow.add_node("add_timestamp", add_timestamp)
    
    # Add Edges
    workflow.set_entry_point("validate_name")
    workflow.add_edge("validate_name", "generate_greeting")
    workflow.add_edge("generate_greeting", "add_timestamp")
    workflow.add_edge("add_timestamp", END)
    
    # Compile Graph
    return workflow.compile()