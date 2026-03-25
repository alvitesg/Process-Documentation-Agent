from process_doc_agent.models import ProcessAssessment


def to_mermaid(assessment: ProcessAssessment) -> str:
    lines = ["flowchart TD"]

    for idx, step in enumerate(assessment.steps):
        node_id = step.id.replace("-", "_")
        label = f"{step.actor}: {step.action}"
        lines.append(f"    {node_id}[\"{label}\"]")
        if idx > 0:
            prev_id = assessment.steps[idx - 1].id.replace("-", "_")
            lines.append(f"    {prev_id} --> {node_id}")

    return "\n".join(lines) + "\n"


def to_audit_narrative(assessment: ProcessAssessment) -> str:
    bullets = "\n".join(
        f"- **{s.id}** ({s.actor}) {s.action}" + (f" [System: {s.system}]" if s.system else "")
        for s in assessment.steps
    )
    controls = "\n".join(
        f"- **{c.id}**: {c.description} (Owner: {c.owner}, Frequency: {c.frequency})"
        for c in assessment.controls
    )

    return f"""# Audit Narrative: {assessment.process_name}

## Scope Summary
{assessment.scope_summary}

## Process Walkthrough
{bullets}

## Control Points
{controls}

## Noted Gaps / Follow-ups
- Validate whether all critical approvals are evidenced and retained.
- Confirm segregation of duties across initiation, approval, and posting.
- Obtain samples for control operating effectiveness testing.
"""


def to_rcsa_markdown(assessment: ProcessAssessment) -> str:
    header = (
        "| Risk ID | Risk Statement | Control ID | Control Description | Design Adequacy | "
        "Residual Risk | Action Plan |\n"
        "|---|---|---|---|---|---|---|\n"
    )

    rows = []
    for risk in assessment.risks:
        related_controls = [c for c in assessment.controls if risk.id in c.mapped_risks]
        if not related_controls:
            rows.append(
                f"| {risk.id} | {risk.statement} | N/A | No mapped control identified. | "
                "Weak | High | Design and implement preventive/detective control. |"
            )
            continue

        for ctrl in related_controls:
            rows.append(
                f"| {risk.id} | {risk.statement} | {ctrl.id} | {ctrl.description} | "
                "Moderate | Medium | Enhance documentation and evidence retention. |"
            )

    return header + "\n".join(rows) + "\n"
