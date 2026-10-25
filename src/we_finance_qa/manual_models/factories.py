from we_finance_qa.manual_models.models import MODEL_LOAN

DEFAULT = {
    "day_count": "actual",
    "first_payment_date": "2026-02-15",
    "issue_date": "2026-01-15",
    "monthly_fee": "0.00",
    "months": 36,
    "name": "Учебный кредит",
    "payment": "39857.17",
    "payment_day_changes": [],
    "principal": "1200000.00",
    "rates": [{"annual_rate": "12", "start": "2026-01-15"}],
    "weekend_shift": False,
}


def make_loan(**overrides) -> MODEL_LOAN:
    return MODEL_LOAN(**{**DEFAULT, **overrides})
