# Acceptance criteria: observable, falsifiable, bounded

An acceptance criterion is not a task list and not a confidence statement. It defines an observation that can support or contradict a request outcome.

## A useful criterion answers four questions

1. **Observation scope** — where, for whom and under what state is the behaviour observed?
2. **Expected outcome** — what should be observable?
3. **Verification** — how will that observation be obtained?
4. **Indeterminate path** — when is the evidence insufficient to decide safely?

## Bad vs bounded

Bad:

> Bug fixed.

Bounded:

> With an already-registered email submitted to `POST /signup`, the response is HTTP 409 and the persisted user count does not increase.

Bad:

> Landing page improved.

Bounded:

> At a 390 px viewport, the approved primary CTA is visible without horizontal scrolling and links to the approved intake route.

## Mechanism is usually evidence, not outcome

`build passes`, `lint passes`, `typecheck passes` and `tests pass` are normally verification evidence. They do not by themselves establish that the requested product behaviour exists.

A build may be green while the wrong CTA ships. A test may be green while it asserts the wrong requirement.

## Alternative outcomes

When more than one outcome is valid, declare the alternatives before execution. Do not rewrite the criterion after seeing the result simply to make the work pass.

## Indeterminate and criterion-invalid states

A request consumer must be allowed to say:

- required evidence is unavailable;
- the declared source of truth is contradictory;
- the criterion cannot distinguish valid from invalid behaviour;
- the criterion itself is wrong.

Missing evidence must never be silently translated into success.

## Byte identity

Require exact bytes only when exact byte identity is genuinely the requirement. Otherwise test behaviour, semantics or rendered outcome. Over-specific identity checks often reject valid implementations without improving product correctness.

## Negative tests

Where a false positive would be costly, design at least one control that should fail. A criterion that only sees a happy path can prove much less than it appears to prove.
