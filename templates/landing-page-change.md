# V1 domain extension — Landing page change

Use this together with [`request.md`](request.md). The V1 request contract remains canonical; this file adds landing-specific questions only.

## Domain context

- Page / route:
- Reviewed viewport(s):
- Current deployed/reference identity:
- Approved design/copy source and version:

## Landing-specific in-scope surfaces

- Hero / navigation / proof / pricing / FAQ / CTA / footer:
- Responsive breakpoint(s):

## Protected boundaries

Confirm whether each is out of scope or explicitly authorised:

- offer / positioning;
- approved copy;
- price;
- checkout/intake destination;
- analytics events;
- SEO metadata/structured data;
- authentication/data collection.

## Acceptance-criterion prompts

For each relevant AC in the V1 request, make the observation concrete:

- viewport and browser/device scope;
- exact approved copy/source identity when copy identity matters;
- CTA destination and resulting behaviour;
- visibility/layout observation that can fail;
- accessibility or keyboard behaviour when material;
- valid alternative layout outcomes;
- conditions that make visual evidence indeterminate.

Do not use `looks better` or `more professional` as standalone acceptance criteria.

## Verification-evidence prompts

Possible evidence requirements:

- desktop/mobile screenshots at named viewport sizes;
- link/CTA smoke test;
- build/typecheck/lint;
- accessibility check;
- analytics event observation;
- approved-copy comparison;
- production smoke after deploy when authorised.

These checks support acceptance; they do not replace the observable ACs.
