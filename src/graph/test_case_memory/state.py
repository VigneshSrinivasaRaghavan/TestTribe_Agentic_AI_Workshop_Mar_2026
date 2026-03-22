from typing import TypedDict, List, Dict

class TestCaseState(TypedDict):
    requirements: str
    retrieved_context: str
    conversation_history: List[Dict]
    past_patterns: str
    test_cases: List[Dict]
    error: List[str]
    validation_status: str # "pass" | "fail"
    retry_count: int
    human_approval: str # "pending" | "approved" | "rejected
    human_feedback: str