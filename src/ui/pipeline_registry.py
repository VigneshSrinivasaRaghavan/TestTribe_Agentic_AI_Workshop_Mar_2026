"""
Pipeline registry — defines which pipelines are available in the UI.
Add a new PipelineConfig entry to PIPELINE_REGISTRY to expose a pipeline.
"""
from dataclasses import dataclass
from typing import Callable
from src.graph.incident_response.graph import build_incident_response_graph
from src.graph.jira_testrail_slack.graph import build_graph

@dataclass
class PipelineConfig:
    name: str
    input_type: str        # "log" | "jira_key"
    description: str
    run_fn: Callable

def run_incident_response(log_content: str) -> dict:
    graph = build_incident_response_graph()
    return graph.invoke({
        "log_content": log_content,
        "next_agent": "",
        "log_analysis": None,
        "root_cause": None,
        "solution": None,
        "incident_report": "",
        "steps_completed": [],
        "errors": [],
    })

def run_jira_testrail_slack(jira_key: str) -> dict:
    graph = build_graph()
    return graph.invoke({
        "jira_key": jira_key,
        "next_agent": "",
        "jira_summary": None,
        "jira_description": None,
        "test_cases": None,
        "testrail_case_ids": None,
        "slack_message_ts": None,
        "retrieved_context": None,
        "past_patterns": None,
        "conversation_history": None,
        "summary_report": "",
        "steps_completed": [],
        "errors": [],
    })

PIPELINE_REGISTRY: list[PipelineConfig] = [
    PipelineConfig(
        name="Incident Response",
        input_type="log",
        description="Analyze log content and generate an incident report.",
        run_fn=run_incident_response
    ),
    PipelineConfig(
    name="Jira → TestRail → Slack",
    input_type="jira_key",
    description="Fetch a Jira ticket, generate test cases, push to TestRail, notify Slack.",
    run_fn=run_jira_testrail_slack,
),
]