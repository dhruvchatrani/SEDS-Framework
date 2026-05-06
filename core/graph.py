import os
from typing import Literal
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

# Load environment variables (API Keys) before initializing agents/LLM
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from core.state import SEDSState, StrategicCommunication, Proposal
from agents.base import SimulationAgent, CEO_PROMPT, FINANCE_PROMPT, OPS_PROMPT, RISK_PROMPT

# Initialize LLM strictly with the required model
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview")

# Instantiate Strategic Agents
ops_agent = SimulationAgent("COO", OPS_PROMPT, llm)
finance_agent = SimulationAgent("CFO", FINANCE_PROMPT, llm)
risk_agent = SimulationAgent("CRO", RISK_PROMPT, llm)
ceo_agent = SimulationAgent("CEO", CEO_PROMPT, llm)

# --- Node Definitions ---

def strategic_planning_node(state: SEDSState):
    """COO proposes or revises an operational growth initiative."""
    proposal_result = ops_agent.run(state, structured_output_type=Proposal)
    
    msg = StrategicCommunication(
        sender="COO", 
        content=f"Proposed strategic initiative: {proposal_result.description}", 
        action="PROPOSE"
    )
    return {"active_proposal": proposal_result, "strategic_log": [msg]}

def fiscal_validation_node(state: SEDSState):
    """CFO validates the proposal against ROI and budget benchmarks."""
    review_msg = finance_agent.run(state, structured_output_type=StrategicCommunication)
    review_msg.sender = "CFO"
    return {"strategic_log": [review_msg]}

def risk_assessment_node(state: SEDSState):
    """CRO stress-tests the proposal for systemic vulnerabilities."""
    review_msg = risk_agent.run(state, structured_output_type=StrategicCommunication)
    review_msg.sender = "CRO"
    return {"strategic_log": [review_msg]}

def executive_adjudication_node(state: SEDSState):
    """CEO evaluates cross-departmental feedback and determines alignment score."""
    ceo_msg = ceo_agent.run(state, structured_output_type=StrategicCommunication)
    ceo_msg.sender = "CEO"
    
    # Calculate a mock alignment score based on CEO action for now
    # In a real system, this would be a more complex heuristic
    alignment_map = {"CONCUR": 1.0, "PROPOSE": 0.5, "REJECT": 0.2, "COUNTER": 0.4, "ANALYZE": 0.6}
    current_alignment = alignment_map.get(ceo_msg.action, 0.3)
    
    current_depth = state.get("iteration_depth", 0)
    return {
        "strategic_log": [ceo_msg], 
        "iteration_depth": current_depth + 1,
        "alignment_score": current_alignment
    }
    
def consensus_routing_logic(state: SEDSState) -> Literal["strategic_planning_node", "__end__"]:
    """Determines protocol termination based on alignment score or depth limit."""
    if state.get("iteration_depth", 0) >= 4:
        return "__end__"
    
    if state.get("alignment_score", 0.0) >= 0.8:
        return "__end__"
        
    return "strategic_planning_node"

# --- Protocol Construction ---

builder = StateGraph(SEDSState)

builder.add_node("strategic_planning_node", strategic_planning_node)
builder.add_node("fiscal_validation_node", fiscal_validation_node)
builder.add_node("risk_assessment_node", risk_assessment_node)
builder.add_node("executive_adjudication_node", executive_adjudication_node)

builder.add_edge(START, "strategic_planning_node")
builder.add_edge("strategic_planning_node", "fiscal_validation_node")
builder.add_edge("strategic_planning_node", "risk_assessment_node")

# Fan-in to CEO adjudication
builder.add_edge("fiscal_validation_node", "executive_adjudication_node")
builder.add_edge("risk_assessment_node", "executive_adjudication_node")

# Iterative alignment loop
builder.add_conditional_edges("executive_adjudication_node", consensus_routing_logic)

maes_graph = builder.compile() # Keeping variable name for compatibility with test_run.py for now
