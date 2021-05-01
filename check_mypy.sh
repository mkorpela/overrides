#!/bin/bash -x
set -e
mypy mypy_fails | grep "Found 3 errors in 2 files (checked 2 source files)"
mypy mypy_passes