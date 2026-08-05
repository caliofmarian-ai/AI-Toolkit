#!/usr/bin/env bash
set -e

# CSL Governance Kernel Tests
# Tests the Safety and Governance Kernel components
# CSL Reference: Volume VII (Safety and Governance), RFC-0005
# CORE: CORE-023-011

python3 - <<'PY'
import sys
sys.path.insert(0, "lib")

from python.rule_engine import (
    GovernanceKernel,
    Permission,
    PermissionCategory,
    RiskLevel,
    ApprovalStatus,
    ApprovalRequiredError,
    EmergencyStopError,
)

print("=== CSL Governance Kernel ===")

kernel = GovernanceKernel()
kernel.permissions.grant(Permission(PermissionCategory.EXECUTE, "*"))

# GK-01: Auto-approve low-risk actions
approval = kernel.authorize("compile", actor="test")
assert approval.status == ApprovalStatus.AUTO_APPROVED, f"GK-01 FAIL: {approval.status}"
print("GK-01 PASS: Low-risk action auto-approved")

# GK-02: Auto-approve read actions
approval2 = kernel.authorize("read", actor="test")
assert approval2.status == ApprovalStatus.AUTO_APPROVED, f"GK-02 FAIL: {approval2.status}"
print("GK-02 PASS: Read action auto-approved")

# GK-03: Block high-risk actions without explicit approval
try:
    kernel.authorize("deploy", actor="test")
    assert False, "GK-03 FAIL: deploy should require approval"
except ApprovalRequiredError as e:
    assert "deploy" in str(e).lower()
    print("GK-03 PASS: High-risk deploy blocked pending approval")

# GK-04: Explicit approval unlocks high-risk action
approval3 = kernel.approvals.request("deploy", RiskLevel.HIGH)
kernel.approvals.approve(approval3.approval_id, approved_by="human-reviewer")
assert kernel.approvals.is_approved(approval3.approval_id)
print("GK-04 PASS: Explicit approval recorded")

# GK-05: Emergency stop blocks all actions
kernel.emergency_stop.activate("test emergency", activated_by="admin")
try:
    kernel.authorize("compile", actor="test")
    assert False, "GK-05 FAIL: should be blocked by emergency stop"
except EmergencyStopError:
    print("GK-05 PASS: Emergency stop blocks all actions")

# GK-06: Emergency stop can be deactivated
kernel.emergency_stop.deactivate("admin")
assert not kernel.emergency_stop.is_active
approval4 = kernel.authorize("compile", actor="test")
assert approval4.status == ApprovalStatus.AUTO_APPROVED
print("GK-06 PASS: Emergency stop deactivated, actions resume")

# GK-07: Audit log records all events
records = kernel.audit.all_records()
assert len(records) >= 3, f"GK-07 FAIL: expected >= 3 audit records, got {len(records)}"
print(f"GK-07 PASS: {len(records)} audit records generated")

# GK-08: Risk classification
risk_read = kernel.risk.classify("read")
assert risk_read.level == RiskLevel.NONE
risk_deploy = kernel.risk.classify("deploy")
assert risk_deploy.requires_approval
risk_modify = kernel.risk.classify("modify_canonical")
assert risk_modify.level == RiskLevel.CRITICAL
print("GK-08 PASS: Risk classification correct (read=NONE, deploy=HIGH, modify_canonical=CRITICAL)")

print("\nCSL Governance Kernel: ALL PASS")
PY
