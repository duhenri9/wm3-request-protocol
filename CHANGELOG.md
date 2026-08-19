# Changelog

All notable protocol changes are recorded here.

## Unreleased — V1 release candidate

### Added

- normative Request Protocol V1 specification;
- Draft 2020-12 JSON Schema interchange contract;
- dependency-free semantic validator with deterministic evidence report;
- valid and deliberately invalid machine-readable fixtures;
- GitHub Issue Forms and pull-request evidence template;
- explicit acceptance vs verification-evidence semantics;
- source-of-truth identity/stale-state guidance;
- `VALID | INVALID | INDETERMINATE` request-contract vocabulary;
- protocol lifecycle, anti-patterns and RepoOps boundary documentation;
- English-first public documentation with PT-BR retained as a first-class translation.

### Changed

- primary request/bug templates now use the V1 vocabulary;
- implementation checks such as build/typecheck are treated as verification evidence unless they are themselves the requested behaviour;
- publication authority and gate conditions are explicit.

### Migration

See [`docs/migration-v0-to-v1.md`](docs/migration-v0-to-v1.md).

## 2026-07-04 — Initial public protocol

- context/problem/source-of-truth discipline;
- in-scope/out-of-scope boundaries;
- definition-of-done and validation templates;
- landing, checkout, bug and PR-review examples.
