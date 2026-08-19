# Request lifecycle

WM3 Request Protocol separates **request readiness** from **execution completion**.

```text
DRAFT
  ↓
contract validation
  ↓
BLOCKED ── resolve source/scope/criterion/authority issue ──┐
  │                                                        │
  └────────────────────────────────────────────────────────┘
  ↓
READY_WHEN
  ↓
execution by an authorised external process
  ↓
evidence collection
  ↓
review / acceptance decision outside this protocol validator
```

## DRAFT

The request is being authored. Required facts may still be missing.

## BLOCKED

A known issue prevents safe progression, for example:

- contradictory scope;
- unavailable/stale source of truth;
- non-falsifiable criterion;
- unresolved material unknown;
- missing approval authority.

## READY_WHEN

The request contract is sufficiently defined to state the conditions under which execution/publication may progress. It does **not** mean those conditions are already satisfied.

## Evidence and execution

An executor may use the V1 contract as input, but execution receipts, test results, diffs and runtime observations are produced later by other systems/processes.

## Contract changes during execution

If the problem, source of truth, material scope or acceptance meaning changes, update the request contract explicitly. Do not silently reinterpret it in the final PR.

## Indeterminate

If a criterion cannot decide because evidence is unavailable or contradictory, preserve the indeterminate state. The protocol is designed to make uncertainty visible, not to maximise green outcomes.
