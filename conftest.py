# pytest root conftest — makes src/ importable from tests
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
