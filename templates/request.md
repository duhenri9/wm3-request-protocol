# WM3 Request Protocol V1 — Change Request

> This template defines a request contract. It does not authorise execution or prove delivery.

## Identity

- **Request ID:**
- **Protocol version:** `1.0`
- **Profile:** `compact | standard`

## Context

What is the relevant current state? Name the product, repository, route, flow or operational context.

## Problem

Describe the problem **before** prescribing the implementation.

## Source of truth

List at least one source. Include an exact SHA/version/date/revision when one exists.

| Kind | Reference | Identity / version |
|---|---|---|
| commit / document / URL / decision / production behaviour |  |  |

If a source is mutable, explain how stale-state risk will be handled.

## In scope

- 

## Out of scope

- 

The same surface must not appear in both lists.

## Acceptance criteria

Each criterion must describe an observable outcome, not merely a mechanism such as `build passes`.

### AC-1 — [name]

- **Observation scope:**
- **Expected observable outcome:**
- **Verification:**
- **Valid alternatives:**
- **Indeterminate when:**

Add more criteria only when they represent distinct observable requirements.

## Verification evidence

List checks/artifacts required to support acceptance. Their inclusion here does not mean they have already passed.

| ID | Kind | Required? | How / artifact |
|---|---|---|---|
| EV-1 | test / build / typecheck / screenshot / security review / runtime observation | yes |  |

## Risks

- 

## Unknowns

- 

## Assumptions (optional)

- 

## Reversibility (optional)

How can the change be rolled back or isolated if evidence later contradicts the decision?

## Data / privacy impact (optional)

What data boundary changes, if any?

## Approval authority

Who or what role is authorised to approve the relevant merge/publication decision?

- 

## Publication gate

- **State:** `DRAFT | BLOCKED | READY_WHEN`
- **Conditions:**
  - 

## Control line

> This request exists to [observable objective] without changing [important protected boundary].

If evidence is missing, contradictory, or a criterion cannot safely decide the result, report that explicitly rather than manufacturing success.
