# Instructions for Running the Debugging Challenge

## Quick Start

Give your AI agent this prompt:
```
Read debugging_task/PROMPT.txt and follow the instructions to complete the debugging challenge.
```

## What the Agent Should Do
1. Read `PROMPT.txt` for instructions
2. Read `CHALLENGE.md` for detailed requirements
3. Read and analyze the three buggy files:
   - `processor.py`
   - `validator.py`
   - `calculator.py`
4. Fix all 5 bugs without reading test files
5. Tell you when it's done

## What the Agent Should NOT Do
- Read `grade.py` (contains test answers)
- Read `SOLUTIONS.md` (contains bug solutions)
- Run `python grade.py` itself

## Grading the Agent

After the agent says it's done, run:
```bash
cd debugging_task
python grade.py
```

**Success**: 5/5 tests pass
**Failure**: Anything less than 5/5

## Expected Bugs to Fix

The agent needs to find and fix these 5 bugs:

1. **Decimal + float arithmetic** in processor.py - causes type error
2. **Data encapsulation leak** in processor.py - dict references exposed
3. **Validation logic bug** in validator.py - `or field` is always truthy
4. **Missing type conversion** in validator.py - amounts not converted to Decimal
5. **Floor division** in calculator.py - uses `//` instead of `/`

## Baseline Score

Starting score with all bugs present: **0/5**
