from typing import Dict


def generate_initial_score(problem_title: str) -> Dict:
    """
    Stub scoring engine.
    Later: evaluate candidate answers + LLM rubric scoring.
    """

    # All zero initially — candidate hasn't answered yet
    return {
        "problem": problem_title,
        "rubric_scores": {
            "requirements": 0,
            "api_design": 0,
            "data_model": 0,
            "scalability": 0,
            "reliability": 0,
            "observability": 0,
            "security": 0,
            "tradeoffs": 0,
        },
        "overall_score": 0,
        "max_score": 40,
        "feedback": "No answers evaluated yet.",
    }
