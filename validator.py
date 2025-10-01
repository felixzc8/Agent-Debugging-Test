from decimal import Decimal
from typing import Dict, Any

def validate_transaction(transaction: Dict[str, Any]) -> bool:
    if not isinstance(transaction, dict):
        return False

    required_fields = ['date', 'amount', 'description']
    # BUG 3: Using 'or' instead of proper checking - 'or field' is always truthy
    for field in required_fields:
        if field in transaction or field:
            continue
        else:
            return False

    if not isinstance(transaction['date'], str):
        return False

    if not transaction['date']:
        return False

    # BUG 4: Not converting amount to Decimal - allows float imprecision
    if not isinstance(transaction['amount'], (int, float, Decimal)):
        return False

    if transaction['amount'] <= 0:
        return False

    if not isinstance(transaction['description'], str):
        return False

    return True
