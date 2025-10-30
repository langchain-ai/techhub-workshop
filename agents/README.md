# Agent Architecture

This document explains the design patterns and structure of agent implementations in this workshop.

## Design Philosophy

The agent architecture follows these principles:

1. **Progressive Disclosure**: Simple by default, customizable when needed
2. **Clear Separation**: Configuration vs. behavior vs. domain knowledge
3. **Easy Customization**: One place to change workshop-wide settings
4. **Pedagogical Value**: Structure teaches best practices

## File Structure

```
agents/
├── db_agent.py            # Database agent implementation
├── docs_agent.py          # Documents agent implementation
├── supervisor_agent.py    # Supervisor agent implementation
└── README.md              # This file
```

**Note:** Workshop-wide configuration (`DEFAULT_MODEL`, etc.) is in the root-level `config.py` file.

## Architecture Pattern

Each agent file follows this structure:

```python
# 1. IMPORTS
from config import DEFAULT_MODEL
from tools import tool1, tool2

# 2. MODULE-LEVEL CONFIGURATION (easy to find and edit)
AGENT_SYSTEM_PROMPT = """..."""
AGENT_BASE_TOOLS = [tool1, tool2]

# 3. FACTORY FUNCTION (encodes domain knowledge)
def create_agent(
    # Required parameters (no defaults)
    state_schema=None,
    # Optional extensions
    additional_tools=None,
    # Infrastructure
    use_checkpointer=True,
    # Override-able defaults
    model=None,
    system_prompt=None,
):
    """Factory that encodes what makes this agent type."""
    # Use defaults unless overridden
    llm = init_chat_model(model or DEFAULT_MODEL)
    prompt = system_prompt or AGENT_SYSTEM_PROMPT
    tools = AGENT_BASE_TOOLS.copy()
    
    if additional_tools:
        tools.extend(additional_tools)
    
    # Build and return agent
    ...
```

## Why This Pattern?

### Module-Level Constants

**Before (buried in function):**
```python
def create_db_agent():
    system_prompt = """You are a specialist..."""  # Hard to find
    tools = [tool1, tool2]  # Hidden
    llm = init_chat_model("anthropic:claude-haiku-4-5")  # Hardcoded
```

**After (explicit at module level):**
```python
DB_AGENT_SYSTEM_PROMPT = """You are a specialist..."""
DB_AGENT_BASE_TOOLS = [tool1, tool2]

def create_db_agent(model=None, system_prompt=None):
    llm = init_chat_model(model or DEFAULT_MODEL)
    prompt = system_prompt or DB_AGENT_SYSTEM_PROMPT
```

**Benefits:**
- ✅ Configuration is easy to find at top of file
- ✅ Can be imported and reused: `from agents.db_agent import DB_AGENT_SYSTEM_PROMPT`
- ✅ Clear what defines this agent type
- ✅ Still overrideable for specific needs

### Shared Configuration (Root `config.py`)

**Purpose:** Workshop-wide settings in one place

```python
# .env file
WORKSHOP_MODEL="anthropic:claude-haiku-4-5"
WORKSHOP_TEMPERATURE="0.0"

# config.py (at root level)
DEFAULT_MODEL = os.getenv("WORKSHOP_MODEL", "anthropic:claude-haiku-4-5")
DEFAULT_TEMPERATURE = float(os.getenv("WORKSHOP_TEMPERATURE", "0.0"))
```

**Benefits:**
- ✅ Change model for entire workshop in `.env` file
- ✅ Single source of truth
- ✅ Easy for customers to customize
- ✅ Follows 12-factor app principles

### Factory Functions Still Valuable

**Question:** If everything is parameterized, why have a factory?

**Answer:** The factory encodes **domain knowledge**, not just configuration:

```python
# Without factory - Students write this every time:
llm = init_chat_model(os.getenv("WORKSHOP_MODEL", "anthropic:claude-haiku-4-5"))
tools = [get_order_details, get_product_price]
system_prompt = """You are a database specialist..."""
agent_kwargs = {"model": llm, "tools": tools, "system_prompt": system_prompt}
if use_checkpointer:
    agent_kwargs["checkpointer"] = MemorySaver()
agent = create_agent(**agent_kwargs)

# With factory - Students write this:
db_agent = create_db_agent()
```

**The factory provides:**
1. **Domain Knowledge**: "A DB agent needs these tools, this prompt"
2. **Sensible Defaults**: Works out of the box
3. **Complexity Management**: Handles checkpointer, tool extension, state schema
4. **Progressive Disclosure**: Simple usage, advanced customization available

## Usage Examples

### Basic Usage (95% of cases)

```python
from agents import create_db_agent

# Uses all defaults from config
db_agent = create_db_agent()
```

### Workshop Customization (change model for all agents)

```python
# In .env file
WORKSHOP_MODEL="openai:gpt-4o-mini"

# All agents automatically use the new model
db_agent = create_db_agent()  # Uses GPT-4o-mini
```

### Per-Agent Customization

```python
# Override specific settings for this instance
db_agent = create_db_agent(
    state_schema=CustomState,
    additional_tools=[get_customer_orders],
    model="anthropic:claude-sonnet-4",
    system_prompt="Custom prompt for testing"
)
```

### Accessing Configuration

```python
# Import and use constants directly
from agents.db_agent import DB_AGENT_SYSTEM_PROMPT, DB_AGENT_BASE_TOOLS
from config import DEFAULT_MODEL

print(f"Using model: {DEFAULT_MODEL}")
print(f"Base tools: {[t.name for t in DB_AGENT_BASE_TOOLS]}")
```

## Deployment Considerations

For deployment, agents disable checkpointers:

```python
# deployments/db_agent_graph.py
from agents import create_db_agent

graph = create_db_agent(use_checkpointer=False)
```

This keeps the factory simple while supporting both dev and prod contexts.

## Extension Pattern

To add a new agent:

1. **Create agent file** (`agents/new_agent.py`)
2. **Define constants** (prompt, tools)
3. **Implement factory** (using pattern above)
4. **Export in `__init__.py`**
5. **Create deployment wrapper** (`deployments/new_agent_graph.py`)

See `db_agent.py` as the reference implementation.

