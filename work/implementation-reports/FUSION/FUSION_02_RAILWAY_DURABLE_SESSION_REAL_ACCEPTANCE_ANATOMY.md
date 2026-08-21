# FUSION-02 — Railway Durable Session Real Acceptance Anatomy

## Purpose

Determine the real infrastructure position for durable AI Partner sessions
before performing a destructive or misleading redeploy acceptance.

## Authority

Local HEAD: dd65c0135ca4ce11b75dd483b9af47e3f5032741

Origin main: dd65c0135ca4ce11b75dd483b9af47e3f5032741

## Preserved physiology

- repository root and durable state root remain separate;
- AI_TOOLKIT_STATE_ROOT is the durable-state contract;
- no reset was performed;
- no restore was performed;
- no stash was performed;
- no force push was performed;
- no production mutation was authorized by this inspection.

## Acceptance boundary

Software support alone does not prove Railway persistence.

Real acceptance requires the same session identity and persisted conversation
to survive an actual Railway redeploy.

## Observed execution

==========================================================
FUSION-02 — RAILWAY DURABLE SESSION REAL ACCEPTANCE ANATOMY
==========================================================

[1/7] GIT AUTHORITY + WORKTREE CONSERVATION
----------------------------------------------------------
From https://github.com/caliofmarian-ai/AI-Toolkit
 * branch            main       -> FETCH_HEAD
LOCAL=dd65c0135ca4ce11b75dd483b9af47e3f5032741
REMOTE=dd65c0135ca4ce11b75dd483b9af47e3f5032741

--- git status ---
 M lib/python/dashboard/service.py
 M work/implementation-reports/FUSION/FUSION_02_TERMUX_EXECUTION_ERROR_MEMORY.md
?? work/implementation-reports/FUSION/FUSION_02_AI_PARTNER_REAL_SESSION_REATTACHMENT_ANATOMY.md

PASS: local HEAD matches origin/main.
PASS: no reset performed.
PASS: no restore performed.
PASS: no stash performed.
PASS: no force push performed.

==========================================================
[2/7] VERIFY DURABLE SESSION IMPLEMENTATION IN CURRENT SOURCE
==========================================================
23:            else os.environ.get("AI_TOOLKIT_STATE_ROOT", "")
PASS: AI_TOOLKIT_STATE_ROOT support exists in AISessionEngine.

--- AISessionEngine.__init__ ---
(self, repository_root: 'str' = '.', *, state_root: 'str | None' = None) -> 'None'

--- source excerpt ---
    def __init__(
        self,
        repository_root: str = ".",
        *,
        state_root: str | None = None,
    ) -> None:
        self.root = Path(repository_root).resolve()

        configured_state_root = (
            state_root
            if state_root is not None
            else os.environ.get("AI_TOOLKIT_STATE_ROOT", "")
        )

        if configured_state_root:
            self.state_root = Path(
                configured_state_root
            ).expanduser().resolve()
        else:
            # Historical/local compatibility:
            # without an explicit durable root, preserve the established
            # repository-local state anatomy.
            self.state_root = self.root

        self.dir = (
            self.state_root
            / ".ai"
            / "ai_sessions"
        )


==========================================================
[3/7] RAILWAY CLI AVAILABILITY + PROJECT LINK
==========================================================
RAILWAY_CLI: FOUND
railway 5.23.0


--- Railway project/service status ---

A newer Railway CLI is available: v5.30.4 (current: v5.23.0).
Run `railway upgrade --yes` to update.

Workspace:       caliofmarian-ai's Projects

Project:         Ai-Toolkit
Project ID:      22b36405-7daa-479b-a2be-f0b93ef5666d

Environment:     production
Environment ID:  5c14c0b6-420e-492a-8d5d-06eeeca4f086

Linked service

AI-Toolkit
    status:        ● Online
    repo:          caliofmarian-ai/AI-Toolkit
    url:           https://ai-toolkit-production.up.railway.app
    volume:        ai-toolkit-volume · /data/ai-toolkit-state · 0.1 GB / 4.9 GB
    region:        EU West
    deployment ID: e2e42429-2990-4539-ba04-e01650eb4e78
    service ID:    e915efd7-5c51-46f9-9f1d-2b968efbd067

────────────────────────────────────────────────

All resources

    Services
      - AI-Toolkit: ● Online · https://ai-toolkit-production.up.railway.app · ai-toolkit-volume


==========================================================
[4/7] INSPECT REAL RAILWAY VARIABLES
==========================================================
PASS: Railway variables are readable.

PASS: AI_TOOLKIT_STATE_ROOT exists in Railway variables.
AI_TOOLKIT_STATE_ROOT: CONFIGURED

==========================================================
[5/7] INSPECT RAILWAY RUNTIME / DURABLE MOUNT
==========================================================
RUNTIME_PWD=/data/data/com.termux/files/home/storage/shared/AI-Projects/AI-Toolkit
AI_TOOLKIT_STATE_ROOT=/data/ai-toolkit-state

--- state root anatomy ---
STATE_ROOT_EXISTS=NO

--- session directory ---
SESSION_DIR_EXISTS=NO

PASS: Railway-linked runtime inspection command completed.

==========================================================
[6/7] CURRENT SESSION PERSISTENCE POSITION
==========================================================
SOFTWARE_SUPPORT: PRESENT
STATE_ROOT_VARIABLE: PRESENT
RUNTIME_STATE_ROOT: NOT_DEMONSTRATED
SESSION_STORAGE: NOT_YET_OBSERVED

IMPORTANT:
  This inspection does NOT claim redeploy persistence merely
  because AISessionEngine supports AI_TOOLKIT_STATE_ROOT.

  Real acceptance requires:
    session before redeploy
    durable session file
    Railway redeploy
    same durable session file
    same session_id
    continued conversation

==========================================================
[7/7] GENERATE IMPLEMENTATION REPORT
==========================================================


## Next physiological decision

If a persistent Railway mount and AI_TOOLKIT_STATE_ROOT are demonstrated,
perform the real session -> redeploy -> same-session acceptance.

If either is absent, configure the missing Railway infrastructure first.

Generated: 2026-08-21T05:59:19.940273+00:00
