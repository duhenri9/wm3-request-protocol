# Contributing

Contributions should make requests clearer, more falsifiable or easier to reuse without turning the protocol into an execution engine.

## Before opening a PR

Run the V1 quality gate:

```bash
python -m compileall tools
python -m unittest tools/test_validate_request.py
python tools/validate_request.py examples/machine-readable/valid-request.json
```

CI also proves the deliberately invalid fixtures, repository-link integrity and V1 vocabulary consistency.

## Protocol changes

For changes to required fields or semantics:

1. update `spec/request-protocol-v1.md`;
2. update `schema/request.v1.schema.json`;
3. update the validator when the semantic rule is machine-checkable;
4. add positive and/or negative fixtures;
5. update human/GitHub templates that expose the affected vocabulary;
6. record the change in `CHANGELOG.md`.

Do not weaken an existing negative control simply to make CI green.

## Design rules

- observable acceptance beats generic quality words;
- missing evidence must not become success;
- templates may specialise a domain but should not create a second vocabulary;
- keep request definition separate from mutation authority/execution;
- keep the compact profile genuinely compact;
- do not add private WM3 prompts, customer data or commercial implementation details.
