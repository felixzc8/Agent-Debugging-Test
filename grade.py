#!/usr/bin/env python3
from decimal import Decimal
import sys
from processor import TransactionProcessor

class TestResult:
    def __init__(self, name: str, passed: bool, message: str = ""):
        self.name = name
        self.passed = passed
        self.message = message

def test_decimal_precision():
    """Test BUG 1: Decimal arithmetic precision"""
    processor = TransactionProcessor()

    transactions = [
        {'date': '2024-01-01', 'amount': 0.1, 'description': 'Test 1'},
        {'date': '2024-01-01', 'amount': 0.2, 'description': 'Test 2'},
    ]

    for t in transactions:
        processor.add_transaction(t)

    total = processor.get_daily_total('2024-01-01')
    expected = Decimal('0.3')

    if total == expected and isinstance(total, Decimal):
        return TestResult("Decimal precision", True)
    else:
        return TestResult("Decimal precision", False,
                         f"Expected {expected}, got {total} (type: {type(total)})")

def test_data_encapsulation():
    """Test BUG 2: Internal data structure protection"""
    processor = TransactionProcessor()

    processor.add_transaction({
        'date': '2024-01-01',
        'amount': Decimal('100'),
        'description': 'Original'
    })

    transactions = processor.get_transactions_by_date('2024-01-01')
    original_description = processor.transactions[0]['description']

    # Modify returned transaction dict
    transactions[0]['description'] = 'HACKED'

    # Check if internal state was affected
    if processor.transactions[0]['description'] == original_description:
        return TestResult("Data encapsulation", True)
    else:
        return TestResult("Data encapsulation", False,
                         "External code can modify internal transaction data")

def test_validation_logic():
    """Test BUG 3: Validation logic error"""
    processor = TransactionProcessor()

    invalid_transaction = {
        'date': '2024-01-01',
        'amount': Decimal('100'),
    }

    try:
        result = processor.add_transaction(invalid_transaction)
        if result == False:
            return TestResult("Validation logic", True)
        else:
            return TestResult("Validation logic", False,
                             "Should reject transaction missing 'description' field")
    except KeyError:
        return TestResult("Validation logic", False,
                         "Validation should check all fields exist before accessing them")

def test_amount_conversion():
    """Test BUG 4: Amount should be converted to Decimal"""
    processor = TransactionProcessor()

    result = processor.add_transaction({
        'date': '2024-01-01',
        'amount': 100.50,
        'description': 'Float amount'
    })

    if not result:
        return TestResult("Amount type handling", False,
                         "Should accept numeric amounts")

    transaction = processor.get_transactions_by_date('2024-01-01')[0]
    if isinstance(transaction['amount'], Decimal):
        return TestResult("Amount type handling", False,
                         "Validator should convert amount to Decimal")

    return TestResult("Amount type handling", True)

def test_average_precision():
    """Test BUG 5: Division precision in average calculation"""
    processor = TransactionProcessor()

    transactions = [
        {'date': '2024-01-01', 'amount': Decimal('10.50'), 'description': 'T1'},
        {'date': '2024-01-01', 'amount': Decimal('20.75'), 'description': 'T2'},
        {'date': '2024-01-01', 'amount': Decimal('30.25'), 'description': 'T3'},
    ]

    for t in transactions:
        processor.add_transaction(t)

    stats = processor.calculate_statistics('2024-01-01')

    if not isinstance(stats['average'], Decimal):
        return TestResult("Average calculation precision", False,
                         f"Average should be Decimal, got {type(stats['average'])}")

    expected = Decimal('20.50')
    if stats['average'] == expected:
        return TestResult("Average calculation precision", True)
    else:
        return TestResult("Average calculation precision", False,
                         f"Expected {expected}, got {stats['average']}")

def main():
    print("=" * 60)
    print("DEBUGGING CHALLENGE - GRADING SYSTEM")
    print("=" * 60)
    print()

    tests = [
        test_decimal_precision,
        test_data_encapsulation,
        test_validation_logic,
        test_amount_conversion,
        test_average_precision,
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

    passed = 0
    for i, result in enumerate(results, 1):
        status = "✓ PASS" if result.passed else "✗ FAIL"
        print(f"{i}. {result.name:40s} {status}")
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
