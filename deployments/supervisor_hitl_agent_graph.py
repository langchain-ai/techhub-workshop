# deployments/supervisor_hitl_agent_graph.py
"""
Deployment wrapper for Customer Verification + Supervisor Agent with HITL.

This is the most complete agent in the workshop, combining:
- Customer identity verification with HITL
- Query classification and routing
- Supervisor agent with specialized sub-agents (DB + Docs)
- State-dependent tools (get_customer_orders uses customer_id from state)

For deployment, the checkpointer is disabled because LangGraph API
provides managed persistence automatically.
"""

from agents.supervisor_hitl_agent import create_supervisor_hitl_agent

# Module-level graph instance for deployment
# use_checkpointer=False because LangGraph API provides managed persistence
graph = create_supervisor_hitl_agent(use_checkpointer=False)
