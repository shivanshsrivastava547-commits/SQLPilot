"""Analysis package for SQLPilot."""

from analysis.evidence import create_evidence_entry
from analysis.explore import build_explore_findings
from analysis.hypothesis import build_hypotheses, evaluate_hypothesis
from analysis.intelligence import detect_anomalies, summarize_data_quality
from analysis.metrics import determine_trend, percentage_change
from analysis.proactive import build_proactive_insights
from analysis.reliability import build_reliability_report
from analysis.resilience import handle_result_error, normalize_result_payload
from analysis.result_analyzer import analyze_query_result

__all__ = [
    "analyze_query_result",
    "build_explore_findings",
    "build_hypotheses",
    "build_proactive_insights",
    "build_reliability_report",
    "create_evidence_entry",
    "determine_trend",
    "detect_anomalies",
    "evaluate_hypothesis",
    "handle_result_error",
    "normalize_result_payload",
    "percentage_change",
    "summarize_data_quality",
]
