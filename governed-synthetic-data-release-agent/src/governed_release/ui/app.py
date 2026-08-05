from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import httpx
import pandas as pd
import streamlit as st

API_URL = os.getenv("GOVERNED_RELEASE_API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Governed Synthetic Data Release", page_icon="🛡️", layout="wide")
st.title("🛡️ Governed Autonomous Synthetic Data Release Agent")
st.caption("When an AI Agent Decides Whether Data May Leave the Vault")
st.info(
    "The LLM interprets and explains. Deterministic code calculates. Policy decides. Humans accept residual risk. Only the export gateway releases."
)


def api(method: str, path: str, **kwargs: Any) -> Any:
    try:
        response = httpx.request(method, f"{API_URL}{path}", timeout=360, **kwargs)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as exc:
        st.error(f"API error: {exc}")
        return None


scenario_labels = {
    "Internal sandbox release allowed": "internal_allow",
    "External release requires approval": "external_approval",
    "Privacy leakage detected": "privacy_leakage",
    "Prompt injection and exfiltration attempt": "prompt_injection",
}
with st.sidebar:
    st.header("Demo control")
    selected_label = st.selectbox("Scenario", list(scenario_labels))
    if st.button("Run scenario", type="primary", use_container_width=True):
        result = api("POST", f"/workflows/run/{scenario_labels[selected_label]}")
        if result:
            st.session_state["workflow"] = result
    if st.button("Refresh current", use_container_width=True) and st.session_state.get("workflow"):
        workflow_id = st.session_state["workflow"]["workflow_id"]
        result = api("GET", f"/workflows/{workflow_id}")
        if result:
            st.session_state["workflow"] = result
    st.divider()
    st.write("API", API_URL)
    health = api("GET", "/health")
    st.success("Connected") if health else st.warning("Start with `make demo`")

state = st.session_state.get("workflow")
if not state:
    st.markdown(
        "Choose one of the four scenarios and run it. The workflow persists in SQLite and can be resumed after approvals."
    )
    st.stop()

request = state["request"]
classification_tab, generation_tab, metrics_tab, decision_tab, timeline_tab = st.tabs(
    [
        "1 · Request",
        "2 · Classification",
        "3 · Generation",
        "4 · Privacy & Utility",
        "5 · Decision & Evidence",
    ]
)

with classification_tab:
    st.subheader("Data-release request")
    cols = st.columns(3)
    cols[0].metric("Requester", request["requester"]["display_name"])
    cols[1].metric("Role", request["requester"]["role"])
    cols[2].metric("Requested rows", request["requested_rows"])
    st.json(
        {
            "request_id": state["request_id"],
            "workflow_id": state["workflow_id"],
            "trace_id": state["trace_id"],
            "agent_identity": request["agent"],
            "purpose": request["purpose"],
            "intended_use": request["intended_use"],
            "recipient": request["recipient"],
            "destination": request["destination"],
            "release_duration_days": request["release_duration_days"],
        }
    )

with generation_tab:
    st.subheader("Deterministic field classification")
    classifications = pd.DataFrame(state.get("classifications") or [])
    if not classifications.empty:
        st.dataframe(
            classifications[
                [
                    "field_name",
                    "field_class",
                    "disposition",
                    "detection_method",
                    "confidence",
                    "rule_id",
                    "reason",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )
        permitted = classifications[classifications["disposition"] == "RELEASE_PERMITTED"][
            "field_name"
        ].tolist()
        removed = classifications[classifications["disposition"] == "RELEASE_PROHIBITED"][
            "field_name"
        ].tolist()
        c1, c2 = st.columns(2)
        c1.success("Permitted: " + ", ".join(permitted))
        c2.error("Removed: " + ", ".join(removed))
    else:
        st.warning("Classification did not run for this blocked request.")

with metrics_tab:
    st.subheader("Generation")
    plan = state.get("generation_plan")
    run = state.get("generation_run")
    if plan:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Generator", run["generator"] if run else plan["generator"])
        c2.metric("Rows", run["row_count"] if run else plan["requested_rows"])
        c3.metric("Runtime (s)", run["runtime_seconds"] if run else "pending")
        c4.metric("Candidate ID", state["candidate_id"])
        st.progress(1.0 if run else 0.4)
        st.json({"plan": plan, "run": run, "current_state": state["stage"]})
    else:
        st.warning("Generation was blocked before a plan could execute.")

with decision_tab:
    st.subheader("Privacy and analytical utility")
    utility = state.get("utility_report")
    privacy = state.get("privacy_report")
    if utility and privacy:
        cols = st.columns(4)
        cols[0].metric(
            "Utility score",
            utility["normalized_utility_score"],
            f"threshold {utility['threshold']}",
        )
        cols[1].metric("Fraud ROC-AUC", utility["fraud_roc_auc"])
        cols[2].metric("Exact match rate", privacy["exact_match_rate"])
        cols[3].metric("Privacy risk", privacy["risk_category"])
        st.write("Utility")
        st.json(utility)
        st.write("Privacy")
        st.json(privacy)
    else:
        st.warning("Evaluators did not run because the Control Plane blocked the request earlier.")

with timeline_tab:
    decision = state.get("decision") or "PENDING"
    st.subheader(f"Control Plane decision: {decision}")
    policy = state.get("policy_decision")
    if policy:
        if decision == "ALLOW":
            st.success(policy["rationale"])
        elif decision == "REQUIRE_APPROVAL":
            st.warning(policy["rationale"])
        else:
            st.error(policy["rationale"])
        st.json(
            {
                "agent_recommendation": "Interpretation only; not authoritative",
                "metric_result": {
                    "utility": state.get("utility_report"),
                    "privacy": state.get("privacy_report"),
                },
                "policy_decision": policy,
                "human_decisions": state.get("approvals"),
                "export_status": state.get("export_receipt"),
                "kill_switch_status": "checked by policy and gateway",
            }
        )

    if decision == "REQUIRE_APPROVAL":
        st.markdown("### Independent approval checkpoint")
        approval_roles = {item["role"] for item in state.get("approvals", [])}
        c1, c2 = st.columns(2)
        if "DATA_OWNER" not in approval_roles and c1.button(
            "Approve as Data Owner", use_container_width=True
        ):
            result = api(
                "POST",
                f"/workflows/{state['workflow_id']}/approve",
                json={
                    "role": "DATA_OWNER",
                    "approver_id": "data_owner_001",
                    "comment": "Reviewed purpose, recipient, privacy, utility and evidence.",
                    "outcome": "APPROVE",
                },
            )
            if result:
                st.session_state["workflow"] = result
                st.rerun()
        if "PRIVACY_OFFICER" not in approval_roles and c2.button(
            "Approve as Privacy Officer", use_container_width=True
        ):
            result = api(
                "POST",
                f"/workflows/{state['workflow_id']}/approve",
                json={
                    "role": "PRIVACY_OFFICER",
                    "approver_id": "privacy_officer_001",
                    "comment": "Reviewed residual auxiliary-data risk and release duration.",
                    "outcome": "APPROVE",
                },
            )
            if result:
                st.session_state["workflow"] = result
                st.rerun()
        if st.button("Resume after approvals", type="primary"):
            result = api("POST", f"/workflows/{state['workflow_id']}/resume")
            if result:
                st.session_state["workflow"] = result
                st.rerun()

    st.markdown("### Evidence artifacts")
    evidence = pd.DataFrame(state.get("evidence_artifacts") or [])
    if not evidence.empty:
        st.dataframe(
            evidence[["artifact_type", "path", "sha256"]], use_container_width=True, hide_index=True
        )
        zip_rows = evidence[evidence["path"].str.endswith("evidence_bundle.zip")]
        if not zip_rows.empty:
            path = Path(zip_rows.iloc[0]["path"])
            if path.exists():
                st.download_button(
                    "Download evidence ZIP",
                    path.read_bytes(),
                    file_name=f"{state['workflow_id']}-evidence.zip",
                    mime="application/zip",
                )
    receipt = state.get("export_receipt")
    if decision == "ALLOW" and receipt:
        released = Path(receipt["released_path"])
        if released.exists():
            st.download_button(
                "Download authorized released dataset",
                released.read_bytes(),
                file_name=released.name,
                mime="text/csv",
            )
