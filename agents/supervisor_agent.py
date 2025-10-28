"""Supervisor agent for TechHub customer support.

This supervisor coordinates between specialized sub-agents (Database and Documents)
to handle customer queries. It routes queries to the appropriate specialist(s) and
can orchestrate parallel or sequential coordination when needed.
"""

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver


def create_supervisor_agent(db_agent, docs_agent):
    """Create supervisor agent that routes between database and documents agents.

    Args:
        db_agent: Compiled database agent graph
        docs_agent: Compiled documents agent graph

    Returns:
        Compiled supervisor agent graph that can route to specialists.
    """

    # Wrap Database Agent as a tool
    @tool
    def database_specialist(query: str) -> str:
        """Consult the database specialist for structured data queries.

        This specialist has access to TechHub's operational database and can:
        - Look up order status and tracking information
        - Retrieve customer order history
        - Check product prices and inventory availability

        Use this specialist when the user needs real-time operational data
        (orders, inventory, pricing) rather than product details or policies.

        Args:
            query: The question to ask the database specialist (may be rephrased by supervisor)

        Returns:
            The database specialist's answer based on current database records
        """
        result = db_agent.invoke({"messages": [{"role": "user", "content": query}]})
        return result["messages"][-1].content

    # Wrap Documents Agent as a tool
    @tool
    def documentation_specialist(query: str) -> str:
        """Consult the documentation specialist for product information and policies.

        This specialist has access to TechHub's documentation library and can:
        - Look up product specifications, features, and technical details
        - Explain return, refund, and warranty policies
        - Provide shipping and delivery information
        - Answer questions about product compatibility and setup

        Use this specialist when the user needs detailed product information,
        policy explanations, or guidance (not real-time operational data).

        Args:
            query: The question to ask the documentation specialist (may be rephrased by supervisor)

        Returns:
            The documentation specialist's answer based on product docs and policies
        """
        result = docs_agent.invoke({"messages": [{"role": "user", "content": query}]})
        return result["messages"][-1].content

    llm = init_chat_model("anthropic:claude-haiku-4-5")

    return create_agent(
        model=llm,
        tools=[database_specialist, documentation_specialist],
        system_prompt="""You are a supervisor for TechHub customer support.

Your role is to understand customer questions and route them to the appropriate specialists:
- Use database_specialist for order status, product prices, and customer order history
- Use documentation_specialist for product specs, policies, and general information

You can use multiple tools if needed to fully answer the question.
Always provide helpful, complete responses to customers.""",
        checkpointer=MemorySaver(),
    )
