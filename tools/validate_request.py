#!/usr/bin/env python3
"""Dependency-free semantic validator for WM3 Request Protocol V1.

This is intentionally not a complete JSON Schema implementation. The JSON Schema
is the interchange contract; this linter enforces the repository's bounded V1
structural subset and protocol-specific semantic contradictions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

PROTOCOL_VERSION = "1.0"
ALLOWED_PROFILES = {"compact", "standard"}
ALLOWED_GATE_STATES = {"DRAFT", "BLOCKED", "READY_WHEN"}
REQUIRED_FIELDS = (
    "request_id",
    "protocol_version",
    "profile",
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
    "publication_gate",
)
ALLOWED_TOP_LEVEL = set(REQUIRED_FIELDS) | {
    "assumptions",
    "reversibility",
    "data_privacy",
}
VAGUE_OUTCOMES = {
    "bug fixed",
    "bug corrigido",
    "fixed",
    "corrigido",
    "done",
    "pronto",
    "works",
    "funciona",
    "improved",
    "melhorado",
    "better",
    "melhor",
}


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    message: str


@dataclass(frozen=True)
class ValidationReport:
    schema: str
    outcome: str
    protocol_version: str | None
    request_id: str | None
    findings: list[Finding]
    request_sha256: str
    report_sha256: str
    claim_boundary: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["findings"] = [asdict(item) for item in self.findings]
        return payload


CLAIM_BOUNDARY = (
    "VALID means the document passed the bounded WM3 Request Protocol V1 structural "
    "and semantic lint rules implemented by this tool. It does not prove that the "
    "request is safe, complete in every domain, authorised, executed or successfully delivered."
)


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def normalize_scope(value: str) -> str:
    return " ".join(value.casefold().split())


def add(findings: list[Finding], code: str, path: str, message: str) -> None:
    findings.append(Finding(code=code, path=path, message=message))


def validate_string_list(
    document: dict[str, Any],
    field: str,
    findings: list[Finding],
    *,
    minimum: int = 0,
) -> list[str]:
    value = document.get(field)
    if not isinstance(value, list):
        add(findings, "INVALID_TYPE", f"$.{field}", f"{field} must be an array")
        return []
    if len(value) < minimum:
        add(
            findings,
            "MIN_ITEMS",
            f"$.{field}",
            f"{field} must contain at least {minimum} item(s)",
        )
    result: list[str] = []
    for index, item in enumerate(value):
        if not non_empty_string(item):
            add(
                findings,
                "INVALID_STRING",
                f"$.{field}[{index}]",
                "value must be a non-empty string",
            )
        else:
            result.append(item)
    if len({normalize_scope(item) for item in result}) != len(result):
        add(findings, "DUPLICATE_VALUE", f"$.{field}", f"{field} contains duplicates")
    return result


def validate_sources(document: dict[str, Any], findings: list[Finding]) -> None:
    value = document.get("source_of_truth")
    if not isinstance(value, list):
        add(
            findings,
            "INVALID_TYPE",
            "$.source_of_truth",
            "source_of_truth must be an array",
        )
        return
    if not value:
        add(
            findings,
            "MISSING_SOURCE_OF_TRUTH",
            "$.source_of_truth",
            "at least one source of truth is required",
        )
        return
    for index, source in enumerate(value):
        path = f"$.source_of_truth[{index}]"
        if not isinstance(source, dict):
            add(findings, "INVALID_TYPE", path, "source must be an object")
            continue
        extra = set(source) - {"kind", "ref", "identity"}
        if extra:
            add(
                findings,
                "UNKNOWN_FIELD",
                path,
                f"unknown source field(s): {', '.join(sorted(extra))}",
            )
        for field in ("kind", "ref"):
            if not non_empty_string(source.get(field)):
                add(
                    findings,
                    "MISSING_FIELD",
                    f"{path}.{field}",
                    f"source {field} is required",
                )
        if "identity" in source and not non_empty_string(source["identity"]):
            add(
                findings,
                "INVALID_STRING",
                f"{path}.identity",
                "identity must be a non-empty string when provided",
            )


def validate_criteria(document: dict[str, Any], findings: list[Finding]) -> None:
    value = document.get("acceptance_criteria")
    if not isinstance(value, list):
        add(
            findings,
            "INVALID_TYPE",
            "$.acceptance_criteria",
            "acceptance_criteria must be an array",
        )
        return
    if not value:
        add(
            findings,
            "MISSING_ACCEPTANCE_CRITERIA",
            "$.acceptance_criteria",
            "at least one acceptance criterion is required",
        )
        return

    ids: set[str] = set()
    allowed = {
        "id",
        "observation_scope",
        "expected_outcome",
        "verification",
        "valid_alternatives",
        "indeterminate_when",
    }
    for index, criterion in enumerate(value):
        path = f"$.acceptance_criteria[{index}]"
        if not isinstance(criterion, dict):
            add(findings, "INVALID_TYPE", path, "criterion must be an object")
            continue
        extra = set(criterion) - allowed
        if extra:
            add(
                findings,
                "UNKNOWN_FIELD",
                path,
                f"unknown criterion field(s): {', '.join(sorted(extra))}",
            )
        for field in ("id", "observation_scope", "expected_outcome", "verification"):
            if not non_empty_string(criterion.get(field)):
                add(
                    findings,
                    "MISSING_FIELD",
                    f"{path}.{field}",
                    f"criterion {field} is required",
                )

        criterion_id = criterion.get("id")
        if non_empty_string(criterion_id):
            if criterion_id in ids:
                add(
                    findings,
                    "DUPLICATE_ID",
                    f"{path}.id",
                    f"duplicate acceptance criterion id: {criterion_id}",
                )
            ids.add(criterion_id)

        expected = criterion.get("expected_outcome")
        if non_empty_string(expected) and expected.strip().casefold().rstrip(".!?") in VAGUE_OUTCOMES:
            add(
                findings,
                "AMBIGUOUS_ACCEPTANCE",
                f"{path}.expected_outcome",
                "expected_outcome is tautological or too vague to falsify",
            )

        for optional_list in ("valid_alternatives", "indeterminate_when"):
            if optional_list not in criterion:
                continue
            items = criterion[optional_list]
            if not isinstance(items, list):
                add(
                    findings,
                    "INVALID_TYPE",
                    f"{path}.{optional_list}",
                    f"{optional_list} must be an array",
                )
                continue
            for item_index, item in enumerate(items):
                if not non_empty_string(item):
                    add(
                        findings,
                        "INVALID_STRING",
                        f"{path}.{optional_list}[{item_index}]",
                        "value must be a non-empty string",
                    )


def validate_evidence(document: dict[str, Any], findings: list[Finding]) -> None:
    value = document.get("verification_evidence")
    if not isinstance(value, list):
        add(
            findings,
            "INVALID_TYPE",
            "$.verification_evidence",
            "verification_evidence must be an array",
        )
        return
    if not value:
        add(
            findings,
            "MISSING_VERIFICATION_EVIDENCE",
            "$.verification_evidence",
            "at least one verification-evidence requirement is required",
        )
        return

    ids: set[str] = set()
    for index, evidence in enumerate(value):
        path = f"$.verification_evidence[{index}]"
        if not isinstance(evidence, dict):
            add(findings, "INVALID_TYPE", path, "evidence entry must be an object")
            continue
        extra = set(evidence) - {"id", "kind", "required", "how"}
        if extra:
            add(
                findings,
                "UNKNOWN_FIELD",
                path,
                f"unknown evidence field(s): {', '.join(sorted(extra))}",
            )
        for field in ("id", "kind", "how"):
            if not non_empty_string(evidence.get(field)):
                add(
                    findings,
                    "MISSING_FIELD",
                    f"{path}.{field}",
                    f"evidence {field} is required",
                )
        if not isinstance(evidence.get("required"), bool):
            add(
                findings,
                "INVALID_TYPE",
                f"{path}.required",
                "required must be a boolean",
            )
        evidence_id = evidence.get("id")
        if non_empty_string(evidence_id):
            if evidence_id in ids:
                add(
                    findings,
                    "DUPLICATE_ID",
                    f"{path}.id",
                    f"duplicate evidence id: {evidence_id}",
                )
            ids.add(evidence_id)


def validate_gate(document: dict[str, Any], findings: list[Finding]) -> None:
    gate = document.get("publication_gate")
    if not isinstance(gate, dict):
        add(
            findings,
            "INVALID_TYPE",
            "$.publication_gate",
            "publication_gate must be an object",
        )
        return
    extra = set(gate) - {"state", "conditions"}
    if extra:
        add(
            findings,
            "UNKNOWN_FIELD",
            "$.publication_gate",
            f"unknown publication gate field(s): {', '.join(sorted(extra))}",
        )
    state = gate.get("state")
    if state not in ALLOWED_GATE_STATES:
        add(
            findings,
            "INVALID_GATE_STATE",
            "$.publication_gate.state",
            f"state must be one of {sorted(ALLOWED_GATE_STATES)}",
        )
    conditions = gate.get("conditions")
    if not isinstance(conditions, list) or not conditions:
        add(
            findings,
            "MISSING_GATE_CONDITION",
            "$.publication_gate.conditions",
            "publication gate requires at least one condition",
        )
    elif any(not non_empty_string(item) for item in conditions):
        add(
            findings,
            "INVALID_STRING",
            "$.publication_gate.conditions",
            "every publication-gate condition must be a non-empty string",
        )


def validate_document(document: Any) -> list[Finding]:
    findings: list[Finding] = []
    if not isinstance(document, dict):
        return [Finding("INVALID_TYPE", "$", "request must be a JSON object")]

    for field in REQUIRED_FIELDS:
        if field not in document:
            add(findings, "MISSING_FIELD", f"$.{field}", f"required field {field} is missing")

    extra = set(document) - ALLOWED_TOP_LEVEL
    if extra:
        add(
            findings,
            "UNKNOWN_FIELD",
            "$",
            f"unknown top-level field(s): {', '.join(sorted(extra))}",
        )

    for field in ("request_id", "context", "problem"):
        if field in document and not non_empty_string(document[field]):
            add(findings, "INVALID_STRING", f"$.{field}", f"{field} must be a non-empty string")

    if document.get("protocol_version") != PROTOCOL_VERSION:
        add(
            findings,
            "UNSUPPORTED_PROTOCOL_VERSION",
            "$.protocol_version",
            f"protocol_version must be {PROTOCOL_VERSION}",
        )
    if document.get("profile") not in ALLOWED_PROFILES:
        add(
            findings,
            "INVALID_PROFILE",
            "$.profile",
            f"profile must be one of {sorted(ALLOWED_PROFILES)}",
        )

    validate_sources(document, findings)
    in_scope = validate_string_list(document, "in_scope", findings, minimum=1)
    out_scope = validate_string_list(document, "out_of_scope", findings)
    overlap = sorted(
        {normalize_scope(item) for item in in_scope}
        & {normalize_scope(item) for item in out_scope}
    )
    if overlap:
        add(
            findings,
            "SCOPE_CONTRADICTION",
            "$",
            "the same normalized scope appears in both in_scope and out_of_scope: "
            + ", ".join(overlap),
        )

    validate_criteria(document, findings)
    validate_evidence(document, findings)
    validate_string_list(document, "risks", findings)
    validate_string_list(document, "unknowns", findings)
    validate_string_list(document, "approval_authority", findings, minimum=1)
    validate_gate(document, findings)

    for optional_list in ("assumptions",):
        if optional_list in document:
            validate_string_list(document, optional_list, findings)
    for optional_string in ("reversibility", "data_privacy"):
        if optional_string in document and not non_empty_string(document[optional_string]):
            add(
                findings,
                "INVALID_STRING",
                f"$.{optional_string}",
                f"{optional_string} must be a non-empty string when provided",
            )

    return sorted(findings, key=lambda item: (item.path, item.code, item.message))


def make_report(document: Any, findings: list[Finding]) -> ValidationReport:
    request_digest = sha256(document)
    unsigned = {
        "schema": "wm3-request-protocol.validation.v1",
        "outcome": "VALID" if not findings else "INVALID",
        "protocol_version": document.get("protocol_version") if isinstance(document, dict) else None,
        "request_id": document.get("request_id") if isinstance(document, dict) else None,
        "findings": [asdict(item) for item in findings],
        "request_sha256": request_digest,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return ValidationReport(
        schema=unsigned["schema"],
        outcome=unsigned["outcome"],
        protocol_version=unsigned["protocol_version"],
        request_id=unsigned["request_id"],
        findings=findings,
        request_sha256=request_digest,
        report_sha256=sha256(unsigned),
        claim_boundary=CLAIM_BOUNDARY,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path, help="V1 request JSON file")
    parser.add_argument("--report", type=Path, help="write deterministic validation report")
    parser.add_argument(
        "--expect-code",
        action="append",
        default=[],
        help="assert that at least one finding with this code is emitted",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        document = json.loads(args.request.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"request-protocol: unable to read request: {error}", file=sys.stderr)
        return 3

    findings = validate_document(document)
    report = make_report(document, findings)
    payload = report.to_dict()
    rendered = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")

    emitted_codes = {item.code for item in findings}
    missing_expected = sorted(set(args.expect_code) - emitted_codes)
    if missing_expected:
        print(
            "request-protocol: expected finding code(s) not emitted: "
            + ", ".join(missing_expected),
            file=sys.stderr,
        )
        return 4

    return 0 if not findings else 2


if __name__ == "__main__":
    raise SystemExit(main())
