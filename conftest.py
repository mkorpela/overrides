import sys
from pathlib import Path
from typing import Optional


def pytest_ignore_collect(collection_path: Path) -> Optional[bool]:
    if sys.version_info[0] == 3 and sys.version_info[1] < 8:
        if str(collection_path.name).endswith("__py38.py"):
            return True
    return None
