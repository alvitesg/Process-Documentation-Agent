from dataclasses import dataclass, field
from typing import List


@dataclass
class ProcessStep:
    id: str
    actor: str
    action: str
    system: str = ""
    control_ref: str = ""


@dataclass
class RiskItem:
    id: str
    statement: str
    category: str
    likelihood: str
    impact: str


@dataclass
class ControlItem:
    id: str
    objective: str
    description: str
    frequency: str
    owner: str
    control_type: str
    mapped_risks: List[str] = field(default_factory=list)


@dataclass
class ProcessAssessment:
    process_name: str
    scope_summary: str
    steps: List[ProcessStep]
    risks: List[RiskItem]
    controls: List[ControlItem]
