# PCC-01 — SESSION BINDING IMPLEMENTATION REPORT — RUN 010

**Stage:** Session Binding

**Execution date:** 2026-08-13

**Expected baseline:** `5c82eb85b42e0cc686cd95e8b2ee053c36a62b82`

**Purpose:** Build the first explicit binding tissue between a Session identity and an Experience identity without collapsing either concept.

**Git conservation:** NOT PERFORMED

---

## 1. Baseline Verification

```text
Expected:    5c82eb85b42e0cc686cd95e8b2ee053c36a62b82
LOCAL:       5c82eb85b42e0cc686cd95e8b2ee053c36a62b82
origin/main: 5c82eb85b42e0cc686cd95e8b2ee053c36a62b82
PASS: LOCAL == expected baseline
PASS: origin/main == expected baseline
```

## 2. Pre-Implementation Working Tree

```text
PASS: repository clean except current RUN 010 report
```

## 3. Existing Core Experience Anatomy

```text
PASS: lib/python/experience/__init__.py
PASS: lib/python/experience/identity.py
PASS: lib/python/experience/model.py
PASS: lib/python/experience/lifecycle.py
PASS: lib/python/experience/repository.py
PASS: lib/python/experience/service.py
```

## 4. Existing Session Tissue Inspection

```text
lib/python/session_runtime/models.py:5:class Session:
lib/python/session_runtime/runtime.py:6:class SessionRuntime:
lib/python/session_runtime/storage.py:4:class SessionStorage:
lib/python/ai_cto_scanner/detectors.py:370:            r"session_id\b",
lib/python/development_state_engine/models.py:381:    session_id: str
lib/python/development_state_engine/models.py:396:        _require_non_empty_string("session_id", self.session_id)
lib/python/development_state_engine/models.py:406:            "session_id": self.session_id,
lib/python/development_state_engine/models.py:419:            session_id=data["session_id"],
lib/python/development_state_engine/runtime.py:1104:                session_id="UNBOUND",
lib/python/ai_platform/service.py:69:    def ask_repository(self, question: str, *, session_id: str = "", provider_id: str = "", model: str = "", prompt_name: str = "") -> Dict[str, Any]:
lib/python/ai_platform/service.py:74:        if session_id:
lib/python/ai_platform/service.py:75:            session = self.sessions.append_interaction(session_id, effective_question, result["answer"], result["usage"])
lib/python/ai_platform/service.py:95:            "session_id": session["id"],
lib/python/ai_platform/sessions.py:10:class AISessionEngine:
lib/python/ai_platform/sessions.py:49:    def get(self, session_id: str) -> Dict[str, Any]:
lib/python/ai_platform/sessions.py:50:        path = self.dir / f"{session_id}.json"
lib/python/ai_platform/sessions.py:53:    def append_interaction(self, session_id: str, question: str, answer: str, usage: Mapping[str, Any]) -> Dict[str, Any]:
lib/python/ai_platform/sessions.py:54:        session = self.get(session_id)
lib/python/ai_platform/sessions.py:56:            raise ValueError(f"unknown session {session_id}")
lib/python/dashboard/service.py:436:                    ("Session", result.get("session_id", "")),
lib/python/engineering_workspace/models.py:90:class WorkspaceSession:
lib/python/engineering_workspace/models.py:91:    session_id: str
lib/python/epistemic/session.py:20:class Session:
lib/python/epistemic/session.py:31:class SessionManager:
tests/experience/test_experience_model.py:21:    assert not hasattr(experience, "session_id")
tests/experience/test_experience_core.py:48:        "session_id",

NOTE:
Term occurrence is not treated as behavioral compatibility.
No existing Session implementation is automatically inherited merely because its name contains Session.
```

## 5. Target Boundary

```text
PASS: Session Binding production target absent
PASS: Session Binding test target absent
```

## 6. Session Binding Dedicated Behavioral Test

```text
FFFFF......FFFFF                                                         [100%]
=================================== FAILURES ===================================
______________ test_session_binding_connects_distinct_identities _______________

    def test_session_binding_connects_distinct_identities():
        experience = Experience.create()
    
>       binding = SessionBinding.create(
            session_id="session-alpha",
            experience_id=experience.experience_id,
        )

tests/experience/test_experience_session_binding.py:15: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

cls = <class 'lib.python.experience.session_binding.SessionBinding'>
session_id = 'session-alpha'
experience_id = ExperienceId(value='207db940-8dc4-449d-9533-3c039ab6b270')

    @classmethod
    def create(
        cls,
        *,
        session_id: str,
        experience_id: ExperienceId,
    ) -> "SessionBinding":
        normalized_session_id = normalize_session_id(session_id)
    
        if not isinstance(experience_id, str):
>           raise InvalidExperienceBindingError(
                "experience_id must be a string identity"
            )
E           lib.python.experience.session_binding.InvalidExperienceBindingError: experience_id must be a string identity

lib/python/experience/session_binding.py:88: InvalidExperienceBindingError
_______________ test_session_identity_is_not_experience_identity _______________

    def test_session_identity_is_not_experience_identity():
        experience = Experience.create()
    
>       binding = SessionBinding.create(
            session_id="session-alpha",
            experience_id=experience.experience_id,
        )

tests/experience/test_experience_session_binding.py:27: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

cls = <class 'lib.python.experience.session_binding.SessionBinding'>
session_id = 'session-alpha'
experience_id = ExperienceId(value='7c8210a5-251d-413b-afa4-b81b26db8559')

    @classmethod
    def create(
        cls,
        *,
        session_id: str,
        experience_id: ExperienceId,
    ) -> "SessionBinding":
        normalized_session_id = normalize_session_id(session_id)
    
        if not isinstance(experience_id, str):
>           raise InvalidExperienceBindingError(
                "experience_id must be a string identity"
            )
E           lib.python.experience.session_binding.InvalidExperienceBindingError: experience_id must be a string identity

lib/python/experience/session_binding.py:88: InvalidExperienceBindingError
___________________ test_binding_does_not_replace_experience ___________________

    def test_binding_does_not_replace_experience():
        experience = Experience.create()
    
>       binding = SessionBinding.create(
            session_id="session-alpha",
            experience_id=experience.experience_id,
        )

tests/experience/test_experience_session_binding.py:38: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

cls = <class 'lib.python.experience.session_binding.SessionBinding'>
session_id = 'session-alpha'
experience_id = ExperienceId(value='8d963d79-1c39-4dc7-9e90-564236e0bd6a')

    @classmethod
    def create(
        cls,
        *,
        session_id: str,
        experience_id: ExperienceId,
    ) -> "SessionBinding":
        normalized_session_id = normalize_session_id(session_id)
    
        if not isinstance(experience_id, str):
>           raise InvalidExperienceBindingError(
                "experience_id must be a string identity"
            )
E           lib.python.experience.session_binding.InvalidExperienceBindingError: experience_id must be a string identity

lib/python/experience/session_binding.py:88: InvalidExperienceBindingError
__________________ test_binding_preserves_experience_identity __________________

    def test_binding_preserves_experience_identity():
        experience = Experience.create()
        original_identity = experience.experience_id
    
>       binding = SessionBinding.create(
            session_id="session-alpha",
            experience_id=original_identity,
        )

tests/experience/test_experience_session_binding.py:51: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

cls = <class 'lib.python.experience.session_binding.SessionBinding'>
session_id = 'session-alpha'
experience_id = ExperienceId(value='e4f36056-4f5d-45a7-8429-9ab7ec25be66')

    @classmethod
    def create(
        cls,
        *,
        session_id: str,
        experience_id: ExperienceId,
    ) -> "SessionBinding":
        normalized_session_id = normalize_session_id(session_id)
    
        if not isinstance(experience_id, str):
>           raise InvalidExperienceBindingError(
                "experience_id must be a string identity"
            )
E           lib.python.experience.session_binding.InvalidExperienceBindingError: experience_id must be a string identity

lib/python/experience/session_binding.py:88: InvalidExperienceBindingError
________________________ test_session_id_is_normalized _________________________

    def test_session_id_is_normalized():
        experience = Experience.create()
    
>       binding = SessionBinding.create(
            session_id="  session-alpha  ",
            experience_id=experience.experience_id,
        )

tests/experience/test_experience_session_binding.py:63: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

cls = <class 'lib.python.experience.session_binding.SessionBinding'>
session_id = '  session-alpha  '
experience_id = ExperienceId(value='14c40724-a6df-4729-ab2a-d2edde7f78a5')

    @classmethod
    def create(
        cls,
        *,
        session_id: str,
        experience_id: ExperienceId,
    ) -> "SessionBinding":
        normalized_session_id = normalize_session_id(session_id)
    
        if not isinstance(experience_id, str):
>           raise InvalidExperienceBindingError(
                "experience_id must be a string identity"
            )
E           lib.python.experience.session_binding.InvalidExperienceBindingError: experience_id must be a string identity

lib/python/experience/session_binding.py:88: InvalidExperienceBindingError
________________ test_binding_can_confirm_experience_membership ________________

    def test_binding_can_confirm_experience_membership():
        experience = Experience.create()
    
>       binding = SessionBinding.create(
            session_id="session-alpha",
            experience_id=experience.experience_id,
        )

tests/experience/test_experience_session_binding.py:106: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

cls = <class 'lib.python.experience.session_binding.SessionBinding'>
session_id = 'session-alpha'
experience_id = ExperienceId(value='50e78e31-0a7e-4b60-89bf-4aecc6dbdebf')

    @classmethod
    def create(
        cls,
        *,
        session_id: str,
        experience_id: ExperienceId,
    ) -> "SessionBinding":
        normalized_session_id = normalize_session_id(session_id)
    
        if not isinstance(experience_id, str):
>           raise InvalidExperienceBindingError(
                "experience_id must be a string identity"
            )
E           lib.python.experience.session_binding.InvalidExperienceBindingError: experience_id must be a string identity

lib/python/experience/session_binding.py:88: InvalidExperienceBindingError
_______________ test_binding_rejects_other_experience_membership _______________

    def test_binding_rejects_other_experience_membership():
        first = Experience.create()
        second = Experience.create()
    
>       binding = SessionBinding.create(
            session_id="session-alpha",
            experience_id=first.experience_id,
        )

tests/experience/test_experience_session_binding.py:118: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

cls = <class 'lib.python.experience.session_binding.SessionBinding'>
session_id = 'session-alpha'
experience_id = ExperienceId(value='26635ea9-278d-4f4b-8aab-9ced0ca21c4c')

    @classmethod
    def create(
        cls,
        *,
        session_id: str,
        experience_id: ExperienceId,
    ) -> "SessionBinding":
        normalized_session_id = normalize_session_id(session_id)
    
        if not isinstance(experience_id, str):
>           raise InvalidExperienceBindingError(
                "experience_id must be a string identity"
            )
E           lib.python.experience.session_binding.InvalidExperienceBindingError: experience_id must be a string identity

lib/python/experience/session_binding.py:88: InvalidExperienceBindingError
_________________ test_binding_can_confirm_session_membership __________________

    def test_binding_can_confirm_session_membership():
        experience = Experience.create()
    
>       binding = SessionBinding.create(
            session_id="session-alpha",
            experience_id=experience.experience_id,
        )

tests/experience/test_experience_session_binding.py:129: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

cls = <class 'lib.python.experience.session_binding.SessionBinding'>
session_id = 'session-alpha'
experience_id = ExperienceId(value='d4c1043d-d700-4b38-a42d-87725f0686ce')

    @classmethod
    def create(
        cls,
        *,
        session_id: str,
        experience_id: ExperienceId,
    ) -> "SessionBinding":
        normalized_session_id = normalize_session_id(session_id)
    
        if not isinstance(experience_id, str):
>           raise InvalidExperienceBindingError(
                "experience_id must be a string identity"
            )
E           lib.python.experience.session_binding.InvalidExperienceBindingError: experience_id must be a string identity

lib/python/experience/session_binding.py:88: InvalidExperienceBindingError
________________ test_binding_rejects_other_session_membership _________________

    def test_binding_rejects_other_session_membership():
        experience = Experience.create()
    
>       binding = SessionBinding.create(
            session_id="session-alpha",
            experience_id=experience.experience_id,
        )

tests/experience/test_experience_session_binding.py:141: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

cls = <class 'lib.python.experience.session_binding.SessionBinding'>
session_id = 'session-alpha'
experience_id = ExperienceId(value='5b639ae9-ede5-4ecc-a331-a162239d284d')

    @classmethod
    def create(
        cls,
        *,
        session_id: str,
        experience_id: ExperienceId,
    ) -> "SessionBinding":
        normalized_session_id = normalize_session_id(session_id)
    
        if not isinstance(experience_id, str):
>           raise InvalidExperienceBindingError(
                "experience_id must be a string identity"
            )
E           lib.python.experience.session_binding.InvalidExperienceBindingError: experience_id must be a string identity

lib/python/experience/session_binding.py:88: InvalidExperienceBindingError
____________ test_binding_rejects_invalid_session_membership_query _____________

    def test_binding_rejects_invalid_session_membership_query():
        experience = Experience.create()
    
>       binding = SessionBinding.create(
            session_id="session-alpha",
            experience_id=experience.experience_id,
        )

tests/experience/test_experience_session_binding.py:152: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

cls = <class 'lib.python.experience.session_binding.SessionBinding'>
session_id = 'session-alpha'
experience_id = ExperienceId(value='9e1a604f-0f8a-45e9-a506-720dd0b84698')

    @classmethod
    def create(
        cls,
        *,
        session_id: str,
        experience_id: ExperienceId,
    ) -> "SessionBinding":
        normalized_session_id = normalize_session_id(session_id)
    
        if not isinstance(experience_id, str):
>           raise InvalidExperienceBindingError(
                "experience_id must be a string identity"
            )
E           lib.python.experience.session_binding.InvalidExperienceBindingError: experience_id must be a string identity

lib/python/experience/session_binding.py:88: InvalidExperienceBindingError
=========================== short test summary info ============================
FAILED tests/experience/test_experience_session_binding.py::test_session_binding_connects_distinct_identities
FAILED tests/experience/test_experience_session_binding.py::test_session_identity_is_not_experience_identity
FAILED tests/experience/test_experience_session_binding.py::test_binding_does_not_replace_experience
FAILED tests/experience/test_experience_session_binding.py::test_binding_preserves_experience_identity
FAILED tests/experience/test_experience_session_binding.py::test_session_id_is_normalized
FAILED tests/experience/test_experience_session_binding.py::test_binding_can_confirm_experience_membership
FAILED tests/experience/test_experience_session_binding.py::test_binding_rejects_other_experience_membership
FAILED tests/experience/test_experience_session_binding.py::test_binding_can_confirm_session_membership
FAILED tests/experience/test_experience_session_binding.py::test_binding_rejects_other_session_membership
FAILED tests/experience/test_experience_session_binding.py::test_binding_rejects_invalid_session_membership_query
10 failed, 6 passed in 0.69s
```

## EXECUTION FAILURE

**Reason:** Session Binding dedicated tests failed

### HEAD
```text
5c82eb85b42e0cc686cd95e8b2ee053c36a62b82
```

### Git Status
```text
?? lib/python/experience/session_binding.py
?? tests/experience/test_experience_session_binding.py
?? work/implementation-reports/PCC-01/PCC-01_SESSION_BINDING_IMPLEMENTATION_REPORT_RUN_010.md
```

**RUN 010: FAIL**

No git add performed.

No commit performed.

No push performed.
