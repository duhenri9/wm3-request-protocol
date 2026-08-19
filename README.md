# WM3 Request Protocol

**English** · [Português (Brasil)](README.pt-BR.md)

An open-source, versioned contract for turning vague product/software requests into bounded work definitions with **source of truth, scope, observable acceptance, required evidence and publication authority**.

> A clear request is still not proof that the work was delivered.

## The 60-second difference

Weak request:

> Fix the signup bug and make sure it works.

V1 request:

- **Problem:** duplicate email returns HTTP 500.
- **Source of truth:** current `POST /signup` contract + reviewed base SHA.
- **In scope:** duplicate-email handling.
- **Out of scope:** auth provider, pricing, database schema.
- **AC-1:** with an existing email, return HTTP 409 and do not increase user count.
- **Verification:** integration fixture + build at the reviewed head SHA.
- **Indeterminate when:** the fixture cannot establish the pre-request user count.
- **Gate:** `READY_WHEN` AC-1 and required evidence are green.

That is materially different from `bug fixed` or `build passes`.

## V1 contract

```text
problem
  ↓
source of truth + identity
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

V1 includes:

- a [normative specification](spec/request-protocol-v1.md);
- a [Draft 2020-12 JSON Schema](schema/request.v1.schema.json);
- a [human V1 request template](templates/request.md);
- GitHub Issue Forms and a PR evidence template;
- a dependency-free semantic validator/linter;
- valid and deliberately invalid machine-readable fixtures;
- CI negative controls;
- focused guidance for [acceptance criteria](docs/acceptance-criteria.md), [source of truth](docs/source-of-truth.md), [anti-patterns](docs/anti-patterns.md) and the [request lifecycle](docs/request-lifecycle.md).

## Validate a machine-readable request

```bash
python tools/validate_request.py examples/machine-readable/valid-request.json
```

The validator emits deterministic request/report SHA-256 identities and a bounded request-contract result.

It deliberately **does not** execute the requested work, verify external authority or claim that implementation succeeded.

The JSON Schema is the interchange contract. The bundled validator is intentionally a dependency-free semantic linter, not a claim of complete JSON Schema Draft 2020-12 implementation.

## Decision vocabulary

For request-contract evaluation:

- `VALID` — implemented V1 structure/semantic lint rules passed;
- `INVALID` — a required rule is missing or contradicted;
- `INDETERMINATE` — a consumer cannot safely establish a required fact.

For publication state:

- `DRAFT`;
- `BLOCKED`;
- `READY_WHEN`.

`READY_WHEN` means progression conditions are explicit. It does not mean they have already been satisfied.

## Why acceptance and verification are separate

A build can pass while the wrong behaviour ships. A test can pass while asserting the wrong requirement.

V1 therefore separates:

**Acceptance criterion**

> With an already-registered email submitted to `/signup`, the API returns HTTP 409 and persisted user count remains unchanged.

from

**Verification evidence**

> Integration fixture passed; build passed at reviewed head SHA; required security review completed.

See [Acceptance criteria](docs/acceptance-criteria.md).

## Compact without becoming vague

V1 has two authoring profiles:

- `compact` — small/low-risk changes;
- `standard` — material product/software changes.

The compact profile keeps the same vocabulary and essential boundaries. It is not permission to omit source of truth, scope, acceptance, evidence or authority.

## Request Protocol is not RepoOps

WM3 Request Protocol owns **the work/request contract**.

[RepoOps](https://github.com/duhenri9/RepoOps) is a separate project concerned with bounded repository execution, authority, verification and evidence receipts.

A valid Request Protocol document may exist before a single line of implementation code exists. See [Protocol vs RepoOps](docs/protocol-vs-repoops.md).

## Human and GitHub-native use

- [General V1 request](templates/request.md)
- [V1 bug request](templates/bug-report.md)
- GitHub `V1 change request` Issue Form
- GitHub `V1 bug report` Issue Form
- [PR evidence template](.github/pull_request_template.md)

Existing landing, checkout/intake and PR-review templates/examples are retained as domain guidance. The V1 vocabulary remains canonical; see the [migration guide](docs/migration-v0-to-v1.md).

## Quality gate

The V1 repository gate is designed to prove the protocol tooling itself, not the correctness of arbitrary downstream requests:

```bash
python -m compileall tools
python -m unittest tools/test_validate_request.py
python tools/validate_request.py examples/machine-readable/valid-request.json
```

CI additionally requires the invalid fixtures to fail for their expected reasons and checks repository-local documentation links/vocabulary consistency.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Protocol changes should update the specification, schema, tooling, fixtures and exposed templates together rather than allowing those representations to drift.

## License and trademarks

Content and code are MIT licensed. The MIT License does not grant trademark rights in WM3 Digital names or brand assets; see [TRADEMARKS.md](TRADEMARKS.md).

## Related WM3 work

WM3 Request Protocol is independently useful and requires no commercial WM3 product. For readers interested in related WM3 work, Audit 360 explores alignment between product promise, flow, implementation and project context.
