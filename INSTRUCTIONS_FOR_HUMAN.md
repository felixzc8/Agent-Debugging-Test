# Instructions for Running the Debugging Challenge

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

## Expected Bugs

1. **Decimal + float arithmetic** in processor.py
2. **Data encapsulation leak** in processor.py
3. **Validation logic bug** in validator.py - `or field` is always truthy
4. **Missing type conversion** in validator.py
5. **Floor division** in calculator.py - uses `//` instead of `/`

Baseline score: **0/5**
