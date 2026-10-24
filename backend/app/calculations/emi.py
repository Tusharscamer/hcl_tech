import math
from typing import Dict, Any, List

def calculate_emi(principal: float, annual_interest_rate: float, tenure_months: int) -> float:
    """
    Standard banking formula:
    EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
    where r = annual_interest_rate / 12 / 100
    """
    if principal <= 0 or tenure_months <= 0:
        return 0.0
    if annual_interest_rate == 0:
        return round(principal / tenure_months, 2)

    monthly_rate = annual_interest_rate / (12 * 100)
    pow_factor = math.pow(1 + monthly_rate, tenure_months)
    emi = principal * monthly_rate * (pow_factor / (pow_factor - 1))
    return round(emi, 2)

def generate_amortization_schedule(
    principal: float,
    annual_interest_rate: float,
    tenure_months: int,
    limit_months: int = 12
) -> List[Dict[str, Any]]:
    """
    Generates deterministic month-by-month principal and interest breakdown.
    """
    emi = calculate_emi(principal, annual_interest_rate, tenure_months)
    monthly_rate = annual_interest_rate / (12 * 100)
    balance = principal
    schedule = []

    for month in range(1, min(tenure_months + 1, limit_months + 1)):
        interest_payment = round(balance * monthly_rate, 2)
        principal_payment = round(emi - interest_payment, 2)
        balance = max(0.0, round(balance - principal_payment, 2))
        schedule.append({
            "month": month,
            "emi": emi,
            "principal": principal_payment,
            "interest": interest_payment,
            "remaining_balance": balance
        })
        if balance <= 0:
            break

    return schedule
