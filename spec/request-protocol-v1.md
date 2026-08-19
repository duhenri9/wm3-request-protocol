# WM3 Request Protocol V1

Status: **release candidate specification** until the V1 merge/release gate is closed.

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** are normative requirements in this specification.

## 1. Purpose

WM3 Request Protocol defines a bounded contract for requested product/software work. It exists to make a request inspectable before execution: the problem, source of truth, scope, acceptance observations, evidence requirements and publication authority are explicit.

The protocol does **not** execute work and does not certify that work succeeded.

```text
request intent
    ↓
problem + source of truth
    ↓
in scope / out of scope
    ↓
observable acceptance criteria
    ↓
required verification evidence
    ↓
risks + unknowns + authority
    ↓
publication gate
```

## 2. Profiles

V1 defines two authoring profiles using the same vocabulary:

- `compact` — small, low-risk changes; fields may be concise but required fields remain required.
- `standard` — default for material product/software changes.

A profile MUST NOT remove the source-of-truth, scope, acceptance, evidence or authority boundary.

## 3. Required request fields

A V1 request MUST contain:

- `request_id` — stable request identity;
- `protocol_version` — exactly `1.0` for this specification;
- `profile` — `compact` or `standard`;
- `context` — relevant current state;
- `problem` — the problem before a proposed implementation;
- `source_of_truth[]` — one or more references that constrain the request;
- `in_scope[]` — explicit allowed/requested outcomes or surfaces;
- `out_of_scope[]` — explicit protected boundaries (may be empty only when genuinely none are known);
- `acceptance_criteria[]` — falsifiable observable criteria;
- `verification_evidence[]` — checks/artifacts required to support acceptance;
- `risks[]` — known material failure modes (may be empty after deliberate review);
- `unknowns[]` — unresolved facts (may be empty after deliberate review);
- `approval_authority[]` — roles/identities allowed to approve the relevant publication/merge decision;
- `publication_gate` — current gate state and conditions.

Optional V1 fields include `assumptions`, `reversibility` and `data_privacy`.

## 4. Source of truth

Each source-of-truth entry MUST contain:

- `kind` — for example `commit`, `url`, `document`, `decision`, `production-behaviour`, `design`;
- `ref` — a human-resolvable reference;
- `identity` — exact version/SHA/date/revision when one exists.

A mutable URL SHOULD include an immutable identity or retrieval/version note when stale-state risk matters.

An executor MUST be allowed to report that a declared source of truth is unavailable, stale or contradictory. It MUST NOT silently substitute a different source.

## 5. Scope

`in_scope` defines what the request authorises or asks to change/observe. `out_of_scope` defines protected boundaries.

The same normalized scope statement MUST NOT appear in both lists. A material contradiction means the request is invalid until clarified.

Scope is not mutation authority by itself. Systems that execute work need a separate authority mechanism.

## 6. Acceptance criteria

Each acceptance criterion MUST contain:

- `id` — stable unique criterion id;
- `observation_scope` — where/for whom/under what state the behaviour is observed;
- `expected_outcome` — an observable state or behaviour;
- `verification` — how the observation can be checked;
- `valid_alternatives[]` — optional alternate outcomes that are explicitly acceptable;
- `indeterminate_when[]` — conditions under which the criterion cannot safely decide.

### 6.1 Falsifiability

A criterion MUST be capable of being contradicted by an observation.

Bad:

> `bug fixed`

Better:

> When an already-registered email is submitted to `/signup`, the API returns HTTP 409 and the user count does not increase.

### 6.2 Behaviour vs implementation evidence

Build, lint, typecheck and test-suite success usually belong in `verification_evidence`, not in `expected_outcome`.

They MAY be acceptance outcomes only when the requested behaviour is specifically about those mechanisms.

### 6.3 Criterion-invalid / indeterminate path

A reviewer or executor MUST be able to state that a criterion itself cannot safely decide the request because evidence is missing, contradictory or the criterion is invalid.

A system MUST NOT convert missing evidence into success.

## 7. Verification evidence

Each verification-evidence entry MUST contain:

- `id` — unique evidence requirement id;
- `kind` — for example `test`, `build`, `typecheck`, `screenshot`, `manual-review`, `security-review`, `runtime-observation`;
- `required` — boolean;
- `how` — the check/artifact expected.

Evidence requirements describe what must be collected. Their presence in a request does not prove that evidence has already been collected or passed.

## 8. Risks, unknowns and assumptions

A request SHOULD distinguish:

- known risks — understood ways the change can fail;
- unknowns — unresolved facts that can affect the decision;
- assumptions — facts treated as true for the current request.

A material unknown SHOULD become a publication-gate condition when proceeding without resolving it would make acceptance unsafe.

## 9. Approval authority and publication gate

`approval_authority` identifies who/what is authorised to approve the requested publication/merge decision.

`publication_gate.state` is one of:

- `DRAFT` — not ready for execution/publication decision;
- `BLOCKED` — a known condition prevents progression;
- `READY_WHEN` — the request may progress only after every declared condition is satisfied.

`publication_gate.conditions[]` MUST state the observable conditions for progression.

The protocol does not itself verify that an approver is authentic; execution systems require their own trusted-identity boundary.

## 10. Result vocabulary

Tools consuming the protocol SHOULD preserve at least these decision states when evaluating the **request contract**:

- `VALID` — structural and protocol-lint rules passed;
- `INVALID` — the request contradicts or omits a required contract rule;
- `INDETERMINATE` — a required fact cannot be safely established.

These are request-contract states, **not execution completion states**.

## 11. Machine-readable representation

`schema/request.v1.schema.json` is the interchange schema for V1.

`tools/validate_request.py` is a dependency-free semantic linter for repository fixtures. It intentionally does not claim to be a complete JSON Schema implementation. It checks the V1 structural subset and protocol-specific semantic contradictions used by CI.

A consumer that needs formal JSON Schema conformance SHOULD validate against the schema with a standards-compliant Draft 2020-12 implementation in addition to semantic protocol linting.

## 12. Boundary with RepoOps

WM3 Request Protocol owns **the request contract**.

RepoOps or another execution system may consume that contract, but execution, mutation authority, command policy, evidence collection and completion acceptance are separate responsibilities.

A Request Protocol document MUST NOT be treated as proof that implementation occurred.

## 13. Versioning

Backward-incompatible field/semantic changes require a new major protocol version. Backward-compatible clarifications MAY ship as a minor specification revision and MUST be recorded in `CHANGELOG.md`.

`v1.0.0` MUST NOT be tagged until the schema, human templates, GitHub Issue Forms, examples and CI agree on the V1 vocabulary and the migration note is complete.
