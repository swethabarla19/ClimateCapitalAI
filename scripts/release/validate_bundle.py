#!/usr/bin/env python3
"""Validate a ClimateCapital four-file bundle; reviewed release is the default."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPOSITORY_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from climatecapital.contracts.common import ReleaseTier  # noqa: E402
from climatecapital.release.validator import (  # noqa: E402
    BundleValidationError,
    validate_bundle,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle_directory", type=Path)
    parser.add_argument(
        "--manifest-sha256",
        required=True,
        help="external lowercase SHA-256 of the exact manifest.json bytes",
    )
    parser.add_argument(
        "--development-fixture",
        action="store_true",
        help="validate FIXTURE tier for local development; never release eligible",
    )
    args = parser.parse_args()
    expected_tier = (
        ReleaseTier.FIXTURE if args.development_fixture else ReleaseTier.REVIEWED_RELEASE
    )
    try:
        bundle = validate_bundle(
            args.bundle_directory,
            manifest_sha256=args.manifest_sha256,
            expected_release_tier=expected_tier,
        )
    except BundleValidationError as error:
        for violation in error.violations:
            print(
                f"{violation.code}\t{violation.path}\t{violation.message}",
                file=sys.stderr,
            )
        return 1
    print(
        "bundle valid: "
        f"tier={bundle.manifest.release_tier} "
        f"data_version={bundle.manifest.data_version} "
        f"manifest_sha256={bundle.manifest_sha256}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
