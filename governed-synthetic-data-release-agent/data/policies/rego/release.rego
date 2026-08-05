package governed_release

default decision := {"decision": "DENY", "rationale": "No allow rule matched"}

decision := {"decision": "SUSPEND", "rationale": "Kill switch enabled"} if { input.kill_switch_enabled }
decision := {"decision": "DENY", "rationale": "Prompt injection or authority violation"} if { count(input.tool_violations) > 0 }
decision := {"decision": "DENY", "rationale": "Privacy threshold failed"} if { not input.privacy_pass }
decision := {"decision": "QUARANTINE", "rationale": "Utility threshold failed"} if { not input.utility_pass }
decision := {"decision": "REQUIRE_APPROVAL", "rationale": "External release needs two approvals"} if { input.external_recipient; count(input.approved_roles) < 2 }
decision := {"decision": "ALLOW", "rationale": "All deterministic controls passed"} if { input.identity_valid; input.authority_valid; input.purpose_valid; input.privacy_pass; input.utility_pass; input.evidence_complete; not input.kill_switch_enabled; count(input.tool_violations) == 0; not input.external_recipient }
decision := {"decision": "ALLOW", "rationale": "All deterministic controls and approvals passed"} if { input.external_recipient; count(input.approved_roles) == 2; input.privacy_pass; input.utility_pass; input.evidence_complete }
