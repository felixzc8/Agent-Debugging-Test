# Solutions - Debugging Challenge (v3.0 - AI-Hard Edition)

## Bug 1: Mutation Side Effect in Validation (Difficulty: 9/10)
**Location:** `validator.py:22-25`

**Problem:**
```python
def validate_transaction(transaction: Dict[str, Any]) -> bool:
    # ... checks ...

    # BUG: Converts to Decimal BEFORE checking if amount is positive
    transaction['amount'] = Decimal(str(transaction['amount']))

    if transaction['amount'] <= 0:
        return False  # Validation failed, but input dict is already mutated!
```

The validator converts `amount` to `Decimal` at line 22, then checks if it's positive at line 24. If the amount is negative, validation fails and returns `False`, **but the caller's dictionary has already been mutated** from `int`/`float` to `Decimal`.

**Why It's AI-Hard:**
- No syntactic pattern to match
- Code looks reasonable at first glance
- Requires understanding (1) mutation timing, (2) side effects, (3) principle that failed operations shouldn't modify state
- Must trace execution order across lines

**Fix:**
```python
def validate_transaction(transaction: Dict[str, Any]) -> bool:
    # ... other checks ...

    if not isinstance(transaction['amount'], (int, float, Decimal)):
        return False

    # Check positivity BEFORE converting
    if transaction['amount'] <= 0:
        return False

    # Only convert if all validations pass
    transaction['amount'] = Decimal(str(transaction['amount']))
    return True
```

---

## Bug 2: Stale Statistics Cache (Difficulty: 9/10)
**Location:** `processor.py:11, 75-99`

**Problem:**
```python
class TransactionProcessor:
    def __init__(self):
        self._stats_cache = {}  # Cache for statistics

    def add_transaction(self, transaction):
        # ... adds transaction ...
        # BUG: Doesn't invalidate cache when new data added!

    def calculate_statistics(self, date):
        if date in self._stats_cache:
            return self._stats_cache[date]  # Returns stale data!

        # Calculate and cache...
        self._stats_cache[date] = stats
        return stats
```

The statistics are cached, but when `add_transaction()` adds a new transaction for a date that's already been queried, the cache is never invalidated. Subsequent calls return stale data.

**Why It's AI-Hard:**
- Stateful bug - only appears after specific sequence: query→add→query
- No single-line fix
- Requires understanding (1) cache invalidation, (2) state management, (3) temporal dependencies
- Must test with specific operation sequence to discover

**Fix Option 1 - Invalidate cache:**
```python
def add_transaction(self, transaction):
    # ... validation and adding ...

    # Invalidate cache for this date
    date = transaction['date']
    if date in self._stats_cache:
        del self._stats_cache[date]
```

**Fix Option 2 - Remove caching:**
```python
def calculate_statistics(self, date):
    # Just calculate directly, don't cache
    transactions = self.get_transactions_by_date(date)
    # ... calculate and return ...
```

---

## Bug 3: Median Calculation for Even-Length Lists (Difficulty: 8/10)
**Location:** `processor.py:47-52`

**Problem:**
```python
def get_median_amount(self, date):
    amounts = [t['amount'] for t in self.transactions if t['date'] == date]
    if not amounts:
        return Decimal('0')
    sorted_amounts = sorted(amounts)
    # BUG: Just returns middle element, doesn't average for even-length
    return sorted_amounts[len(sorted_amounts) // 2]
```

For a list like `[10, 20, 30, 40]`:
- Sorted: `[10, 20, 30, 40]`
- Index `len // 2 = 2`
- Returns `30`
- **Should return `(20 + 30) / 2 = 25`**

**Why It's AI-Hard:**
- Edge case - only fails with even-length lists
- Code looks correct for odd-length lists
- Requires understanding (1) median algorithm, (2) even vs odd behavior
- Must reason about different input sizes

**Fix:**
```python
def get_median_amount(self, date):
    amounts = [t['amount'] for t in self.transactions if t['date'] == date]
    if not amounts:
        return Decimal('0')

    sorted_amounts = sorted(amounts)
    n = len(sorted_amounts)

    if n % 2 == 1:
        # Odd length: return middle element
        return sorted_amounts[n // 2]
    else:
        # Even length: average two middle elements
        mid1 = sorted_amounts[n // 2 - 1]
        mid2 = sorted_amounts[n // 2]
        return (mid1 + mid2) / Decimal('2')
```

---

## Bug 4: Date Range Boundary Error (Difficulty: 8/10)
**Location:** `processor.py:36-45`

**Problem:**
```python
def get_date_range_transactions(self, start_date, days):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = start + timedelta(days=days)  # end = start + 7 for days=7

    result = []
    for t in self.transactions:
        t_date = datetime.strptime(t['date'], '%Y-%m-%d')
        # BUG: Uses <= on end, should be <
        if start <= t_date <= end:  # Includes one extra day!
            result.append(t)
    return result
```

For `start='2024-01-01'` and `days=7`:
- `end = 2024-01-01 + 7 days = 2024-01-08`
- Range: `2024-01-01 <= date <= 2024-01-08`
- **Includes 8 days (Jan 1-8), not 7!**

**Why It's AI-Hard:**
- Both `<=` and `<` are syntactically valid
- Requires understanding (1) half-open intervals, (2) timedelta semantics, (3) inclusive vs exclusive
- Must reason about relationship between `days` parameter and comparison operator

**Fix:**
```python
def get_date_range_transactions(self, start_date, days):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = start + timedelta(days=days)

    result = []
    for t in self.transactions:
        t_date = datetime.strptime(t['date'], '%Y-%m-%d')
        # Use < for exclusive end (half-open interval [start, end))
        if start <= t_date < end:
            result.append(t)
    return result
```

---

## Bug 5: Non-Atomic Batch Processing (Difficulty: 9/10)
**Location:** `processor.py:54-73`

**Problem:**
```python
def process_batch(self, transactions):
    successful = 0
    failed = 0

    for transaction in transactions:
        if self.add_transaction(transaction):
            successful += 1
        else:
            failed += 1
            # BUG: Returns immediately on failure
            return {
                'successful': successful,
                'failed': failed,
                'total_processed': successful + failed
            }

    return {...}
```

When processing a batch `[valid1, valid2, invalid, valid3]`:
1. Adds `valid1` ✓ (state modified)
2. Adds `valid2` ✓ (state modified)
3. Fails on `invalid` ✗ (returns immediately)
4. **Never tries `valid3`**
5. **Leaves `valid1` and `valid2` in the system (partial state)**

This violates transactional "all or nothing" semantics.

**Why It's AI-Hard:**
- Requires understanding (1) atomicity, (2) transactional integrity, (3) rollback semantics
- No syntactic error
- Implicit requirement (transactions should be atomic)
- Must reason about partial state and failure recovery

**Fix Option 1 - Validate all first:**
```python
def process_batch(self, transactions):
    # Validate all before adding any
    for transaction in transactions:
        if not validate_transaction(transaction):
            return {'successful': 0, 'failed': len(transactions), 'total_processed': len(transactions)}

    # All valid, add them all
    successful = 0
    for transaction in transactions:
        if self.add_transaction(transaction):
            successful += 1

    return {'successful': successful, 'failed': 0, 'total_processed': successful}
```

**Fix Option 2 - Rollback on failure:**
```python
def process_batch(self, transactions):
    snapshot = self.transactions.copy()  # Save state

    successful = 0
    failed = 0

    for transaction in transactions:
        if self.add_transaction(transaction):
            successful += 1
        else:
            failed += 1
            # Rollback on failure
            self.transactions = snapshot
            return {'successful': 0, 'failed': len(transactions), 'total_processed': len(transactions)}

    return {'successful': successful, 'failed': 0, 'total_processed': successful}
```

---

## Summary: Why These Bugs Are AI-Hard

| Bug | Pattern Matching? | Requires Understanding Of |
|-----|------------------|---------------------------|
| 1. Mutation side effect | ❌ No pattern | Execution order, side effects, validation semantics |
| 2. Stale cache | ❌ No pattern | State management, temporal dependencies, cache invalidation |
| 3. Median even-length | ❌ No pattern | Algorithm edge cases, median definition, even vs odd |
| 4. Date boundary | ❌ No pattern | Inclusive/exclusive ranges, timedelta semantics |
| 5. Non-atomic batch | ❌ No pattern | Transactional integrity, atomicity, rollback |

**Key Insight:** These bugs cannot be found by searching for syntactic patterns like:
- `def func(arg=[])`
- `class Foo:\n    var = []`
- `str.method()` without assignment

They require genuine understanding of:
- When state changes
- How operations interact
- What implicit contracts exist
- How algorithms should behave

**Average AI Difficulty: 8.6/10**
