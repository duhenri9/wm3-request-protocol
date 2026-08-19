# V1 domain extension — Checkout or intake change

Use this together with [`request.md`](request.md). V1 owns source-of-truth, scope, acceptance, evidence and authority semantics; this file adds high-risk checkout/intake prompts.

## Domain context

- Route / form / checkout provider:
- Current contract/version:
- Data destination:
- Payment/intake state involved:

## Protected boundaries

Explicitly classify each as in or out of scope:

- price/currency/tax;
- payment provider configuration;
- authentication/session;
- database schema;
- consent/privacy copy;
- lead/customer notification;
- webhook/API contract;
- retry/idempotency behaviour;
- analytics/conversion event.

## Acceptance-criterion prompts

For each relevant AC, identify:

- exact input/state;
- expected response/UI state;
- persistence/payment side effect that must or must not occur;
- duplicate/retry behaviour;
- failure-state behaviour;
- observation that distinguishes a false positive;
- conditions where evidence is unavailable and the result is indeterminate.

`Form submits successfully` is insufficient when the real requirement includes persistence, payment, email or webhook effects.

## Negative-control prompts

Where material, require at least one failure/control case such as:

- invalid input does not create a record;
- duplicate request does not duplicate payment/persistence;
- provider failure does not display false success;
- stale session does not silently lose user data;
- an unauthorised state does not bypass the intended gate.

## Verification-evidence prompts

Possible evidence requirements:

- contract/integration tests;
- sandbox provider receipt;
- persistence before/after observation;
- idempotency/retry fixture;
- security/privacy review;
- build/typecheck;
- authorised production smoke only when the publication gate permits it.
