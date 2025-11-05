"""
Workshop-wide configuration for the AI Engineering Lifecycle workshop.

All default settings can be customized via environment variables in .env file.
This makes it easy to adapt the workshop for different:
- Model providers (OpenAI, Anthropic, Azure, etc.)
- Model versions (GPT-4, Claude Sonnet, etc.)
- Performance profiles (fast models vs. high-quality models)
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from langchain_community.utilities import SQLDatabase
from langchain_core.vectorstores import VectorStoreRetriever

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

# Primary model used by all agents throughout the workshop
# Set WORKSHOP_MODEL in .env to change the model for all sections
# Examples:
#   - "anthropic:claude-haiku-4-5" (fast, cost-effective)
#   - "anthropic:claude-sonnet-4" (balanced)
#   - "openai:gpt-4o-mini" (fast, OpenAI)
#   - "openai:gpt-4o" (high-quality, OpenAI)
DEFAULT_MODEL = os.getenv("WORKSHOP_MODEL", "anthropic:claude-haiku-4-5")

# ============================================================================
# DATA PATHS CONFIGURATION
# ============================================================================

DEFAULT_DB_PATH = Path(__file__).parent / "data" / "structured" / "techhub.db"
DEFAULT_VECTORSTORE_PATH = (
    Path(__file__).parent / "data" / "vector_stores" / "techhub_vectorstore.pkl"
)

# ============================================================================
# RUNTIME CONTEXT CONFIGURATION
# ============================================================================


@dataclass
class RuntimeContext:
    """Runtime context for tools and agents containing database connection and vector store retrievers."""

    db: SQLDatabase
    product_retriever: Optional[VectorStoreRetriever] = None
    policy_retriever: Optional[VectorStoreRetriever] = None


def get_techhub_runtime_context(with_vectorstore: bool = False) -> RuntimeContext:
    """Get runtime context for TechHub agents.

    This factory function creates a RuntimeContext with the appropriate resources
    based on what tools your agent needs.

    Args:
        with_vectorstore: If True, includes retrievers for RAG tools (search_product_docs, search_policy_docs).
                         If False, only includes database connection for DB tools.

    Returns:
        RuntimeContext configured with requested resources.

    Examples:
        >>> # For agents with only database tools
        >>> context = get_techhub_runtime_context()

        >>> # For agents with database + RAG tools
        >>> context = get_techhub_runtime_context(with_vectorstore=True)
    """
    db = SQLDatabase.from_uri(f"sqlite:///{DEFAULT_DB_PATH}")

    if with_vectorstore:
        # Import here to avoid circular dependency and enable lazy loading
        from tools.documents import _get_policy_retriever, _get_product_retriever

        return RuntimeContext(
            db=db,
            product_retriever=_get_product_retriever(),
            policy_retriever=_get_policy_retriever(),
        )

    return RuntimeContext(db=db)


# ============================================================================
# FUTURE CONFIGURATION
# ============================================================================
# As the workshop grows, additional settings can be added here:
#
# Embedding model for RAG:
# DEFAULT_EMBEDDING_MODEL = os.getenv(
#     "EMBEDDING_MODEL",
#     "sentence-transformers/all-MiniLM-L6-v2"
# )
#
# Data paths:
# DATABASE_PATH = os.getenv(
#     "DATABASE_PATH",
#     "./data/structured/techhub.db"
# )
#
# VECTOR_STORE_PATH = os.getenv(
#     "VECTOR_STORE_PATH",
#     "./data/vector_stores/techhub_vectorstore.pkl"
# )
