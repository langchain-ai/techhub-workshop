# Deployment Configurations

This directory contains deployment-ready graph instances for LangSmith deployment.

## Purpose

The `deployments/` directory provides a clean separation between:
- **Development/Workshop**: Factory functions in `agents/` with flexible parameters
- **Deployment**: Fixed, module-level graph instances ready for `langgraph.json`

## Pattern

### Factory Function (agents/)
Used in notebooks and development for flexibility:

```python
from agents import create_db_agent
from tools import get_customer_orders

# Flexible - can customize state schema and tools
db_agent = create_db_agent(
    state_schema=CustomState,
    additional_tools=[get_customer_orders]
)
```

### Deployment Instance (deployments/)
Used for LangSmith deployment with fixed configuration:

```python
# deployments/db_agent_graph.py
from agents import create_db_agent

# Module-level instance for deployment
# use_checkpointer=False because platform provides managed persistence
graph = create_db_agent(use_checkpointer=False)
```

### Configuration (langgraph.json)
References the module-level graph instance:

```json
{
  "graphs": {
    "db_agent": "./deployments/db_agent_graph.py:graph"
  }
}
```

## Why This Approach?

1. **Pedagogical Clarity**: Workshop participants see both patterns
2. **Separation of Concerns**: Development flexibility vs. deployment stability
3. **Best Practice**: Follows [LangChain deployment guidelines](https://docs.langchain.com/langsmith/setup-pyproject)
4. **Module 3 Foundation**: This pattern becomes essential for deployment workflows

## Important: Checkpointer Behavior

**Development (notebooks):**
```python
db_agent = create_db_agent()  # use_checkpointer=True by default
```

**Deployment (LangGraph API):**
```python
graph = create_db_agent(use_checkpointer=False)  # Platform provides persistence
```

Why? LangGraph API [handles persistence automatically](https://docs.langchain.com/oss/python/langgraph/persistence) with managed Postgres. Set `use_checkpointer=False` to disable the local checkpointer for deployment.

## Current Deployments

- `db_agent_graph.py` - Database agent for querying orders and products
- `docs_agent_graph.py` - Documents agent for searching product docs and policies
- `supervisor_agent_graph.py` - Supervisor agent coordinating between specialists

## Adding New Deployments

1. Create a new file: `deployments/your_agent_graph.py`
2. Import and instantiate: `graph = create_your_agent()`
3. Add to `langgraph.json`: `"your_agent": "./deployments/your_agent_graph.py:graph"`
4. Export in `__init__.py`

