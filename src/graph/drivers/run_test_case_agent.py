from src.graph.test_case_generator.graph import build_graph
from src.core import get_logger

logger = get_logger("test_case_driver")

def main():
    app = build_graph()
    
    # Initialize empty state
    init_state = {
        "requirement": "",
        "test_cases": [],
        "errors": []
    }
    
    final_state = app.invoke(init_state)
    
    # Show results
    logger.info(f"✅ Test Case Driver Pipeline complete!")
    logger.info(f"Generated {len(final_state.get('test_cases', []))} test cases")
    
    if final_state.get('errors'):
        logger.error(f"Errors: {final_state['errors']}")
        
if __name__ == "__main__":
    main()