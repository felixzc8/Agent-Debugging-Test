from decimal import Decimal
from typing import List, Dict
from datetime import datetime, timedelta
from validator import validate_transaction
from calculator import calculate_total, calculate_average

class TransactionProcessor:
    def __init__(self):
        self.transactions = []
        self.daily_totals = {}
        self._stats_cache = {}

    def add_transaction(self, transaction: Dict) -> bool:
        if not validate_transaction(transaction):
            return False

        self.transactions.append(transaction)
        date = transaction['date']

        if date not in self.daily_totals:
            self.daily_totals[date] = Decimal('0')

        self.daily_totals[date] += transaction['amount']

        return True

    def get_daily_total(self, date: str) -> Decimal:
        return self.daily_totals.get(date, Decimal('0'))

    def get_all_transactions(self) -> List[Dict]:
        return self.transactions

    def get_transactions_by_date(self, date: str) -> List[Dict]:
        return [t for t in self.transactions if t['date'] == date]

    def get_date_range_transactions(self, start_date: str, days: int) -> List[Dict]:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = start + timedelta(days=days)

        result = []
        for t in self.transactions:
            t_date = datetime.strptime(t['date'], '%Y-%m-%d')
            if start <= t_date <= end:
                result.append(t)
        return result

    def get_median_amount(self, date: str) -> Decimal:
        amounts = [t['amount'] for t in self.transactions if t['date'] == date]
        if not amounts:
            return Decimal('0')
        sorted_amounts = sorted(amounts)
        return sorted_amounts[len(sorted_amounts) // 2]

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

        return {
            'successful': successful,
            'failed': failed,
            'total_processed': successful + failed
        }

    def calculate_statistics(self, date: str) -> Dict:
        if date in self._stats_cache:
            return self._stats_cache[date]

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

        stats = {
            'count': len(transactions),
            'total': total,
            'average': average
        }

        self._stats_cache[date] = stats
        return stats
