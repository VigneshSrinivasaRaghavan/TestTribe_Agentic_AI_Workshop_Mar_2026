from typing import TypedDict, List, Dict

class TestCaseState(TypedDict):
    requirements: str
    test_cases: List[Dict]
    error: List[str]