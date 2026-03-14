"""
Convenience entry-point so the backend can be started with:

    python main.py
    # or
    uv run main.py

The real FastAPI application lives in app/main.py and is the target for uvicorn:

    uvicorn app.main:app --reload
"""

import uvicorn


def main() -> None:
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
