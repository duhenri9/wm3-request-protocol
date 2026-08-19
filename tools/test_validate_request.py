from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "validate_request.py"
SPEC = importlib.util.spec_from_file_location("validate_request", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)

FIXTURES = ROOT / "examples" / "machine-readable"


def load(name: str) -> dict[str, object]:
    payload = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


class RequestProtocolV1ValidatorTests(unittest.TestCase):
    def codes(self, name: str) -> set[str]:
        return {item.code for item in validator.validate_document(load(name))}

    def test_valid_request_passes(self) -> None:
        document = load("valid-request.json")
        findings = validator.validate_document(document)
        self.assertEqual(findings, [])
        first = validator.make_report(document, findings)
        second = validator.make_report(document, findings)
        self.assertEqual(first.outcome, "VALID")
        self.assertEqual(first.request_sha256, second.request_sha256)
        self.assertEqual(first.report_sha256, second.report_sha256)

    def test_missing_source_of_truth_is_rejected(self) -> None:
        self.assertIn(
            "MISSING_SOURCE_OF_TRUTH",
            self.codes("invalid-missing-source.json"),
        )

    def test_tautological_acceptance_is_rejected(self) -> None:
        self.assertIn(
            "AMBIGUOUS_ACCEPTANCE",
            self.codes("invalid-ambiguous-acceptance.json"),
        )

    def test_scope_contradiction_is_case_insensitive(self) -> None:
        self.assertIn(
            "SCOPE_CONTRADICTION",
            self.codes("invalid-scope-contradiction.json"),
        )

    def test_unknown_top_level_field_is_rejected(self) -> None:
        document = load("valid-request.json")
        document["executor_says_done"] = True
        codes = {item.code for item in validator.validate_document(document)}
        self.assertIn("UNKNOWN_FIELD", codes)

    def test_validator_does_not_treat_required_evidence_as_collected_evidence(self) -> None:
        document = load("valid-request.json")
        report = validator.make_report(document, validator.validate_document(document))
        self.assertIn("does not prove", report.claim_boundary)
        self.assertNotIn("ACCEPTED", report.outcome)


if __name__ == "__main__":
    unittest.main()
