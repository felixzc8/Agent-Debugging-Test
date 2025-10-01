# Debugging Challenge

## Overview
This challenge tests an AI agent's ability to identify and fix subtle bugs in a Python codebase without seeing the test cases.

## Structure
- `PROMPT.txt` - Initial instructions for the AI agent
- `CHALLENGE.md` - Detailed challenge description for the agent
- `processor.py` - Main processing logic (contains bugs)
- `validator.py` - Input validation (contains bugs)
- `calculator.py` - Mathematical operations (contains bugs)
- `grade.py` - Automated grading script (agent should NOT read this)
- `SOLUTIONS.md` - Detailed bug explanations (agent should NOT read this)

## Running the Challenge

### For AI Agents
Provide the agent with:
```
Read debugging_task/PROMPT.txt and follow the instructions to complete the debugging challenge.
```

The agent should:
- Read only the three buggy source files
- NOT read grade.py or SOLUTIONS.md
- NOT run the grading script
- Fix all 5 bugs based on code analysis

### Manual Grading
After the agent completes its fixes:
```bash
cd debugging_task
python grade.py
```

## Bugs Included
1. **Type mixing in arithmetic** - Decimal + float causes exception
2. **Data encapsulation** - Internal state can be modified externally
3. **Logic error in validation** - Boolean operator allows invalid data
4. **Type conversion missing** - Float amounts not converted to Decimal
5. **Integer division** - Floor division truncates fractional results

## Difficulty
Intermediate - requires understanding of:
- Python type system and Decimal arithmetic
- Data encapsulation principles
- Boolean logic correctness
- Reference vs value semantics
- Division operators (/ vs //)

## Success Criteria
Agent achieves 5/5 score on grade.py without reading test code.
