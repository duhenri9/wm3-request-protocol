# Request anti-patterns

## Solution before problem

> Add a modal.

The request has selected implementation before stating the actual problem. Record the problem first; a modal may or may not be the smallest valid solution.

## Tautological acceptance

> Bug fixed.

This cannot distinguish a correct implementation from an incorrect one.

## Generic quality words

> Make it better / cleaner / stronger / more professional.

These are directional preferences, not observable acceptance criteria.

## Green-build equivalence

> Done when build and lint pass.

A technically valid build can still implement the wrong behaviour. Build/lint usually belong under verification evidence.

## Mutable source without identity

> Follow the current page.

If the page changes during execution, the request no longer has a stable reference. Capture an identity/version/screenshot/commit when stale-state risk matters.

## Scope contradiction

`in_scope`: checkout behaviour  
`out_of_scope`: checkout behaviour

The request both authorises and forbids the same surface. Resolve before execution.

## Hidden authority

> Ship when it looks good.

Who can decide that? Name approval authority and gate conditions.

## Happy-path-only acceptance

A request may appear complete while a known failure mode is untested. Add negative evidence when false success is materially risky.

## Post-hoc criterion rewrite

Changing acceptance after observing the implementation can turn evaluation into justification. Criteria may be corrected, but the correction should be explicit and treated as a contract change.

## Protocol as proof of delivery

A well-written request is still only a request. It is not evidence that work was executed, verified or accepted.
