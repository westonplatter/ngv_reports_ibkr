"""
Helpers that behave the same on ib_async v2 and v3.

v3 changes that matter here:

- ``util.df`` returns polars. ``util.pandasDf`` (new in v3) returns pandas.
- Execution, commission, order and order-status numbers are ``Decimal | None``.
- ``CommissionReport.commission`` is renamed to ``commissionAndFees``. The old
  name still works on v3 with a ``DeprecationWarning`` and is removed in v4.
"""

from collections.abc import Iterable
from decimal import Decimal
from typing import Any

import pandas as pd
from ib_async import util


def pandas_df(objs: Iterable[Any]) -> pd.DataFrame | None:
    """
    Build a pandas DataFrame from ib_async objects.

    Uses ``util.pandasDf`` on v3 and ``util.df`` on v2. With no objects, v2
    returns ``None`` and v3 returns an empty DataFrame with no columns.
    """
    to_pandas = getattr(util, "pandasDf", util.df)
    return to_pandas(objs)


def to_float(value: Any) -> Any:
    """Convert a ``Decimal`` to ``float``. Leave every other value as is."""
    if isinstance(value, Decimal):
        return float(value)
    return value


def commission_and_fees(commission_report: Any) -> Any:
    """Read a CommissionReport's commission: ``commissionAndFees`` on v3, ``commission`` on v2."""
    if commission_report is None:
        return None
    if hasattr(commission_report, "commissionAndFees"):
        return commission_report.commissionAndFees
    return getattr(commission_report, "commission", None)
