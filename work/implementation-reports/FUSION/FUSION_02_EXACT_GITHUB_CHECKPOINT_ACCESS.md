# FUSION-02 Exact GitHub Checkpoint Access

- Generated: 2026-08-26T22:21:15.926820+00:00
- Branch: `fusion-02/mock-free-physiology-recovery`
- Starting commit: `4baa82b3fb5446f75a72039684e2a2a601d92340`
- Human Authority: Marian Caliof
- Lead auditor: ChatGPT
- AI Partner role: supervised semantic collaborator

## Demonstrated gap

AI Partner honestly reported that exact branch, commit and requested file
bytes were unavailable. The existing Evidence Engine was limited to the
current local checkout.

## Implemented physiology

An explicit request containing repository, full commit and bounded paths now
travels through the existing Evidence Engine. It retrieves the immutable
commit and real file bytes from the public GitHub API.

The requested branch is resolved separately. Branch head and requested commit
remain distinct provenance fields and equality is reported rather than
assumed.

Evidence entering the existing Working Context contains repository identity,
requested branch, requested commit, resolved commit, blob SHA, byte count,
bounded content and completeness state.

Retrieval remains read-only, authority-neutral and incapable of promoting
Evidence to Canon.

## Security and boundedness

- fixed HTTPS GitHub API host;
- explicit public repository identity;
- full 40-character commit required;
- maximum four paths;
- maximum 16,000 characters per source;
- parent traversal and absolute paths rejected;
- no credential required or persisted;
- network failure remains NOT AVAILABLE.

## Verification

- Real live GitHub acceptance: `2 passed`
- Focused network-free acceptance: `10 passed`
- Complete FUSION regression: `313 passed`
- Repository regression: `804 passed`
- CSL/UEM Level-3: `ALL PASS`

## Remaining transfer boundary

Checkpoint evidence is attached to the current Working Context and durable
conversation raw sources, but acknowledged checkpoint registration and
automatic rediscovery after restart remain unimplemented.

No merge or takeover authority is granted.
