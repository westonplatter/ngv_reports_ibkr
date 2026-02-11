import re

import pandas as pd

# IBKR timezone abbreviations mapped to IANA timezone names
# The abbreviation tells us which timezone region, the date determines DST
IBKR_TZ_REGIONS = {
    "EST": "America/New_York",
    "EDT": "America/New_York",
    "CST": "America/Chicago",
    "CDT": "America/Chicago",
    "MST": "America/Denver",
    "MDT": "America/Denver",
    "PST": "America/Los_Angeles",
    "PDT": "America/Los_Angeles",
    "UTC": "UTC",
    "GMT": "UTC",
}

# Default timezone for IBKR data
IBKR_DEFAULT_TZ = "America/New_York"


def parse_datetime_series(raw_series: pd.Series, target_tz: str = IBKR_DEFAULT_TZ) -> pd.Series:
    """
    Parse IBKR datetime strings to timezone-aware pandas datetime.

    Args:
        raw_series: Series with IBKR datetime strings like "2026-01-15;10:30:00 EST"
        target_tz: Target timezone for output (default: America/New_York)

    Returns:
        Timezone-aware datetime series in target_tz
    """
    import warnings
    from zoneinfo import ZoneInfo

    raw_series = raw_series.replace("", pd.NaT)

    # Extract timezone abbreviations to determine source timezone
    tz_pattern = r" ([A-Z]{3,4})$"
    tz_matches = raw_series.str.extract(tz_pattern, expand=False).dropna().unique()

    # Check for unknown timezone abbreviations
    unknown_tz = [tz for tz in tz_matches if tz not in IBKR_TZ_REGIONS]
    if unknown_tz:
        warnings.warn(f"Unknown timezone abbreviation(s) in datetime data: {unknown_tz}. " f"Will use {IBKR_DEFAULT_TZ}. Known: {list(IBKR_TZ_REGIONS.keys())}")

    # Determine source timezone (use first known TZ found, or default)
    source_tz = IBKR_DEFAULT_TZ
    for tz in tz_matches:
        if tz in IBKR_TZ_REGIONS:
            source_tz = IBKR_TZ_REGIONS[tz]
            break

    # Strip timezone abbreviation suffix
    raw_series_no_tz = raw_series.str.replace(r" [A-Z]{3,4}$", "", regex=True)

    # Remove colons in time portion
    # ie, "2021-08-20;09:30:00" -> "2021-08-20;093000"
    raw_series_without_colons = raw_series_no_tz.str.replace(":", "")

    # Parse as naive datetime
    fmt = "%Y-%m-%d;%H%M%S"
    series = pd.to_datetime(raw_series_without_colons, format=fmt, errors="coerce")

    # Localize to source timezone (handles DST automatically based on date)
    series = series.dt.tz_localize(source_tz)

    # Convert to target timezone if different
    if source_tz != target_tz:
        series = series.dt.tz_convert(target_tz)

    return series


def parse_date_series(raw_series: pd.Series) -> pd.Series:
    FORMAT = "%Y-%m-%d"
    raw_series = raw_series.replace(r"", pd.NaT)
    series = pd.to_datetime(raw_series, errors="raise", format=FORMAT).dt.date
    return series


class Mutations:
    @classmethod
    def columns_to_snake_case(cls, df) -> None:
        def camel_to_snake(name):
            name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
            return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()

        snake_case_cols = {}
        for col in df.columns:
            snake_case_cols[col] = camel_to_snake(col)
        df.rename(columns=snake_case_cols, inplace=True)


class Transforms:
    @classmethod
    def filter_to_executions(cls, df) -> pd.DataFrame:
        """
        Filter TWS realtime trades to only rows with actual executions.

        Removes rows created from log entries that don't represent trades.
        """
        return df[df["fill_execution_id"].notna()].reset_index(drop=True)

    @classmethod
    def add_strike(cls, df) -> None:
        ddf = df.query('asset_category.isin(["OPT", "FOP"])').description.str.split(" ", expand=True)
        df["strike"] = pd.to_numeric(ddf[2])

    @classmethod
    def convert_date_time(cls, df) -> None:
        df.dateTime = parse_datetime_series(df.dateTime)

    @classmethod
    def convert_open_date_time(cls, df) -> None:
        df.openDateTime = parse_datetime_series(df.openDateTime)

    @classmethod
    def convert_holding_period_date_time(cls, df) -> None:
        df.holdingPeriodDateTime = parse_datetime_series(df.holdingPeriodDateTime)

    @classmethod
    def convert_report_date(cls, df) -> None:
        df.reportDate = parse_date_series(df.reportDate)
