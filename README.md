# Debugging Challenge

Tests an AI agent's ability to identify and fix 5 subtle bugs in a Python codebase without seeing test cases.

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

## Bugs
1. Type mixing in arithmetic (Decimal + float)
2. Data encapsulation violation
3. Validation logic error (`or field` issue)
4. Missing type conversion (float to Decimal)
5. Floor division truncation (`//` vs `/`)

## Success
5/5 tests pass without agent reading test code.
