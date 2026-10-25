from datetime import date
from decimal import Decimal

import pytest
import requests

from we_finance_qa.manual_models import models
from we_finance_qa.manual_models.factories import make_loan

pytestmark = pytest.mark.api

API_MONEY = "/api/v1/money/round"
API_LOAN = "/api/v1/loans"


def test_money_round(base_url):
    response = requests.get(
        (base_url + API_MONEY),
        params={"amount": "422.276"},
        timeout=5,
    )
    total = response.json()
    assert response.status_code == 200
    assert total["amount"] == "422.28"


def test_create_loan(base_url):
    body = make_loan().model_dump(mode="json")
    response = requests.post((base_url + API_LOAN), json=body, timeout=5)
    assert response.status_code == 201, response.text
    res = response.json()

    detail = models.LoanDetail.model_validate(res)
    assert len(detail.schedule) == 36
    assert detail.start.close_date == date(2029, 1, 15)
    last_payment = detail.start.last_payment
    assert last_payment == Decimal("39464.89")
