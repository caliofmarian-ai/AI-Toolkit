# FUSION-02 Lossless Complete-File Reading

- Generated: 2026-08-27T06:12:45.116717+00:00
- Branch: `fusion-02/mock-free-physiology-recovery`
- Starting commit: `9540326d655162dbbe6e0b3d0fd22d3cf54418f3`
- Human Authority: Marian Caliof
- Lead auditor: ChatGPT
- AI Partner role: supervised semantic collaborator

## Human correction

The fixed 16,000-character prefix was rejected. AI Partner must receive the
complete requested text file, not a prefix presented as a file.

## Implemented physiology

The existing Evidence Engine now retrieves the complete native Git blob through
GitHub's raw blob representation. It verifies the declared byte count and Git
blob SHA, decodes the complete UTF-8 text and records SHA-256 identity.

There is no AI-Toolkit per-file character cap.

If complete content fits the selected provider's governed context, the entire
file is delivered once. If it does not fit, the existing Pipeline and Context
Budget Governor divide consciousness into ordered provider-safe windows. Every
window is delivered, the ordered content is reconstructed, and SHA-256 must
match before completion can be declared.

Intermediate AI reading receipts remain temporary Working Notes. They are not
Evidence, Canon or Human Authority.

## Corrected boundaries

- directory responses are rejected without uncontrolled AttributeError;
- mixed successful and unavailable paths are `PARTIAL`;
- mutable branch-head identity is reported separately from the immutable
  requested commit;
- live acceptance no longer assumes the branch will remain at an older commit;
- native GitHub API limits remain external source limits, not silent
  AI-Toolkit truncation;
- Git LFS materialization is not claimed.

## Verification

- Live complete-file acceptance: `6 passed`
- Focused acceptance: `23 passed`
- Complete FUSION regression: `316 passed`
- Repository regression: `807 passed`
- CSL/UEM Level-3: `ALL PASS`

The live acceptance reads the complete Error Memory at the immutable starting
commit, proves it exceeds 16,000 characters, validates its SHA-256 and safely
handles a directory in a mixed request.

## Remaining boundary

Durable registration and automatic rediscovery of acknowledged checkpoint
evidence and temporary reading receipts after restart remain unimplemented.

No merge or takeover authority is granted.
