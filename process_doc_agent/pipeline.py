from pathlib import Path
from typing import Dict, List

from process_doc_agent.models import ControlItem, ProcessAssessment, ProcessStep, RiskItem
from process_doc_agent.renderers import to_audit_narrative, to_mermaid, to_rcsa_markdown


class MockLLMClient:
    """Simple deterministic parser-like fallback for starter usage."""

    def assess(self, source_text: str) -> ProcessAssessment:
        _ = source_text  # placeholder for real model usage
        return ProcessAssessment(
            process_name="Procure-to-Pay",
            scope_summary="Assessment of requisition, approval, purchase order, receipt, and invoice payment.",
            steps=[
                ProcessStep(id="S1", actor="Requester", action="Creates requisition", system="ERP", control_ref="C1"),
                ProcessStep(id="S2", actor="Manager", action="Approves requisition", system="ERP", control_ref="C1"),
                ProcessStep(id="S3", actor="Procurement", action="Issues purchase order", system="ERP", control_ref="C2"),
                ProcessStep(id="S4", actor="AP", action="Performs three-way match and posts invoice", system="ERP", control_ref="C3"),
                ProcessStep(id="S5", actor="Treasury", action="Executes payment run", system="Bank Portal", control_ref="C4"),
            ],
            risks=[
                RiskItem(id="R1", statement="Unauthorized purchases", category="Compliance", likelihood="Medium", impact="High"),
                RiskItem(id="R2", statement="Duplicate or invalid invoice payment", category="Financial", likelihood="Medium", impact="High"),
            ],
            controls=[
                ControlItem(
                    id="C1",
                    objective="Only valid requisitions are approved",
                    description="Manager approval required before PO creation",
                    frequency="Per transaction",
                    owner="Department Manager",
                    control_type="Preventive",
                    mapped_risks=["R1"],
                ),
                ControlItem(
                    id="C3",
                    objective="Prevent payment errors",
                    description="Three-way match between PO, receipt, and invoice",
                    frequency="Per transaction",
                    owner="Accounts Payable",
                    control_type="Preventive",
                    mapped_risks=["R2"],
                ),
            ],
        )


def load_inputs(input_dir: Path) -> str:
    chunks: List[str] = []
    for file_path in sorted(input_dir.glob("*.txt")):
        chunks.append(file_path.read_text(encoding="utf-8"))
    return "\n\n".join(chunks)


def generate_artifacts_from_text(source_text: str) -> Dict[str, str]:
    llm = MockLLMClient()
    assessment = llm.assess(source_text)

    return {
        "audit_narrative.md": to_audit_narrative(assessment),
        "process_flowchart.mmd": to_mermaid(assessment),
        "rcsa.md": to_rcsa_markdown(assessment),
    }


def run_pipeline(input_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    source_text = load_inputs(input_dir)
    artifacts = generate_artifacts_from_text(source_text)

    for filename, content in artifacts.items():
        (output_dir / filename).write_text(content, encoding="utf-8")
