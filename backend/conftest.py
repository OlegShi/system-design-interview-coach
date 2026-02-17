import sys
from pathlib import Path

# Add the backend folder to PYTHONPATH so "import app" works consistently
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
