"""conftest.py — CircuitPython stubs and sys.path setup for firmware desktop tests."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

# Make firmware modules importable as e.g. `from sensors.base import LineSensor`
sys.path.insert(0, str(Path(__file__).parent.parent))

# Stub CircuitPython-only modules before any firmware import
for _mod in ['busio', 'digitalio', 'board', 'analogio', 'microcontroller']:
    if _mod not in sys.modules:
        sys.modules[_mod] = MagicMock()
