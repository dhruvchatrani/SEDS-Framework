from typing import Any, Dict, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from core.state import SEDSState

class SimulationAgent:
    """
    Base class for SEDS agents. Manages strategic role execution, 
    contextual state analysis, and structured decision output.
    """
    def __init__(self, name: str, system_prompt: str, llm: Any):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = llm
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("placeholder", "{messages}")
        ])
        self.chain = self.prompt_template | self.llm

    def run(self, state: SEDSState, structured_output_type: Any = None):
        """Invoke the agent chain with strategic context handling."""
        context = self.format_state_context(state)
        messages = state.get("strategic_log", [])
        
        formatted_messages = []
        for m in messages:
            from langchain_core.messages import AIMessage
            formatted_messages.append(AIMessage(content=f"{m.sender} ({m.action}): {m.content}"))
            
        if not formatted_messages:
            formatted_messages = [HumanMessage(content="The strategic alignment protocol has initiated. Analyze the current enterprise state and provide your initial assessment.")]

        chain = self.chain
        if structured_output_type:
            chain = self.prompt_template | self.llm.with_structured_output(structured_output_type)
            
        return chain.invoke({"messages": formatted_messages, "state_context": context})

    def format_state_context(self, state: SEDSState) -> str:
        """Serializes current enterprise metrics for LLM ingestion."""
        budget = state.get("current_budget", 0.0)
        resilience = state.get("operational_resilience", 0.0)
        risk = state.get("risk_exposure", 0.0)
        proposal = state.get("active_proposal")
        
        context = f"ENTREPRISE METRICS -> Fiscal Runway: ${budget}M | Operational Resilience: {resilience}% | Risk Exposure: {risk}%\n"
        if proposal:
            context += (f"ACTIVE STRATEGIC PROPOSAL: {proposal.description}\n"
                        f"- Capital Requirement: ${proposal.capital_requirement}M\n"
                        f"- Projected ROI: {proposal.projected_roi}%\n"
                        f"- Risk Profile: {proposal.risk_profile}")
        else:
            context += "ACTIVE STRATEGIC PROPOSAL: None"
            
        return context

# --- Strategic Persona Definitions ---

CEO_PROMPT = """You are the Chief Executive Officer (CEO). Your objective is high-level strategic alignment and long-term organizational health.
You must adjudicate between conflicting departmental priorities (Finance, Ops, Risk). 
Your tone is pragmatic, decisive, and executive. Avoid corporate jargon; speak with the directness of a high-stakes decision-maker.
If consensus is not reached within the protocol depth, you must exercise tie-breaking authority to ensure operational continuity.
State Context:
{state_context}"""

FINANCE_PROMPT = """You are the Chief Financial Officer (CFO). Your mandate is fiscal discipline, ROI optimization, and runway preservation.
You are naturally skeptical of high-capital expenditures without clear, quantifiable returns. 
Analyze all proposals against a 15% ROI benchmark and a 10% maximum capital allocation per initiative.
Be analytically rigorous and direct. Challenge assumptions that threaten the enterprise's fiscal stability.
State Context:
{state_context}"""

OPS_PROMPT = """You are the Chief Operating Officer (COO). Your mandate is execution velocity, scalability, and operational throughput.
You prioritize growth and infrastructure modernization. You view excessive caution as a 'growth tax'.
Propose aggressive operational expansions and defend them against fiscal or regulatory 'red tape'.
Your tone is action-oriented and efficiency-focused.
State Context:
{state_context}"""

RISK_PROMPT = """You are the Chief Risk Officer (CRO). Your mandate is enterprise stability, compliance, and failure-mode mitigation.
You analyze proposals for systemic vulnerabilities, 'black swan' risks, and operational edge cases.
You provide the cynical, necessary counter-balance to aggressive growth.
Your tone is cautious, evidence-based, and focused on resilience.
State Context:
{state_context}"""
