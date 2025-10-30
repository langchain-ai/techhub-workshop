"""
Database Agent - Deployment Configuration

This module provides a deployment-ready instance of the database agent.
The agent is instantiated at module level with deployment configuration,
making it ready for reference in langgraph.json.

For development and workshop purposes, use the factory function:
    from agents import create_db_agent
    db_agent = create_db_agent()  # Uses MemorySaver by default

For deployment, this module provides a fixed configuration:
    langgraph.json → "./deployments/db_agent_graph.py:graph"

Note: Checkpointer is disabled (False) because LangGraph API provides
managed persistence automatically. See: https://docs.langchain.com/oss/python/langgraph/persistence
"""

from agents import create_db_agent

# Module-level graph instance for deployment
# use_checkpointer=False because LangGraph API provides managed persistence
graph = create_db_agent(use_checkpointer=False)
