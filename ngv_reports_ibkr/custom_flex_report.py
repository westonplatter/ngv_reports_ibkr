from typing import List

import pandas as pd
import pandera.pandas as pa
from ib_async.flexreport import FlexReport
from loguru import logger

from ngv_reports_ibkr.schemas.ibkr_flex_report import (
    validate_ibkr_flex_report_trades_lazy,
)
from ngv_reports_ibkr.transforms import parse_date_series, parse_datetime_series


class CustomFlexReport(FlexReport):
    def account_ids(self) -> List[str]:
        return list(self.df("AccountInformation")["accountId"].unique())

    def open_positions_by_account_id(self, account_id: str) -> pd.DataFrame:
        df = self.df("OpenPosition")
        # early return if all account have no open positions
        if (df is None) or (len(df.index) == 0):
            return None
        df = df.copy()

        # early return if specific account has no open positions
        df = df[df.accountId == account_id].copy()
        if (df is None) or (len(df.index) == 0):
            return None

        df = df.query("levelOfDetail == 'LOT'").copy()
        df.openDateTime = parse_datetime_series(df.openDateTime)
        df.holdingPeriodDateTime = parse_datetime_series(df.holdingPeriodDateTime)
        df.reportDate = parse_date_series(df.reportDate)
        return df

    def trades_by_account_id(self, account_id: str) -> pd.DataFrame:
        """
        Get trades for a specific account with schema validation.

        Parameters
        ----------
        account_id : str
            The account ID to filter trades for

        Returns
        -------
        pd.DataFrame or None
            DataFrame of trades for the account, or None if no trades exist.
            Returns the DataFrame even if schema validation fails (with errors logged).

        Notes
        -----
        This method validates the returned DataFrame against the IBKR flex report
        trades schema to ensure data integrity. Validation failures are logged as
        errors but do not prevent the DataFrame from being returned. This allows
        analysis of potentially corrupted data while alerting to schema mismatches.

        Schema validation errors are logged with:
        - Account ID context
        - Number of validation failures
        - Detailed error messages

        If validation fails, check logs for specific column/type mismatches.
        """
        df = self.df("Trade")
        # early return if all accounts have no trades
        if (df is None) or (len(df.index) == 0):
            return None

        df = df[df.accountId == account_id].copy()
        # early return if specific account has no trades
        if (df is None) or (len(df.index) == 0):
            return None

        df.dateTime = parse_datetime_series(df.dateTime)
        df.orderTime = parse_datetime_series(df.orderTime)
        df.tradeDate = parse_date_series(df.tradeDate)

        # Validate DataFrame against schema
        try:
            return validate_ibkr_flex_report_trades_lazy(df)
        except pa.errors.SchemaErrors as e:
            logger.error(
                f"Trades data for account '{account_id}' failed schema validation. "
                f"This may indicate corrupted IBKR data or a schema mismatch. "
                f"Found {len(e.failure_cases)} validation error(s). "
                f"Original error: {str(e)}"
            )
            return df

    def closed_trades_by_account_id(self, account_id: str) -> pd.DataFrame:
        df = self.trades_by_account_id(account_id)
        if (df is None) or (len(df.index) == 0):
            return None
        return df.query("openCloseIndicator == 'C'").copy()

    def orders_by_account_id(self, account_id: str) -> pd.DataFrame:
        return self.df("Order").query("accountId == @account_id").copy()

    def change_in_nav_by_account_id(self, account_id: str) -> pd.DataFrame:
        return self.df("ChangeInNAV").query("accountId == account_id").copy()
