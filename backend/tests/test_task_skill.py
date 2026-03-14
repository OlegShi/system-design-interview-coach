"""Tests for the task generation skill."""

from app.skills.task_skill import generate_interview_tasks


def test_generates_correct_structure():
    result = generate_interview_tasks("Design a chat system")
    assert "tasks" in result
    assert "total" in result
    assert "problem" in result
    assert result["problem"] == "Design a chat system"


def test_generates_six_tasks():
    result = generate_interview_tasks("Design a URL shortener")
    assert result["total"] == 6
    assert len(result["tasks"]) == 6


def test_each_task_has_required_fields():
    result = generate_interview_tasks("Design X")
    for task in result["tasks"]:
        assert "id" in task
        assert "title" in task
        assert "question" in task
        assert "category" in task


def test_task_ids_are_unique():
    result = generate_interview_tasks("Design X")
    ids = [t["id"] for t in result["tasks"]]
    assert len(ids) == len(set(ids))


def test_expected_categories():
    result = generate_interview_tasks("Design X")
    categories = {t["category"] for t in result["tasks"]}
    expected = {"requirements", "api_design", "data_model", "scalability", "reliability", "tradeoffs"}
    assert categories == expected
