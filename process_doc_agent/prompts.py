ASSESSMENT_PROMPT = """
You are an internal audit AI specialist.

From the provided process documentation, extract:
- process_name
- scope_summary
- ordered process steps with actor, action, system, and control reference if present
- key risks (id, statement, category, likelihood, impact)
- key controls (id, objective, description, frequency, owner, type, mapped risks)

Return strictly valid JSON.
""".strip()

AUDIT_NARRATIVE_PROMPT = """
Create an audit-ready narrative covering:
1) Process objective and scope
2) End-to-end walkthrough by major stage
3) Identified control points
4) Gaps, ambiguities, and assumptions
5) Auditor follow-up requests
""".strip()

RCSA_PROMPT = """
Create a Risk & Control Self-Assessment table in markdown with columns:
Risk ID | Risk Statement | Control ID | Control Description | Design Adequacy | Residual Risk | Action Plan

Use concise, practical language and include remediation actions for weaknesses.
""".strip()
