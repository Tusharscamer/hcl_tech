from typing import List, Dict, Any
from collections import defaultdict

def aggregate_expenses_by_category(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyzes debit transactions, categorizes them (Food, Transport, Shopping, Bills, etc.),
    calculates proportions and top spending categories.
    """
    category_totals = defaultdict(float)
    category_counts = defaultdict(int)
    merchant_totals = defaultdict(float)
    total_spent = 0.0

    for txn in transactions:
        if txn.get("type") == "DEBIT" and txn.get("status") in ("COMPLETED", "FLAGGED"):
            amt = float(txn.get("amount", 0.0))
            cat = txn.get("category", "General")
            merch = txn.get("merchant", "Unknown")

            category_totals[cat] += amt
            category_counts[cat] += 1
            merchant_totals[merch] += amt
            total_spent += amt

    breakdown = []
    for cat, total in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
        pct = (total / total_spent * 100.0) if total_spent > 0 else 0.0
        breakdown.append({
            "category": cat,
            "amount": round(total, 2),
            "percentage": round(pct, 1),
            "count": category_counts[cat]
        })

    top_merchants = [
        {"merchant": merch, "amount": round(total, 2)}
        for merch, total in sorted(merchant_totals.items(), key=lambda x: x[1], reverse=True)[:5]
    ]

    # Generate insights
    insights = []
    if breakdown:
        top_cat = breakdown[0]
        insights.append(f"Highest spending was in {top_cat['category']} (₹{top_cat['amount']:,.2f}, {top_cat['percentage']}% of total).")
    if total_spent > 25000:
        insights.append("Spending is higher than typical monthly threshold. Review discretionary shopping.")
    else:
        insights.append("Spending is within healthy monthly budget guidelines.")

    return {
        "total_spent": round(total_spent, 2),
        "period": "current_month",
        "category_breakdown": breakdown,
        "top_merchants": top_merchants,
        "insights": insights
    }
