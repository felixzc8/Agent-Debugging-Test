# Instructions for Running the Debugging Challenge (v3.0 - AI-Hard Edition)

## Quick Start

Give your AI agent this prompt:
```
Read PROMPT.txt and follow the instructions to complete the debugging challenge.
```

## Grading

After the agent completes, run:
```bash
python grade.py
```

**Success**: 5/5 tests pass

## What the Agent Knows

The agent is told:
- There are 5 bugs in the codebase
- They should fix bugs in processor.py, validator.py, calculator.py
- They should NOT read grade.py or SOLUTIONS.md

The agent is NOT told:
- Which files contain bugs
- What types of bugs exist
- Where bugs are located
- Any hints or categories

## Expected Bugs (AI Difficulty: 8-9/10 average)

These bugs require genuine discovery and reasoning:

1. **Mutation side effect** (validator.py) - Converts type before validating, mutating input on failure
2. **Stale cache** (processor.py) - Statistics cache never invalidated when new transactions added
3. **Median edge case** (processor.py) - Doesn't average two middle elements for even-length lists
4. **Date boundary** (processor.py) - Uses `<=` instead of `<`, returns N+1 days instead of N
5. **Non-atomic batch** (processor.py) - Leaves partial state when batch processing fails

**Baseline score**: 0/5

## Why This Tests Real Debugging Ability

### Traditional Bug Challenges (Easy for AI)
```python
# Obvious antipatterns that AI can pattern-match:

def func(items=[]):              # ← Mutable default
    items.append(x)

class Foo:
    shared_list = []             # ← Class variable

s.strip()                        # ← Unused return value
transaction['description'] = s
```

### This Challenge (Hard for AI)
```python
# No patterns to match - requires understanding:

# Bug 1: Execution order
transaction['amount'] = Decimal(str(transaction['amount']))  # Line 22
if transaction['amount'] <= 0:                                # Line 24
    return False  # ← Mutation happened before validation!

# Bug 2: State management across time
def calculate_statistics(date):
    if date in self._stats_cache:
        return self._stats_cache[date]  # ← Stale after add_transaction()

# Bug 3: Algorithm edge cases
sorted_amounts = sorted(amounts)
return sorted_amounts[len(amounts) // 2]  # ← Wrong for even-length!

# Bug 4: Semantic boundaries
end = start + timedelta(days=7)
if start <= t_date <= end:  # ← Includes 8 days, not 7!

# Bug 5: Implicit transactional requirements
for transaction in batch:
    self.add_transaction(transaction)  # Modifies state
    if failed:
        return  # ← Left partial state!
```

## What This Measures

✅ **Genuine AI capabilities:**
- Code comprehension without guidance
- Bug discovery (not just verification)
- Execution flow analysis
- Edge case reasoning
- Understanding implicit contracts
- State management reasoning
- Algorithmic correctness analysis

❌ **Not just:**
- Pattern recognition
- Memorized antipatterns
- Guided treasure hunting

## Comparison: Hints vs No Hints

| Aspect | With Category Hints | Without Hints (Current) |
|--------|-------------------|------------------------|
| Agent knows bug types | Yes | No |
| Agent knows locations | Yes (per file) | No |
| Difficulty | 4-5/10 | 8-9/10 |
| Test type | Verification | Discovery |
| Search space | Focused | Entire codebase |
| Reasoning required | Moderate | High |

## Expected Agent Behavior

**With hints (old):**
1. Read "mutation timing bug in validator.py"
2. Search validator.py for type conversion
3. Find and verify the issue
4. Fix in 1-2 minutes

**Without hints (current):**
1. Read all 3 files (~100 lines)
2. Analyze each function independently
3. Reason about correctness, edge cases, state
4. Identify issues through understanding, not guidance
5. Fix over 10-30 minutes

## Difficulty Breakdown

| Bug | Type | Without Hints | Why Hard |
|-----|------|---------------|----------|
| 1. Mutation side effect | Execution order | **9/10** | Must trace order, understand side effects |
| 2. Stale cache | Stateful | **9/10** | Must simulate operation sequences |
| 3. Median edge case | Algorithm | **8/10** | Must reason about even vs odd |
| 4. Date boundary | Semantic | **8/10** | Must understand inclusive/exclusive |
| 5. Non-atomic batch | Implicit requirement | **9/10** | Must recognize atomicity violation |

**Average: 8.6/10 for AI agents**

## Notes

- The bugs are syntactically correct Python
- All type hints are accurate
- No linter warnings
- No obvious code smells
- Requires deep understanding to discover issues
- Tests true debugging ability, not pattern matching
