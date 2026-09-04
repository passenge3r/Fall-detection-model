from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))

from app.webapp import app


def main() -> None:
    target = PROJECT / "openapi.json"
    target.write_text(
        json.dumps(app.openapi(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(target)


if __name__ == "__main__":
    main()
