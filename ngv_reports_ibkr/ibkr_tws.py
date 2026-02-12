"""
IBKR Trader Workstation real-time data source.

Wraps the ib_async IB connection and provides methods for fetching
real-time data (positions, trades, executions) from the TWS API.

Follows the adapter pattern established in custom_flex_report.py:
- IbkrTws wraps the data source and provides DataFrame export methods
- TwsReportOutputAdapterPandas wraps IbkrTws for structured output

See: notebooks/ibkr_tws_realtime.ipynb for the original prototype.
"""

from abc import ABC
from typing import List, Optional

import pandas as pd
import pandera.pandas as pa
from loguru import logger
from pydantic import BaseModel

from ngv_reports_ibkr.expand_contract_columns import expand_contract_column
from ngv_reports_ibkr.schemas.ibkr_tws_positions import (
    validate_ibkr_tws_positions_lazy,
)


class RealTimeSource(ABC):
    """Base class for real-time market data sources."""

    pass


class IbkrTws(RealTimeSource):
    """
    IBKR Trader Workstation real-time data source.

    Wraps an ib_async IB connection and provides methods for fetching
    positions, trades, and executions.

    Parameters
    ----------
    ib : ib_async.IB
        Connected IB instance. Caller is responsible for connection lifecycle.

    Examples
    --------
    >>> from ib_async import IB
    >>> ib = IB().connect("127.0.0.1", 7496, clientId=1)
    >>> tws = IbkrTws(ib=ib)
    >>> accounts = tws.get_accounts()
    >>> positions_df = tws.positions_df(accounts[0])
    """

    def __init__(self, ib=None):
        self.ib = ib

    def get_accounts(self) -> List[str]:
        """Return list of managed account IDs."""
        return self.ib.managedAccounts()

    def get_positions_for_account(self, account_id: str) -> list:
        """
        Fetch raw ib_async Position objects for an account.

        Parameters
        ----------
        account_id : str
            IBKR account ID (e.g., "U1234567")

        Returns
        -------
        list
            List of ib_async Position namedtuples
            (account, contract, position, avgCost)
        """
        return self.ib.positions(account=account_id)

    def positions_df(self, account_id: str) -> Optional[pd.DataFrame]:
        """
        Export positions for an account as a validated pandas DataFrame.

        Fetches raw Position objects, expands contract fields into flat
        columns, and validates against the TWS positions schema.

        Parameters
        ----------
        account_id : str
            IBKR account ID (e.g., "U1234567")

        Returns
        -------
        pd.DataFrame or None
            DataFrame of positions with expanded contract fields,
            or None if the account has no positions.
            Returns the DataFrame even if schema validation fails
            (with errors logged).
        """
        positions = self.get_positions_for_account(account_id)

        if not positions:
            logger.info(f"No positions found for account {account_id}")
            return None

        rows = []
        for pos in positions:
            rows.append(
                {
                    "account": pos.account,
                    "contract": pos.contract,
                    "position": float(pos.position),
                    "avgCost": float(pos.avgCost),
                }
            )

        df = pd.DataFrame(rows)
        df = expand_contract_column(df, "contract")

        try:
            return validate_ibkr_tws_positions_lazy(df)
        except pa.errors.SchemaErrors as e:
            logger.error(
                f"Positions data for account '{account_id}' failed schema validation. "
                f"This may indicate a schema mismatch with live TWS data. "
                f"Found {len(e.failure_cases)} validation error(s). "
                f"Original error: {str(e)}"
            )
            return df

    def get_trades(self) -> list:
        """Return raw ib_async Trade objects."""
        return self.ib.trades()

    def get_executions(self) -> list:
        """Return raw ib_async execution objects."""
        return self.ib.executions()


class TwsReportOutputAdapterPandas(BaseModel):
    """
    Adapter for returning TWS report sections as pandas DataFrames.

    Follows the same pattern as ReportOutputAdapterPandas in adapters.py.
    Wraps an IbkrTws instance and provides structured DataFrame output.

    Examples
    --------
    >>> tws = IbkrTws(ib=connected_ib)
    >>> adapter = TwsReportOutputAdapterPandas(tws=tws)
    >>> positions_df = adapter.get_positions("U1234567")
    """

    class Config:
        arbitrary_types_allowed = True

    tws: IbkrTws

    def get_positions(self, account_id: str) -> Optional[pd.DataFrame]:
        """
        Get positions for an account as a DataFrame.

        Parameters
        ----------
        account_id : str
            IBKR account ID

        Returns
        -------
        pd.DataFrame or None
            DataFrame of positions, or None if no positions exist.
        """
        df = self.tws.positions_df(account_id)
        if df is None:
            logger.warning(
                f"AccountId={account_id}. No positions data from TWS. "
                "Is the account connected and has open positions?"
            )
            return None
        return df

    def process_accounts(self) -> List[dict]:
        """
        For each account, generate a dict of DataFrames for all sections.

        Returns
        -------
        List[dict]
            List of dicts with section DataFrames per account.
        """
        results = []
        for account_id in self.tws.get_accounts():
            logger.info(f"TWS Pandas output adapter for {account_id}")
            dict_of_dfs = self.put_all(aid=account_id)
            results.append(dict_of_dfs)
        return results

    def put_all(self, aid: str) -> dict:
        """
        Generate a dict of DataFrames for all available sections.

        Parameters
        ----------
        aid : str
            Account ID

        Returns
        -------
        dict
            Dict with section name keys and DataFrame values.
        """
        return {
            "positions": self.get_positions(aid),
        }
