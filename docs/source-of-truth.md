# Source of truth and stale-state risk

A request needs to say what reality constrains the change. A source of truth is not just a link; when possible it includes an exact identity.

Examples:

- commit + SHA;
- document + revision/date;
- design + approved version;
- production behaviour + observation timestamp/environment;
- decision record + decision id/date;
- API contract + version.

## Mutable references

`main`, a live URL or an editable document can change after the request is written. When that matters, record the observed identity/version and require a freshness check before merge/publication.

## Contradictory sources

If two declared sources disagree materially, the request should be `BLOCKED` or treated as indeterminate until authority resolves the conflict. An executor must not silently choose the convenient source.

## Unavailable sources

If required evidence cannot be retrieved, do not replace it with memory or an inferred approximation and still claim the request contract is satisfied.

## Source identity is not authority

A document can be identifiable without being authorised. `approval_authority` remains a separate V1 field.
