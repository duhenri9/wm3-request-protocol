# WM3 Request Protocol vs RepoOps

The projects share an evidence-first philosophy but solve different problems.

| Concern | WM3 Request Protocol | RepoOps |
|---|---|---|
| Problem definition | owns | consumes |
| Source of truth | declares | verifies/uses under adapter policy |
| In/out scope | declares | enforces mutation boundary |
| Acceptance criteria | defines | can evaluate using collected evidence |
| Verification requirements | declares | may execute permitted checks |
| Mutation authority | does not own | explicit runtime concern |
| Repository mutation | no | bounded execution concern |
| Evidence receipt | requirement only | executable runtime evidence |
| Completion state | does not certify delivery | bounded acceptance runtime |
| LLM planner | not required | optional/untrusted adapter |

## Boundary rule

A V1 request document may be valid while no implementation exists.

RepoOps may receive a valid request but still reject or mark execution indeterminate because authority, repository state or required evidence does not support completion.

Neither project should silently expand into the other:

- Request Protocol must remain usable without a coding agent.
- RepoOps must not invent requirements that the request contract did not authorise.
