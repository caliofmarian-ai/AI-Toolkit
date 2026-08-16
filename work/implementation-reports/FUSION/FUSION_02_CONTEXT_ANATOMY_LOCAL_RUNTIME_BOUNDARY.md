# FUSION-02 — Context Anatomy Local/Runtime Boundary

Generated: 2026-08-16T19:32:30.206610+00:00

## Live Railway evidence already demonstrated

- Human message characters: **2**
- Reconstructed context characters: **295122**
- Serialized request bytes: **328917**
- Estimated tokens at 4 chars/token: **82230**
- Conservative estimated tokens: **109639**
- Provider result: **HTTP 429 / type=tokens / code=rate_limit_exceeded**

## Runtime-state boundary

The production Owner AI Chat session that produced the live request is stored by AISessionEngine under `.ai/ai_sessions` inside the repository root of the running process.

The Termux checkout does not contain `.ai/ai_sessions`.

Therefore the exact live Railway conversation reconstruction cannot be reproduced honestly from the local checkout.

No synthetic session was created.

## Locally reconstructible AIContextBuilder anatomy

- Complete base-context serialized bytes: **329052**
- Approximate tokens at 4 bytes/chars: **82263**

| Base-context branch | Serialized bytes | Percentage |
|---|---:|---:|
| `repository_profile` | 272210 | 82.73% |
| `runtime_status` | 42127 | 12.80% |
| `workspace` | 8976 | 2.73% |
| `engineering_session` | 2253 | 0.68% |
| `context` | 1715 | 0.52% |
| `canonical_documents` | 730 | 0.22% |
| `repository_health` | 501 | 0.15% |
| `recent_reports` | 107 | 0.03% |
| `dependencies` | 99 | 0.03% |
| `technology_stack` | 51 | 0.02% |
| `current_epic` | 10 | 0.00% |
| `current_issue` | 10 | 0.00% |
| `current_branch` | 6 | 0.00% |
| `current_sprint` | 2 | 0.00% |

## Proven architecture

The complete FUSION-02 context is not only the RAW conversation.

ConversationContextReconstructor combines at least:

- bounded RAW conversation sources;
- active project/session identity;
- Persistent Experience;
- provenance;
- Error Memory references;
- epistemic organism state;
- engineering/repository context;
- epistemic boundaries.

The RAW conversation itself is bounded to 12 sources with a maximum of 6000 content characters per source, but that bound does not bound the complete reconstructed provider context.

## Diagnostic conclusion

The 295122-character live request cannot be attributed to RAW conversation merely from its total size.

The next diagnostic must execute at the Railway reconstruction boundary, where the actual session and Persistent Experience are available, and emit SIZE METADATA ONLY for each top-level context branch.

It must not emit context content, RAW messages, credentials, or complete payloads.

This is the correct observation point because the oversized object exists there immediately before provider transmission.

## Safety

- OpenAI called: **NO**
- Synthetic conversation created: **NO**
- RAW content exposed: **NO**
- Credential exposed: **NO**
- Production code modified: **NO**
- Canon modified: **NO**
