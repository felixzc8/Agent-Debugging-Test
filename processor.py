from decimal import Decimal
from typing import List, Dict
from validator import validate_transaction
from calculator import calculate_total, calculate_average

class TransactionProcessor:
    def __init__(self):
        self.transactions = []
        self.daily_totals = {}

    def add_transaction(self, transaction: Dict) -> bool:
        if not validate_transaction(transaction):
            return False

        self.transactions.append(transaction)
        date = transaction['date']

        if date not in self.daily_totals:
            self.daily_totals[date] = Decimal('0')

        # BUG 1: Mixed type arithmetic - transaction['amount'] might not be Decimal
        self.daily_totals[date] = self.daily_totals[date] + transaction['amount']

        return True

    def get_daily_total(self, date: str) -> Decimal:
        return self.daily_totals.get(date, Decimal('0'))

    def get_transactions_by_date(self, date: str) -> List[Dict]:
        # BUG 2: Returns list of dict references, allowing external modification
        return [t for t in self.transactions if t['date'] == date]

    def process_batch(self, transactions: List[Dict]) -> Dict:
        successful = 0
        failed = 0

        for transaction in transactions:
            if self.add_transaction(transaction):
                successful += 1
            else:
                failed += 1

        return {
            'successful': successful,
            'failed': failed,
            'total_processed': successful + failed
        }

    def calculate_statistics(self, date: str) -> Dict:
        transactions = self.get_transactions_by_date(date)

        if not transactions:
            return {
                'count': 0,
                'total': Decimal('0'),
                'average': Decimal('0')
            }

        amounts = [t['amount'] for t in transactions]
        total = calculate_total(amounts)
        average = calculate_average(amounts)

        return {
            'count': len(transactions),
            'total': total,
            'average': average
        }
