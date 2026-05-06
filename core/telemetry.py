import json
import os
from datetime import datetime
from typing import Any, Dict, List
from core.state import SEDSState

class SEDS_Telemetry:
    """
    Handles structured data persistence and metric extraction for 
    Synthetic Enterprise Decision-Support (SEDS) runs.
    """
    
    def __init__(self, log_dir: str = "artifacts/telemetry"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)

    def log_session(self, final_state: SEDSState, execution_time: float) -> str:
        """
        Serializes the final state and metadata into a JSON artifact.
        Returns the path to the saved artifact.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_id = final_state.get("telemetry_metadata", {}).get("session_id", f"sim_{timestamp}")
        
        artifact = {
            "session_id": session_id,
            "timestamp": timestamp,
            "execution_metrics": {
                "total_execution_time_sec": execution_time,
                "iteration_depth": final_state.get("iteration_depth", 0),
                "final_alignment_score": final_state.get("alignment_score", 0.0)
            },
            "enterprise_metrics": {
                "remaining_budget": final_state.get("current_budget"),
                "operational_resilience": final_state.get("operational_resilience"),
                "risk_exposure": final_state.get("risk_exposure")
            },
            "strategic_log": [
                {
                    "sender": turn.sender,
                    "action": turn.action,
                    "content": turn.content
                } for turn in final_state.get("strategic_log", [])
            ],
            "final_proposal": final_state.get("active_proposal").dict() if final_state.get("active_proposal") else None
        }
        
        file_path = os.path.join(self.log_dir, f"{session_id}.json")
        with open(file_path, "w") as f:
            json.dump(artifact, f, indent=4)
            
        return file_path

    @staticmethod
    def extract_summary(final_state: SEDSState) -> str:
        """Generates a professional executive summary of the run."""
        summary = "=== EXECUTIVE STRATEGIC SUMMARY ===\n"
        summary += f"Status: {'CONVERGED' if final_state.get('alignment_score', 0) > 0.7 else 'DIVERGED'}\n"
        summary += f"Alignment Score: {final_state.get('alignment_score', 0.0)*100:.1f}%\n"
        summary += f"Operational Resilience: {final_state.get('operational_resilience', 0.0)}%\n"
        summary += f"Risk Exposure: {final_state.get('risk_exposure', 0.0)}%\n"
        summary += "===================================="
        return summary
