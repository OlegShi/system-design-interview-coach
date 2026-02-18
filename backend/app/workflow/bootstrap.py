from app.domain.models import Event, Session


def bootstrap_session(session: Session) -> Session:
    # system created
    session.events.append(Event(type="system", content="Session created"))

    # constitution
    session.events.append(Event(type="constitution_started", content="Defining interview principles"))
    session.events.append(
        Event(
            type="constitution_completed",
            content="Interview principles defined",
            payload={
                "principles": [
                    "Start with requirements and constraints (functional + non-functional).",
                    "State traffic assumptions (QPS, payload size, read/write ratio).",
                    "Design APIs and data model early.",
                    "Address scalability and bottlenecks (CPU, I/O, DB, network).",
                    "Discuss consistency tradeoffs and failure modes.",
                    "Include observability (metrics/logs/tracing) and SLOs.",
                    "Call out security and data privacy when relevant.",
                    "Be explicit about tradeoffs (cost vs latency vs correctness).",
                ],
                "rubric": {
                    "requirements": 0,
                    "api_design": 0,
                    "data_model": 0,
                    "scalability": 0,
                    "reliability": 0,
                    "observability": 0,
                    "security": 0,
                    "tradeoffs": 0,
                },
                "scoring_scale": {"min": 0, "max": 5, "meaning": "0=missing, 3=adequate, 5=excellent"},
            },
        )
    )

    # specify
    session.events.append(Event(type="specify_started", content="Defining problem statement and constraints"))
    session.events.append(
        Event(
            type="specify_completed",
            content="Problem specification defined",
            payload={
                "problem_statement": session.title,
                "assumptions": {
                    "qps": 1000,
                    "read_write_ratio": "80/20",
                    "average_payload_kb": 2,
                    "availability_target": "99.9%",
                    "region": "multi-region",
                },
                "non_functional_requirements": [
                    "Low latency (<100ms p95)",
                    "Horizontal scalability",
                    "Graceful degradation under load",
                ],
                "constraints": [
                    "Use commodity cloud infrastructure",
                    "Assume eventual consistency is acceptable",
                ],
            },
        )
    )
    
     # plan
    session.events.append(Event(type="plan_started", content="Creating architecture plan outline"))
    session.events.append(
        Event(
            type="plan_completed",
            content="Architecture plan outline created",
            payload={
                "sections": [
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
                ],
                "high_level_components": [
                    {"name": "API Gateway", "responsibility": "Routing, auth, rate limiting"},
                    {"name": "Core Service", "responsibility": "Business logic and orchestration"},
                    {"name": "Database", "responsibility": "Durable state"},
                    {"name": "Cache", "responsibility": "Hot data + rate limit counters"},
                    {"name": "Queue", "responsibility": "Async processing and retries"},
                    {"name": "Observability Stack", "responsibility": "Metrics, logs, traces"},
                ],
            },
        )
    )


    return session
