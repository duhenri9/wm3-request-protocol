# Migrating the July 2026 protocol to V1

The original public protocol established the core discipline: context, source of truth, in/out scope, definition of done and validation.

V1 preserves that idea but makes several distinctions explicit.

## What changed

### “Definition of done” → acceptance criteria + verification evidence

V1 separates observable product behaviour from implementation checks such as build, lint and typecheck.

### Source of truth now carries identity

A URL or document should include a version/SHA/revision when stale-state risk matters.

### Explicit unknown and indeterminate paths

A request can say that evidence is unavailable or that a criterion cannot safely decide instead of forcing success/failure.

### Approval authority is explicit

Technical correctness is not automatically publication authority.

### Machine-readable contract

V1 adds JSON Schema, deterministic fixtures and a semantic validator for automation/tooling use.

### GitHub-native authoring

Issue Forms and the PR template use the V1 vocabulary instead of creating a parallel workflow language.

## Existing specialised templates

Older landing/checkout/PR examples remain useful domain prompts, but new requests should use the V1 vocabulary as the canonical contract. Specialised templates can add domain questions; they should not redefine acceptance, scope or authority semantics.

## No execution claim

The original protocol sometimes placed validations close to “done”. V1 makes the boundary stronger: describing required evidence is not the same as collecting it, and a valid request is not evidence of delivered work.
