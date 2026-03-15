from langgraph.graph import StateGraph, END
from .state import TestCaseState
from .nodes import read_requirement, generate_tests, save_outputs

def build_graph():
    workflow = StateGraph(TestCaseState)
    
    workflow.add_node("read", read_requirement)
    workflow.add_node("generate", generate_tests)
    workflow.add_node("save", save_outputs)
    
    workflow.set_entry_point("read")
    workflow.add_edge("read", "generate")
    workflow.add_edge("generate", "save")
    workflow.add_edge("save", END)
    
    return workflow.compile()