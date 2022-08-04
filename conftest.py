import sys
from typing import Optional

import py


def pytest_ignore_collect(path: py.path.local, config: "Config") -> Optional[bool]:
    if sys.version_info[0] == 3 and sys.version_info[1] < 8:
        if str(path).endswith("__py38.py"):
            return True
    return None
