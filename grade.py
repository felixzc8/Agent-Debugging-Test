#!/usr/bin/env python3
from decimal import Decimal
from datetime import datetime, timedelta
import sys
from processor import TransactionProcessor

class TestResult:
    def __init__(self, name: str, passed: bool, message: str = ""):
        self.name = name
        self.passed = passed
        self.message = message

def test_validation_mutation_side_effect():
    """Test BUG 1: Validator mutates input even when validation fails"""
    processor = TransactionProcessor()

    invalid_transaction = {
        'date': '2024-01-01',
        'amount': -100,
        'description': 'Negative amount'
    }

    original_type = type(invalid_transaction['amount'])
    result = processor.add_transaction(invalid_transaction)
    new_type = type(invalid_transaction['amount'])

    if result == False and original_type is new_type:
        return TestResult("Validation mutation side effect", True)
    else:
        return TestResult("Validation mutation side effect", False,
                         f"Validation failed correctly but mutated amount type from {original_type.__name__} to {new_type.__name__}")

def test_stale_statistics_cache():
    """Test BUG 2: Statistics cache not invalidated when new transactions added"""
    processor = TransactionProcessor()

    processor.add_transaction({
        'date': '2024-01-01',
        'amount': Decimal('100'),
        'description': 'First'
    })

    stats1 = processor.calculate_statistics('2024-01-01')

    processor.add_transaction({
        'date': '2024-01-01',
        'amount': Decimal('200'),
        'description': 'Second'
    })

    stats2 = processor.calculate_statistics('2024-01-01')

    if stats2['count'] == 2 and stats2['total'] == Decimal('300'):
        return TestResult("Stale statistics cache", True)
    else:
        return TestResult("Stale statistics cache", False,
                         f"After adding 2nd transaction, expected count=2 total=300, got count={stats2['count']} total={stats2['total']}")

def test_median_even_length():
    """Test BUG 3: Median calculation for even-length lists should average middle two"""
    processor = TransactionProcessor()

    amounts = [Decimal('10'), Decimal('20'), Decimal('30'), Decimal('40')]
    for amt in amounts:
        processor.add_transaction({
            'date': '2024-01-01',
            'amount': amt,
            'description': 'Test'
        })

    median = processor.get_median_amount('2024-01-01')
    expected = Decimal('25')

    if median == expected:
        return TestResult("Median calculation (even-length)", True)
    else:
        return TestResult("Median calculation (even-length)", False,
                         f"For [10,20,30,40], median should be 25 (avg of 20,30), got {median}")

def test_date_range_boundary():
    """Test BUG 4: Date range uses wrong boundary comparison"""
    processor = TransactionProcessor()

    for i in range(8):
        date = (datetime(2024, 1, 1) + timedelta(days=i)).strftime('%Y-%m-%d')
        processor.add_transaction({
            'date': date,
            'amount': Decimal('100'),
            'description': f'Day {i}'
        })

    transactions = processor.get_date_range_transactions('2024-01-01', days=7)

    if len(transactions) == 7:
        return TestResult("Date range boundary", True)
    else:
        return TestResult("Date range boundary", False,
                         f"Expected 7 transactions for 7-day range, got {len(transactions)}")

def test_batch_atomicity():
    """Test BUG 5: Batch processing is not atomic (partial state on failure)"""
    processor = TransactionProcessor()

    transactions = [
        {'date': '2024-01-01', 'amount': Decimal('100'), 'description': 'Valid 1'},
        {'date': '2024-01-02', 'amount': Decimal('200'), 'description': 'Valid 2'},
        {'date': '2024-01-03', 'amount': -50, 'description': 'Invalid'},
        {'date': '2024-01-04', 'amount': Decimal('300'), 'description': 'Valid 3'},
    ]

    initial_count = len(processor.get_all_transactions())
    result = processor.process_batch(transactions)
    final_count = len(processor.get_all_transactions())

    if result['failed'] > 0 and final_count == initial_count:
        return TestResult("Batch processing atomicity", True)
    else:
        return TestResult("Batch processing atomicity", False,
                         f"Batch with failure should rollback or not commit any. Started with {initial_count}, ended with {final_count}")

def main():
    print("=" * 60)
    print("DEBUGGING CHALLENGE - GRADING SYSTEM (v3.0)")
    print("AI-Hard Bugs Edition")
    print("=" * 60)
    print()

    tests = [
        test_validation_mutation_side_effect,
        test_stale_statistics_cache,
        test_median_even_length,
        test_date_range_boundary,
        test_batch_atomicity,
    ]

    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            results.append(TestResult(test_func.__name__, False, f"Exception: {str(e)}"))

    print("Test Results:")
    print("-" * 60)

    for i, result in enumerate(results, 1):
        status = "✓ PASS" if result.passed else "✗ FAIL"
        print(f"{i}. {result.name:45s} {status}")
        if not result.passed and result.message:
            print(f"   → {result.message}")

    passed = sum(1 for r in results if r.passed)
    total = len(results)

    print("-" * 60)
    print(f"\nScore: {passed}/{total} bugs fixed")
    print()

    if passed == total:
        print("🎉 CONGRATULATIONS! All bugs fixed!")
        print()
        return 0
    else:
        print(f"❌ {total - passed} bug(s) remaining. Keep debugging!")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
