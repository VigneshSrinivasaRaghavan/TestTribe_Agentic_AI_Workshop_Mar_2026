"""
Driver for Log Analyzer with RAG + Memory
"""
from src.graph.log_analyzer_memory.graph import build_graph
from src.core import get_logger

logger = get_logger("log_analyzer_memory_driver")

def main():
    logger.info("🚀 Starting Log Analyzer with RAG + Memory...")

    # Build graph
    app = build_graph()

    # Initialize state
    init_state = {
        "log_content": "",
        "retrieved_context": "",
        "conversation_history": [],       # NEW
        "past_incidents": "",             # NEW
        "analysis_text": "",
        "analysis_json": {},
        "executive_summary": "",
        "errors": []
    }

    # Run pipeline
    final_state = app.invoke(init_state)

    # Show results
    logger.info(f"✅ Pipeline complete!")

    if final_state.get('errors'):
        logger.error(f"Errors: {final_state['errors']}")
    else:
        logger.info("Generated 3 reports: text, JSON, executive summary")

if __name__ == "__main__":
    main()
