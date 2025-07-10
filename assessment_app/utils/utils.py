import datetime

from assessment_app.models.constants import DAYS_IN_YEAR
from datetime import datetime


def compute_cagr(start_price: float, end_price: float, start_ts: datetime, end_ts: datetime) -> float:
    """
    Compute Compound Annual Growth Rate (CAGR)

    Formula: CAGR = (End Value / Start Value)^(1/n) - 1
    where n is the number of years
    """
    # Calculate number of years between start and end dates
    years = (end_ts - start_ts).days / 365.25

    # Handle edge cases
    if years <= 0:
        return 0.0
    if start_price <= 0:
        return 0.0

    # Calculate CAGR using the formula
    cagr = (end_price / start_price) ** (1 / years) - 1

    return cagr
