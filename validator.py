from decimal import Decimal
from typing import Dict, Any

def validate_transaction(transaction: Dict[str, Any]) -> bool:
    if not isinstance(transaction, dict):
        return False

    required_fields = ['date', 'amount', 'description']
    for field in required_fields:
        if field not in transaction:
            return False

    if not isinstance(transaction['date'], str):
        return False

    if not transaction['date']:
        return False

    if not isinstance(transaction['amount'], (int, float, Decimal)):
        return False

    transaction['amount'] = Decimal(str(transaction['amount']))

    if transaction['amount'] <= 0:
        return False

    if not isinstance(transaction['description'], str):
        return False

    return True
