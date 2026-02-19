from pathlib import Path


def load_instructions(relative_path: str) -> str:
    """
    Loads an agent instructions markdown file from the app directory.
    """
    base_dir = Path(__file__).resolve().parent  # backend/app/agents
    instructions_path = base_dir / relative_path
    return instructions_path.read_text(encoding="utf-8")
