import os
import time
from dotenv import load_dotenv
from core.graph import maes_graph
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from tools.mcp_server import get_market_environment, get_corporate_ledger
from core.state import StrategicCommunication
from core.telemetry import MAES_Telemetry

load_dotenv()

class MDEFScore(BaseModel):
    """Multi-Dimensional Evaluation Framework (MDEF) Scorecard."""
    strategic_fidelity: int = Field(description="0-100: How well agents adhered to their mandated strategic personas.")
    alignment_efficiency: int = Field(description="0-100: Speed and quality of consensus reaching.")
    resilience_rating: int = Field(description="0-100: Ability to maintain organizational stability under shock.")
    executive_summary: str = Field(description="Professional 2-sentence summary of simulation outcomes.")

def run_maes_protocol():
    if not os.environ.get("GOOGLE_API_KEY"):
        print("ERROR: GOOGLE_API_KEY not found in .env")
        return

    telemetry = MAES_Telemetry()
    
    print("🛡️  INITIALIZING MAES PROTOCOL: EXTERNAL SHOCK SCENARIO\n")
    
    print("📡 Querying Industrial Intelligence via MCP...")
    market_context = get_market_environment("Enterprise Infrastructure")
    ledger_context = get_corporate_ledger()
    
    # Inject exogenous shock
    initial_shock = StrategicCommunication(
        sender="ENVIRONMENTAL_ORACLE",
        content=f"EXOGENOUS DISRUPTION DETECTED: {market_context} | FISCAL CONSTRAINTS: {ledger_context}",
        action="INJECT_SHOCK"
    )
    
    initial_state = {
        "current_budget": 100.0,
        "operational_resilience": 75.0,
        "risk_exposure": 10.0,
        "strategic_log": [initial_shock],
        "active_proposal": None,
        "alignment_score": 0.0,
        "iteration_depth": 0,
        "telemetry_metadata": {"session_id": f"MAES_RUN_{int(time.time())}", "shock_type": "MARKET_VOLATILITY"}
    }

    try:
        start_time = time.time()
        final_state = maes_graph.invoke(initial_state)
        execution_time = round(time.time() - start_time, 2)
        
        # Persistence & Telemetry
        artifact_path = telemetry.log_session(final_state, execution_time)
        
        print("\n" + telemetry.extract_summary(final_state))
        print(f"📄 Full Telemetry Artifact: {artifact_path}\n")
        
        print("🔍 Initiating Multi-Dimensional Evaluation (MDEF)...\n")
        eval_llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview").with_structured_output(MDEFScore)
        
        transcript = "\n".join([f"[{m.sender}]: {m.content}" for m in final_state.get("strategic_log", [])])
        eval_prompt = f"""
        Analyze the following Multi-Agent Enterprise Simulation (MAES) transcript.
        The simulation involved a COO, CFO, CRO, and CEO navigating an exogenous shock.
        
        Evaluate based on:
        1. Strategic Fidelity: Did the CFO prioritize fiscal discipline? Did the COO push growth?
        2. Alignment Efficiency: How effectively did the CEO steer them toward consensus?
        3. Resilience: Was the final strategic posture stable?
        
        Transcript:
        {transcript}
        """
        
        score = eval_llm.invoke(eval_prompt)
        print(f"🎯 Strategic Fidelity: {score.strategic_fidelity}/100")
        print(f"📈 Alignment Efficiency: {score.alignment_efficiency}/100")
        print(f"🛡️  Resilience Rating: {score.resilience_rating}/100")
        print(f"📝 Executive Insight: {score.executive_summary}\n")

    except Exception as e:
        print(f"\n❌ Protocol Failure: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_maes_protocol()
