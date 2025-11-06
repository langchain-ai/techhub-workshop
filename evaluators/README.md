# Evaluators

This directory contains evaluators for measuring agent performance in the TechHub customer support workshop.

## Purpose

Evaluators are functions that score how well your application performs on a particular example. They're essential for:

1. **Establishing baselines**: Quantify current performance
2. **Measuring improvements**: Compare before/after metrics
3. **Identifying failure modes**: Understand where and why agents fail
4. **Tracking efficiency**: Monitor resource usage (tool calls, latency, cost)

## Philosophy

The workshop follows a pedagogical progression:

**Module 2, Section 1 (Baseline)**: Students build evaluators from scratch inline in the notebook
- Learn what makes a good evaluator
- Understand inputs, outputs, and reference outputs
- Write custom evaluation logic

**Module 2, Section 2+ (Improvements)**: Students import the evaluators they just built
- Evaluators are now packaged as reusable modules
- Focus shifts to eval-driven development workflow
- Same pattern as agents: build inline → refactor → reuse

## Available Evaluators

### 1. Correctness Evaluator (LLM-as-Judge)

Compares agent output against ground truth using an LLM judge.

```python
from evaluators import correctness_evaluator

# Requires: inputs, outputs, reference_outputs
result = correctness_evaluator(
    inputs={"messages": [{"role": "user", "content": "What's my order status?"}]},
    outputs={"messages": [{"role": "assistant", "content": "Your order shipped"}]},
    reference_outputs={"messages": [{"role": "assistant", "content": "Shipped"}]}
)

# Returns: {"key": "correctness", "score": True/False, "comment": "reasoning"}
```

**What it evaluates:**
- Factual accuracy
- Completeness (addresses all parts of question)
- Logical consistency
- Allows for style differences (focuses on correctness, not format)

**When to use:**
- Final answer evaluation
- Comparing against curated ground truth
- When you have reference outputs for each example

### 2. Tool Call Counter (Trace-Based)

Counts total tool invocations across entire execution trace.

```python
from evaluators import count_total_tool_calls_evaluator
from langsmith import Client

client = Client()

# Get full trace with child runs
run = client.read_run(run_id, load_child_runs=True)

# Evaluator counts all tool-type runs
result = count_total_tool_calls_evaluator(run)

# Returns: {"key": "total_tool_calls", "score": 7}
```

**What it evaluates:**
- Efficiency of execution
- Number of tool invocations (lower often means more efficient)
- Helps identify sequential chains (e.g., get_order_items → get_product_info × N)

**When to use:**
- Tracking efficiency improvements
- Identifying inefficient patterns
- Comparing baseline vs improved agents
- Doesn't require reference outputs

## Usage in Experiments

Both evaluators work seamlessly with LangSmith's `evaluate()` function:

```python
from langsmith import Client
from evaluators import correctness_evaluator, count_total_tool_calls_evaluator

client = Client()

results = client.evaluate(
    target_function,
    data="your-dataset-name",
    evaluators=[
        correctness_evaluator,
        count_total_tool_calls_evaluator
    ],
    experiment_prefix="my-experiment",
    max_concurrency=5
)
```

### How LangSmith Routes Evaluators

LangSmith automatically detects evaluator types by signature:

**Reference-based evaluators** (like `correctness_evaluator`):
```python
def evaluator(inputs: dict, outputs: dict, reference_outputs: dict) -> dict:
    # LangSmith passes example inputs, actual outputs, and reference outputs
```

**Trace-based evaluators** (like `count_total_tool_calls_evaluator`):
```python
def evaluator(run: Run) -> dict:
    # LangSmith passes the full Run object with execution metadata
```

You can mix both types in a single experiment!

## Evaluator Design Patterns

### 1. Binary Scores (Recommended for Beginners)

```python
return {"key": "correctness", "score": True}  # or False
```

**Benefits:**
- Clear, unambiguous
- Easy to aggregate (% correct)
- Forces clearer thinking about what "correct" means
- Faster to label and validate

### 2. Numeric Scores (Advanced)

```python
return {"key": "relevance", "score": 0.85}  # 0.0 to 1.0
```

**Use when:**
- You need gradations (partially correct, mostly correct)
- Averaging makes sense for your metric
- You have clear rubrics for each score level

### 3. Count Metrics (Efficiency)

```python
return {"key": "total_tool_calls", "score": 7}  # integer count
```

**Use for:**
- Resource usage (tools, tokens, time)
- Comparative analysis (fewer is better)
- Tracking efficiency improvements

## Best Practices

### Start Simple
- Begin with 1-2 evaluators (e.g., correctness + efficiency)
- Binary scores are easier than gradations
- Small dataset (10-20 examples) is fine to start

### Focus on What Matters
- Measure what you actually care about
- If you don't know what to do with a metric, don't track it
- Avoid metric overload (analysis paralysis)

### Iterate on Evaluators
- Your evaluators will evolve with your understanding
- First evaluator doesn't need to be perfect
- Refine prompts, rubrics, and logic based on results

### Comments and Reasoning
- Always return `comment` or `reasoning` field
- Helps debug false positives/negatives
- Essential for understanding evaluator behavior

### Determinism
- Use `temperature=0` for LLM judges
- Seed random operations
- Makes experiments reproducible

## Adding New Evaluators

To add a new evaluator:

1. **Define in `evaluators.py`** with clear docstring
2. **Choose signature** (reference-based vs trace-based)
3. **Add to `__init__.py`** exports
4. **Document here** with usage example

Example structure:

```python
# In evaluators.py

def my_custom_evaluator(inputs: dict, outputs: dict, reference_outputs: dict) -> dict:
    """Brief description of what this evaluates.
    
    Detailed explanation...
    
    Args:
        inputs: ...
        outputs: ...
        reference_outputs: ...
    
    Returns:
        Dictionary with key, score, comment
    """
    # Evaluation logic
    
    return {
        "key": "my_metric",
        "score": True,
        "comment": "Why this score"
    }
```

## Resources

- [LangSmith Evaluation Docs](https://docs.langchain.com/langsmith/evaluation)
- [LangSmith Evaluation Approaches](https://docs.langchain.com/langsmith/evaluation-approaches)
- Module 2, Section 1: Where these evaluators are first built
- Module 2, Section 2: Eval-driven development workflow

## Module Progression

The evaluators follow the same pattern as agents in the workshop:

**Module 1**: Agents built inline → refactored to `agents/` → reused
**Module 2**: Evaluators built inline → refactored to `evaluators/` → reused

This teaches best practices for organizing ML/AI code: prototype inline, refactor to modules, reuse across projects.

