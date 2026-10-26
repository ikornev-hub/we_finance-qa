from datetime import date
from decimal import Decimal
from enum import Enum, StrEnum

from pydantic import BaseModel, ConfigDict


class DAY_ENUM(Enum):
    ACTUAL = "actual"
    DAYS_365 = "365"


class PAYMENT_DAY_CHANGE(BaseModel):
    start: date
    day: int


class RATE(BaseModel):
    annual_rate: Decimal
    start: date


class MODEL_LOAN(BaseModel):
    day_count: DAY_ENUM = DAY_ENUM.ACTUAL
    first_payment_date: date
    issue_date: date
    monthly_fee: Decimal = Decimal("0.00")
    months: int
    name: str
    payment: Decimal
    payment_day_changes: list[PAYMENT_DAY_CHANGE] = []
    principal: Decimal
    rates: list[RATE]
    weekend_shift: bool = True


class ScheduleRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    number: int
    date: date
    payment: Decimal
    principal: Decimal
    interest: Decimal
    balance: Decimal
    fee: Decimal


class PaymentStatus(StrEnum):
    """Статус платежа на дату: проведён, сегодня, запланирован."""

    DONE = "done"
    TODAY = "today"
    PLANNED = "planned"


class ScheduleItem(ScheduleRow):
    past: bool
    status: PaymentStatus


class EntryKind(StrEnum):
    """Тип записи истории: обычный платёж по графику или досрочный."""

    REGULAR = "regular"
    PREPAYMENT = "prepayment"


class HistoryEntry(BaseModel):
    """Прошедший платёж: обычный или ЧДП."""

    date: date
    kind: EntryKind
    amount: Decimal
    principal: Decimal
    interest: Decimal
    fee: Decimal
    balance: Decimal
    status: PaymentStatus


class LoanWarning(BaseModel):
    """Предупреждение расчёта (например, ЧДП после закрытия кредита)."""

    code: str
    message: str


class LoanState(BaseModel):
    """Снимок кредита на дату: start — без досрочек, actual — с ними."""

    as_of: date
    balance: Decimal
    next_payment: ScheduleRow | None
    close_date: date
    last_payment: Decimal
    payments_left: int


class LoanDetail(BaseModel):
    """Ответ POST /api/v1/loans и GET /api/v1/loans/{id} — кредит целиком."""

    id: str
    name: str
    start: LoanState
    actual: LoanState
    prepaid_total: Decimal
    interest_saved: Decimal
    months_saved: int
    schedule: list[ScheduleItem]
    history: list[HistoryEntry]
    warnings: list[LoanWarning]


class LoanSummary(BaseModel):
    """Элемент ответа GET /api/v1/loans — кредит коротко."""

    id: str
    name: str
    principal: Decimal
    balance: Decimal
    close_date: date
