"""
Supervisor Agent - Deployment Configuration

This module provides a deployment-ready instance of the supervisor agent.
The supervisor coordinates between database and documents agents to handle
customer support queries.

For development and workshop purposes, use the factory function:
    from agents import create_db_agent, create_docs_agent, create_supervisor_agent

    db_agent = create_db_agent()
    docs_agent = create_docs_agent()
    supervisor = create_supervisor_agent(db_agent, docs_agent)

For deployment, this module provides a fixed configuration:
    langgraph.json → "./deployments/supervisor_agent_graph.py:graph"

Note: All agents use use_checkpointer=False because LangGraph API provides
managed persistence automatically. See: https://docs.langchain.com/oss/python/langgraph/persistence
"""

from agents import create_db_agent, create_docs_agent, create_supervisor_agent

# Instantiate sub-agents for deployment (no checkpointer - platform handles it)
db_agent = create_db_agent(use_checkpointer=False)
docs_agent = create_docs_agent(use_checkpointer=False)

# Module-level supervisor graph instance for deployment
# use_checkpointer=False because LangGraph API provides managed persistence
graph = create_supervisor_agent(
    db_agent=db_agent,
    docs_agent=docs_agent,
    use_checkpointer=False,
)
