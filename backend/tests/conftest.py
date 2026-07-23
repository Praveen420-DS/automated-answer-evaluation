import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = ROOT / "backend"
for path in (ROOT, BACKEND_ROOT):
    if str(path) in sys.path:
        sys.path.remove(str(path))
    sys.path.insert(0, str(path))
