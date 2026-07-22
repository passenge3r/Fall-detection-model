"""Run a project script with an isolated dependency directory first on sys.path."""

from __future__ import annotations

import argparse
import runpy
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--overlay", type=Path, required=True)
    parser.add_argument("script", type=Path)
    parser.add_argument("args", nargs=argparse.REMAINDER)
    options = parser.parse_args()

    overlay = options.overlay.resolve()
    if not overlay.is_dir():
        raise FileNotFoundError(f"Dependency overlay does not exist: {overlay}")
    sys.path.insert(0, str(overlay))
    sys.argv = [str(options.script), *options.args]
    runpy.run_path(str(options.script), run_name="__main__")


if __name__ == "__main__":
    main()
