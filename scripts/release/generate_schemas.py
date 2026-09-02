#!/usr/bin/env python3
"""Generate or verify the tracked M1 JSON Schemas."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPOSITORY_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from climatecapital.contracts.schema_export import SCHEMA_EXPORTS, export_schemas  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail unless every tracked schema exactly matches the contract models",
    )
    args = parser.parse_args()
    output_dir = REPOSITORY_ROOT / "contracts" / "schemas"
    try:
        paths = export_schemas(output_dir, check=args.check)
    except (OSError, ValueError) as error:
        parser.exit(1, f"schema export failed: {error}\n")
    action = "verified" if args.check else "generated"
    print(f"{action} {len(SCHEMA_EXPORTS)} schemas in {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
