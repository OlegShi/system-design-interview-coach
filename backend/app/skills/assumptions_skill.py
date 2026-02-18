from typing import Dict


def generate_default_assumptions(problem_title: str) -> Dict:
    """
    Deterministic assumptions generator (stub).
    Later: LLM-driven + configurable presets.
    """
    title = problem_title.lower()

    # simple heuristics to look smart in demos
    if "rate limiter" in title:
        return {
            "qps": 50000,
            "read_write_ratio": "90/10",
            "average_payload_kb": 1,
            "availability_target": "99.99%",
            "region": "multi-region",
        }

    if "chat" in title or "messaging" in title:
        return {
            "qps": 20000,
            "read_write_ratio": "50/50",
            "average_payload_kb": 4,
            "availability_target": "99.9%",
            "region": "multi-region",
        }

    # default
    return {
        "qps": 1000,
        "read_write_ratio": "80/20",
        "average_payload_kb": 2,
        "availability_target": "99.9%",
        "region": "single-region",
    }
