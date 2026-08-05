from __future__ import annotations

import argparse
import json

from governed_release.application.evidence import verify_evidence_directory
from governed_release.application.workflow import build_service
from governed_release.domain.enums import ApprovalOutcome, ApprovalRole, Scenario


def main() -> None:
    parser = argparse.ArgumentParser(prog="governed-release")
    sub = parser.add_subparsers(dest="command", required=True)
    scenario = sub.add_parser("scenario")
    scenario.add_argument("name", choices=[item.value for item in Scenario])
    approve = sub.add_parser("approve")
    approve.add_argument("workflow_id")
    approve.add_argument("role", choices=[item.value for item in ApprovalRole])
    approve.add_argument("approver_id")
    approve.add_argument("--comment", default="Reviewed local demonstration evidence.")
    resume = sub.add_parser("resume")
    resume.add_argument("workflow_id")
    sub.add_parser("list")
    verify = sub.add_parser("verify-evidence")
    verify.add_argument("workflow_id")
    args = parser.parse_args()
    service = build_service()
    if args.command == "scenario":
        result = service.run_scenario(args.name)
    elif args.command == "approve":
        result = service.approve(
            args.workflow_id, args.role, args.approver_id, args.comment, ApprovalOutcome.APPROVE
        )
    elif args.command == "resume":
        result = service.resume(args.workflow_id)
    elif args.command == "list":
        print(
            json.dumps(
                [s.model_dump(mode="json") for s in service.store.list()], indent=2, default=str
            )
        )
        return
    else:
        ok, errors = verify_evidence_directory(
            service.settings.data_dir / "evidence" / args.workflow_id
        )
        print(json.dumps({"valid": ok, "errors": errors}, indent=2))
        raise SystemExit(0 if ok else 1)
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
