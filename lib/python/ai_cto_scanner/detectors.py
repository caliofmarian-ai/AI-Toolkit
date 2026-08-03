"""
AI CTO Integration Scanner — Component Detectors

Pattern-based detectors for each architectural category.
Each detector scans the workspace index and file contents for evidence.
"""

import re
from pathlib import Path


# ---------------------------------------------------------------------------
# Detection result
# ---------------------------------------------------------------------------

class ComponentMatch:
    """Evidence of a detected component."""

    def __init__(self, name, files, signals, confidence):
        self.name = name
        self.files = files          # list of file paths containing evidence
        self.signals = signals      # list of matched signal strings
        self.confidence = confidence  # 0.0 – 1.0

    def to_dict(self):
        return {
            "name": self.name,
            "files": self.files[:10],
            "signals": self.signals[:10],
            "confidence": round(self.confidence, 3),
            "found": self.confidence > 0.0,
        }


class DetectionResult:
    """Collection of matches for one architectural category."""

    def __init__(self, category):
        self.category = category
        self.matches = []           # list[ComponentMatch]

    def add(self, match):
        self.matches.append(match)

    @property
    def detected_count(self):
        return sum(1 for m in self.matches if m.confidence > 0.0)

    @property
    def total_count(self):
        return len(self.matches)

    @property
    def score(self):
        if not self.matches:
            return 0.0
        return self.detected_count / self.total_count

    def to_dict(self):
        return {
            "category": self.category,
            "score": round(self.score, 3),
            "detected": self.detected_count,
            "total": self.total_count,
            "components": [m.to_dict() for m in self.matches],
        }


# ---------------------------------------------------------------------------
# Base detector
# ---------------------------------------------------------------------------

class BaseDetector:
    """Base class for all component detectors."""

    # Subclasses define this as a list of (component_name, [signal_patterns])
    COMPONENTS = []

    def detect(self, index, root):
        result = DetectionResult(self.category)
        all_files = list(index.files)
        file_paths = [wf.path.replace("\\", "/") for wf in all_files]
        for name, patterns in self.COMPONENTS:
            match = self._detect_component(name, patterns, all_files, file_paths, root)
            result.add(match)
        return result

    @property
    def category(self):
        return self.__class__.__name__.replace("Detector", "")

    def _detect_component(self, name, patterns, all_files, file_paths, root):
        files_found = []
        signals_found = []

        path_patterns = [p for p in patterns if p.startswith("path:")]
        content_patterns = [p for p in patterns if not p.startswith("path:")]

        for wf in all_files:
            path_lower = wf.path.replace("\\", "/").lower()
            name_lower = wf.name.lower()
            matched_path = False

            for pat in path_patterns:
                keyword = pat[5:].lower()
                if keyword in path_lower or keyword in name_lower:
                    files_found.append(wf.path)
                    signals_found.append("path:%s" % keyword)
                    matched_path = True
                    break

            if matched_path:
                continue

        # Content scan for source files
        source_exts = {".py", ".js", ".ts", ".sh", ".go", ".java", ".rb", ".php"}
        config_exts = {".yaml", ".yml", ".json", ".toml", ".cfg", ".ini", ".env"}
        text_exts = source_exts | config_exts | {".md", ".txt"}

        if content_patterns:
            for wf in all_files:
                if wf.extension not in text_exts:
                    continue
                if wf.size > 500_000:
                    continue
                path_lower = wf.path.replace("\\", "/").lower()
                try:
                    text = (Path(root) / wf.path).read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue
                for pat in content_patterns:
                    if re.search(pat, text, re.IGNORECASE | re.MULTILINE):
                        if wf.path not in files_found:
                            files_found.append(wf.path)
                        if pat not in signals_found:
                            signals_found.append(pat)

        confidence = min(1.0, len(files_found) * 0.4 + len(signals_found) * 0.1) if files_found else 0.0
        confidence = min(1.0, confidence)
        return ComponentMatch(name, files_found[:10], signals_found[:10], confidence)


# ---------------------------------------------------------------------------
# Telegram Detector
# ---------------------------------------------------------------------------

class TelegramDetector(BaseDetector):
    COMPONENTS = [
        ("Bot Entry Point", [
            r"from aiogram",
            r"from telegram",
            r"import telebot",
            r"pyrogram",
            r"Bot\(",
            r"Application\.builder",
            r"Dispatcher\(",
            "path:bot.py",
            "path:bot/",
        ]),
        ("Update Handlers", [
            r"@dp\.message",
            r"@router\.message",
            r"message_handler",
            r"on_message",
            r"MessageHandler",
            r"CommandHandler",
            r"register_message_handler",
        ]),
        ("Callback Handlers", [
            r"@dp\.callback_query",
            r"@router\.callback_query",
            r"callback_query_handler",
            r"CallbackQuery",
            r"CallbackQueryHandler",
            r"on_callback",
        ]),
        ("Inline Keyboards", [
            r"InlineKeyboardMarkup",
            r"InlineKeyboardButton",
            r"inline_keyboard",
            r"InlineKeyboard",
        ]),
        ("Reply Keyboards", [
            r"ReplyKeyboardMarkup",
            r"KeyboardButton",
            r"reply_markup",
            r"ReplyKeyboard",
        ]),
        ("Menu Builders", [
            r"build_menu\b",
            r"create_menu\b",
            r"make_menu\b",
            r"MenuBuilder",
            "path:menu",
        ]),
        ("Dashboard Builders", [
            r"dashboard",
            r"DashboardBuilder",
            "path:dashboard",
        ]),
        ("Admin UI", [
            r"admin[_\s]panel",
            r"admin[_\s]menu",
            r"AdminUI",
            "path:admin",
        ]),
        ("Navigation", [
            r"navigate\b",
            r"Navigation\b",
            r"nav_back",
            r"go_to\b",
            "path:navigation",
        ]),
        ("FSM Integration", [
            r"FSMContext",
            r"StatesGroup",
            r"class\s+\w+\(StatesGroup\)",
            r"State\(\)",
            r"fsm",
            r"finish_dialog",
        ]),
    ]

    @property
    def category(self):
        return "Telegram"


# ---------------------------------------------------------------------------
# Owner Control Detector
# ---------------------------------------------------------------------------

class OwnerControlDetector(BaseDetector):
    COMPONENTS = [
        ("Owner Configuration", [
            r"OWNER_ID",
            r"owner_id\b",
            r"owner_config",
            r"ADMIN_ID",
            "path:owner",
        ]),
        ("Roles", [
            r"\broles?\b",
            r"UserRole",
            r"ROLES\b",
            r"user_role",
            r"assign_role",
        ]),
        ("Permissions", [
            r"\bpermissions?\b",
            r"check_permission",
            r"has_permission",
            r"PERMISSIONS\b",
            r"is_allowed",
        ]),
        ("Admin Dashboard", [
            r"admin_dashboard",
            r"admin_panel",
            r"AdminDashboard",
            "path:admin_dashboard",
        ]),
        ("Owner-Only Operations", [
            r"owner_only",
            r"is_owner\b",
            r"@owner_required",
            r"owner_required",
            r"only_owner",
        ]),
        ("Approval Flow", [
            r"\bapproval\b",
            r"approve\b",
            r"reject\b",
            r"ApprovalFlow",
            r"pending_approval",
        ]),
    ]

    @property
    def category(self):
        return "OwnerControl"


# ---------------------------------------------------------------------------
# Runtime Detector
# ---------------------------------------------------------------------------

class RuntimeDetector(BaseDetector):
    COMPONENTS = [
        ("Startup", [
            r"on_startup",
            r"startup\b",
            r"async def start\b",
            r"if __name__.*__main__",
            "path:startup",
            "path:main.py",
        ]),
        ("Bootstrap", [
            r"bootstrap\b",
            r"Bootstrap\b",
            r"initialize\b",
            r"setup_application\b",
            "path:bootstrap",
        ]),
        ("Runtime", [
            r"\bruntime\b",
            r"RuntimeManager",
            r"ApplicationRuntime",
            "path:runtime",
        ]),
        ("Schedulers", [
            r"apscheduler",
            r"AsyncIOScheduler",
            r"aioschedule",
            r"celery",
            r"scheduler\b",
            r"cron\b",
            "path:scheduler",
        ]),
        ("Workers", [
            r"\bworker\b",
            r"Worker\b",
            r"celery\.task",
            r"@task\b",
            "path:worker",
        ]),
        ("Service Initialization", [
            r"ServiceRegistry",
            r"init_services\b",
            r"setup_services\b",
            r"service_init\b",
            r"register_services\b",
        ]),
    ]

    @property
    def category(self):
        return "Runtime"


# ---------------------------------------------------------------------------
# State Detector
# ---------------------------------------------------------------------------

class StateDetector(BaseDetector):
    COMPONENTS = [
        ("Persistence", [
            r"sqlalchemy",
            r"peewee",
            r"tortoise",
            r"asyncpg",
            r"aiosqlite",
            r"redis",
            r"MongoDB",
            r"database\b",
            "path:db",
            "path:database",
            "path:persistence",
        ]),
        ("State Store", [
            r"MemoryStorage",
            r"RedisStorage",
            r"StateMemory",
            r"storage\b",
            r"state_store\b",
            r"Storage\b",
            "path:storage",
            "path:state_store",
        ]),
        ("Session Management", [
            r"session_id\b",
            r"session_manager",
            r"SessionManager",
            r"get_session\b",
            r"create_session\b",
            "path:session",
        ]),
        ("Snapshot Logic", [
            r"snapshot\b",
            r"Snapshot\b",
            r"save_state\b",
            r"dump_state\b",
            r"serialize_state\b",
            "path:snapshot",
        ]),
        ("Restart Recovery", [
            r"recovery\b",
            r"recover\b",
            r"restore_state\b",
            r"on_restart\b",
            r"crash_recovery",
        ]),
        ("Resume Logic", [
            r"resume\b",
            r"Resume\b",
            r"checkpoint\b",
            r"load_context\b",
            r"restore_context\b",
            "path:resume",
        ]),
    ]

    @property
    def category(self):
        return "State"


# ---------------------------------------------------------------------------
# Configuration Detector
# ---------------------------------------------------------------------------

class ConfigurationDetector(BaseDetector):
    COMPONENTS = [
        ("Configuration Files", [
            "path:config.py",
            "path:config.yaml",
            "path:config.yml",
            "path:config.json",
            "path:settings.py",
            "path:settings.yaml",
        ]),
        ("Environment Variables", [
            r"os\.environ",
            r"os\.getenv",
            r"environ\[",
            r"dotenv",
            r"load_dotenv",
            "path:.env",
        ]),
        ("Secrets References", [
            r"SECRET_KEY",
            r"API_TOKEN",
            r"BOT_TOKEN",
            r"secrets\b",
            r"\.env\.example",
            r"getenv\(.*TOKEN",
            "path:.env.example",
            "path:secrets",
        ]),
        ("Runtime Parameters", [
            r"argparse",
            r"click\.",
            r"typer\.",
            r"sys\.argv",
            r"ArgumentParser",
            r"parse_args\b",
        ]),
    ]

    @property
    def category(self):
        return "Configuration"


# ---------------------------------------------------------------------------
# Canonical Detector
# ---------------------------------------------------------------------------

class CanonicalDetector(BaseDetector):
    COMPONENTS = [
        ("Canonical Specifications", [
            r"CANON-\d+",
            "path:CANON-",
            "path:canonical",
            "path:docs/canonical",
        ]),
        ("Implementation Coverage", [
            r"coverage_engine",
            r"CoverageEngine",
            r"coverage_report",
        ]),
        ("Compliance", [
            r"compliance_engine",
            r"ComplianceEngine",
            r"compliance_report",
        ]),
        ("Architecture Drift", [
            r"drift_engine",
            r"DriftEngine",
            r"drift_report",
            r"architecture.*drift",
        ]),
    ]

    @property
    def category(self):
        return "Canonical"


# ---------------------------------------------------------------------------
# Project Memory Detector
# ---------------------------------------------------------------------------

class ProjectMemoryDetector(BaseDetector):
    COMPONENTS = [
        ("Project Memory", [
            r"project_memory",
            r"ProjectMemory",
            r"memory_engine",
            r"MemoryEngine",
            "path:.ai",
            "path:memory",
        ]),
        ("Development State", [
            r"development_state",
            r"DevState",
            r"dev_state\b",
            r"development_context",
        ]),
        ("Context Persistence", [
            r"context_persistence",
            r"persist_context",
            r"ContextPersistence",
            r"save_context\b",
            "path:context",
        ]),
        ("Resume Engine", [
            r"resume_engine",
            r"ResumeEngine",
            r"context_engine",
            r"ContextEngine",
            "path:resume_engine",
            "path:context_engine",
        ]),
        ("Context Integrity", [
            r"context_integrity",
            r"ContextIntegrity",
            r"integrity_check",
            r"verify_context",
        ]),
        ("Snapshot Engine", [
            r"snapshot_engine",
            r"SnapshotEngine",
            r"context_snapshot",
            "path:snapshot_engine",
        ]),
    ]

    @property
    def category(self):
        return "ProjectMemory"
