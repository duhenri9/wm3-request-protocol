#!/usr/bin/env python3
"""Repository-level consistency checks for WM3 Request Protocol V1."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "tools" / "validate_request.py"
SPEC = importlib.util.spec_from_file_location("wm3_request_validator", VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)

LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def check_json_files(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            errors.append(f"invalid JSON {path.relative_to(ROOT)}: {error}")


def check_schema_vocabulary(errors: list[str]) -> None:
    schema_path = ROOT / "schema" / "request.v1.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    required = tuple(schema.get("required", []))
    if required != validator.REQUIRED_FIELDS:
        errors.append(
            "schema required fields drifted from validator: "
            f"schema={required!r} validator={validator.REQUIRED_FIELDS!r}"
        )
    properties = set(schema.get("properties", {}))
    if properties != validator.ALLOWED_TOP_LEVEL:
        errors.append(
            "schema top-level properties drifted from validator: "
            f"schema={sorted(properties)!r} validator={sorted(validator.ALLOWED_TOP_LEVEL)!r}"
        )


def check_exposed_vocabulary(errors: list[str]) -> None:
    checks = {
        "templates/request.md": (
            "Request ID",
            "Protocol version",
            "Context",
            "Problem",
            "Source of truth",
            "In scope",
            "Out of scope",
            "Acceptance criteria",
            "Verification evidence",
            "Risks",
            "Unknowns",
            "Approval authority",
            "Publication gate",
        ),
        ".github/ISSUE_TEMPLATE/change-request.yml": (
            "request_id",
            "context",
            "problem",
            "source_of_truth",
            "in_scope",
            "out_of_scope",
            "acceptance_criteria",
            "verification_evidence",
            "risks",
            "unknowns",
            "approval_authority",
            "publication_gate_state",
            "publication_gate_conditions",
        ),
        ".github/pull_request_template.md": (
            "Request ID",
            "Protocol version",
            "Problem",
            "In scope",
            "Out of scope",
            "Acceptance observations",
            "Verification evidence",
            "Publication gate",
        ),
    }
    for relative, required_tokens in checks.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        for token in required_tokens:
            if token not in text:
                errors.append(f"{relative} missing V1 vocabulary token: {token}")


def check_markdown_links(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for raw_target in LINK.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(
                    f"{path.relative_to(ROOT)} link escapes repository: {raw_target}"
                )
                continue
            if not resolved.exists():
                errors.append(
                    f"{path.relative_to(ROOT)} has broken local link: {raw_target}"
                )


def main() -> int:
    errors: list[str] = []
    check_json_files(errors)
    check_schema_vocabulary(errors)
    check_exposed_vocabulary(errors)
    check_markdown_links(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("repository V1 consistency checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
