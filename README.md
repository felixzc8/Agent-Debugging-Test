# Debugging Challenge (v3.0 - AI-Hard Edition)

Tests an AI agent's ability to identify and fix 5 genuinely challenging bugs without guidance or hints.

## Files
- `PROMPT.txt` - Initial instructions
- `CHALLENGE.md` - Detailed requirements
- `processor.py`, `validator.py`, `calculator.py` - Buggy source files
- `grade.py` - Grading script (agent must NOT read)
- `SOLUTIONS.md` - Bug explanations (agent must NOT read)
- `INSTRUCTIONS_FOR_HUMAN.md` - How to run this test

## Running

Provide agent: `Read PROMPT.txt and follow the instructions to complete the debugging challenge.`

Grade after completion: `python grade.py`

## The Challenge

The agent knows:
- ✅ There are 5 bugs total
- ❌ NOT which files contain bugs
- ❌ NOT what types of bugs exist
- ❌ NOT where bugs are located

No hints. No categories. No guided search.

## 5 AI-Hard Bugs (Hidden from Agent)

1. **Mutation side effect (9/10)** - Validator converts type BEFORE checking validity, mutating input on failure
2. **Stale cache (9/10)** - Statistics cache never invalidated when new data added (stateful bug)
3. **Median edge case (8/10)** - Doesn't average two middle elements for even-length lists
4. **Date boundary (8/10)** - Uses `<=` on wrong boundary, returns N+1 days instead of N
5. **Non-atomic batch (9/10)** - Batch processing leaves partial state on failure (transactional bug)

## Why These Are AI-Hard

**Cannot be found by pattern matching:**
- No `def func(arg=[])` mutable defaults
- No class-level list assignments
- No unused method call return values
- No obvious syntax errors

**Require genuine reasoning:**
- Must trace execution order (mutation timing)
- Must understand state across operations (cache invalidation)
- Must reason about algorithm edge cases (even-length median)
- Must understand semantic meaning (inclusive vs exclusive boundaries)
- Must recognize implicit requirements (transactional atomicity)

## Difficulty Assessment

**With hints (v3.0 beta):** 4-5/10 - Guided treasure hunt
**Without hints (v3.0 final):** 8-9/10 - True discovery required

The agent must:
1. Read all code without knowing where bugs are
2. Analyze each function for potential issues
3. Reason about correctness, edge cases, and implicit contracts
4. Identify exactly 5 bugs (not over-fix or under-fix)

## Success

5/5 tests pass without agent reading test code.

**Baseline score**: 0/5
