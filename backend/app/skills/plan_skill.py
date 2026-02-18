from typing import Dict, List


def generate_plan_outline(problem_title: str) -> Dict:
    """
    Generates a structured architecture plan outline
    for a given system design problem.
    """

    sections: List[str] = [
        "Requirements & constraints recap",
        "High-level architecture",
        "API design",
        "Data model",
        "Scaling strategy",
        "Caching strategy",
        "Consistency & transactions",
        "Failure modes & resilience",
        "Observability (metrics/logs/tracing)",
        "Security & privacy",
        "Cost considerations",
        "Tradeoffs and alternatives",
    ]

    components = [
        {"name": "API Gateway", "responsibility": "Routing, auth, rate limiting"},
        {"name": "Core Service", "responsibility": "Business logic and orchestration"},
        {"name": "Database", "responsibility": "Durable state"},
        {"name": "Cache", "responsibility": "Hot data + rate limit counters"},
        {"name": "Queue", "responsibility": "Async processing and retries"},
        {"name": "Observability Stack", "responsibility": "Metrics, logs, traces"},
    ]

    return {
        "problem": problem_title,
        "sections": sections,
        "high_level_components": components,
    }
