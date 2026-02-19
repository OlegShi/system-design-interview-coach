from typing import Dict, List


def generate_interview_tasks(problem_title: str) -> Dict:
    """
    Generates structured system design interview tasks
    based on the problem statement.
    """

    tasks: List[Dict] = [
        {
            "id": "requirements",
            "title": "Clarify Requirements",
            "question": f"What functional and non-functional requirements must '{problem_title}' satisfy?",
            "category": "requirements",
        },
        {
            "id": "api_design",
            "title": "Design the API",
            "question": "Design the main REST/gRPC endpoints. What are the request/response schemas?",
            "category": "api_design",
        },
        {
            "id": "data_model",
            "title": "Design the Data Model",
            "question": "What database schema would you use? What are the main entities and relationships?",
            "category": "data_model",
        },
        {
            "id": "scaling",
            "title": "Scaling Strategy",
            "question": "How would the system scale under increasing traffic? Where would bottlenecks appear?",
            "category": "scalability",
        },
        {
            "id": "reliability",
            "title": "Failure & Reliability",
            "question": "How do you handle failures, retries, and partial outages?",
            "category": "reliability",
        },
        {
            "id": "tradeoffs",
            "title": "Tradeoffs",
            "question": "What are the main tradeoffs in your design (consistency vs latency vs cost)?",
            "category": "tradeoffs",
        },
    ]

    return {
        "problem": problem_title,
        "tasks": tasks,
        "total": len(tasks),
    }
