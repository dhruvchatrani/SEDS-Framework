from mcp.server.fastmcp import FastMCP
import random

# Initialize a lightweight FastMCP server
mcp = FastMCP("MAES_Market_Server")

@mcp.tool()
def get_market_environment(sector: str) -> str:
    """Fetch the current market trend and identify any supply shocks for a given sector."""
    # Pragmatic mock data focusing on the "Supply Shock" scenario from the PRD
    shocks = [
        "Stable: No current disruptions.",
        "Warning: Minor logistics delays.",
        "CRITICAL SUPPLY SHOCK: 40% cost increase in raw materials. Immediate budget re-allocation recommended."
    ]
    # Weighting the shock to ensure it appears frequently for demonstration purposes
    selected_shock = random.choices(shocks, weights=[0.2, 0.3, 0.5])[0]
    return f"Sector: {sector} | Trend: Highly Volatile | Market Status: {selected_shock}"

@mcp.tool()
def get_corporate_ledger() -> str:
    """Fetch the latest corporate ledger summary to enforce constraints."""
    return "Runway: 12 months. Burn rate: $85,000/month. Total Liquid Capital: $1,020,000. Maximum single-project allocation policy: 10%."

if __name__ == "__main__":
    # Run the server via standard input/output for easy client integration
    mcp.run()
