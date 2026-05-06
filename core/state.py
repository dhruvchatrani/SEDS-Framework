import operator
from typing import Annotated, List, Optional, TypedDict, Dict
from pydantic import BaseModel, Field

class StrategicCommunication(BaseModel):
    """Represents a formal strategic turn in the alignment protocol."""
    sender: str
    content: str
    action: str = Field(description="e.g., PROPOSE, REJECT, CONCUR, COUNTER, ANALYZE")

class Proposal(BaseModel):
    """Represents a formal strategic proposal under review."""
    proposing_entity: str
    description: str
    capital_requirement: float
    projected_roi: float
    risk_profile: str

class SEDSState(TypedDict):
    """The Synthetic Enterprise Decision-Support (SEDS) state schema."""
    current_budget: float
    operational_resilience: float
    risk_exposure: float
    # operator.add ensures that new messages are appended to the list, not overwritten
    strategic_log: Annotated[List[StrategicCommunication], operator.add]
    active_proposal: Optional[Proposal]
    alignment_score: float  # 0.0 to 1.0 tracking consensus
    iteration_depth: int
    telemetry_metadata: Dict
