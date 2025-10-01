from decimal import Decimal
from typing import List, Union

def calculate_total(amounts: List[Union[Decimal, int, float]]) -> Decimal:
    total = Decimal('0')
    for amount in amounts:
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        total += amount
    return total

def calculate_average(amounts: List[Union[Decimal, int, float]]) -> Decimal:
    if not amounts:
        return Decimal('0')

    total = calculate_total(amounts)
    # BUG 5: Integer division loses precision - should use Decimal division
    return total // len(amounts)
