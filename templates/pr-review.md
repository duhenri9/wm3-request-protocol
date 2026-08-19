# V1 domain extension — Pull request review

A PR review compares the **actual delta** with the V1 request contract. The PR description is not the source of truth for what changed.

## Request identity

- Request ID:
- Protocol version:
- Request/source issue:
- Reviewed base SHA:
- Reviewed head SHA:

## Actual delta

- Files/surfaces changed:
- Routes/contracts/data affected:
- Behaviour changed:
- Behaviour preserved:

## Scope comparison

- [ ] Actual delta is inside declared `in_scope`.
- [ ] Protected `out_of_scope` surfaces remain unchanged.
- [ ] Any unexpected delta is listed below.

Unexpected delta:

- 

## Acceptance observations

For every requested AC:

| Criterion | Observed result | Evidence | Decision |
|---|---|---|---|
| AC- |  |  | PASS / FAIL / INDETERMINATE / CRITERION_INVALID |

Do not translate `tests green` or an author statement such as `done` into acceptance without the declared observation/evidence.

## Verification evidence

- [ ] required test/build/typecheck/lint evidence;
- [ ] required visual/runtime evidence;
- [ ] security/privacy evidence when declared;
- [ ] source-of-truth freshness checked;
- [ ] negative/failure controls observed when required.

## Remaining risk / unknowns

- 

## Review decision

- [ ] Approve within the bounded request/evidence reviewed
- [ ] Request changes
- [ ] Comment only
- [ ] Keep draft / block merge

## Merge/publication condition

Approval is tied to the reviewed head identity. If the head changes materially after review, required evidence/approval must be reconsidered.
