"""
Flex Web Service client for IBKR API.

This module provides direct HTTP communication with the IBKR Flex Web Service,
supporting custom date ranges, token lifecycle management, and robust error handling.

The IBKR Flex Web Service has two main endpoints:
1. SendRequest - Initiates a flex query and returns a reference code
2. GetStatement - Retrieves the generated statement using the reference code

Reference: https://www.interactivebrokers.com/en/software/am/am/reports/flex_web_service_version_3.htm
"""

import random
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Callable, Optional, Protocol

import requests
from loguru import logger


# =============================================================================
# Exceptions
# =============================================================================


class FlexClientError(Exception):
    """Base exception for all flex client errors."""

    pass


class FlexRequestError(FlexClientError):
    """Error during SendRequest phase."""

    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message)
        self.error_code = error_code


class FlexStatementError(FlexClientError):
    """Error during GetStatement phase."""

    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message)
        self.error_code = error_code


class FlexTokenError(FlexClientError):
    """Token-related error (invalid or expired)."""

    pass


class FlexTokenExpiredError(FlexTokenError):
    """Token has expired (6-hour lifetime exceeded)."""

    pass


class FlexRetryableError(FlexClientError):
    """Error that can be retried (server busy, rate limited, etc.)."""

    def __init__(self, message: str, error_code: Optional[str] = None, retry_after: float = 5.0):
        super().__init__(message)
        self.error_code = error_code
        self.retry_after = retry_after


class FlexDateRangeError(FlexClientError):
    """Invalid date range (exceeds 365 days or invalid format)."""

    pass


# =============================================================================
# Error Code Mapping
# =============================================================================


class FlexErrorCode(str, Enum):
    """Known IBKR Flex API error codes."""

    SERVER_BUSY = "1009"
    TOKEN_EXPIRED = "1012"
    INVALID_TOKEN = "1015"
    RATE_LIMITED = "1018"
    STATEMENT_IN_PROGRESS = "1019"
    INVALID_QUERY = "1003"
    QUERY_NOT_FOUND = "1004"
    DATE_RANGE_EXCEEDED = "1020"


# Error codes that should trigger a retry
RETRYABLE_ERROR_CODES = {
    FlexErrorCode.SERVER_BUSY,
    FlexErrorCode.RATE_LIMITED,
    FlexErrorCode.STATEMENT_IN_PROGRESS,
}

# Error codes related to token issues (no retry)
TOKEN_ERROR_CODES = {
    FlexErrorCode.TOKEN_EXPIRED,
    FlexErrorCode.INVALID_TOKEN,
}


# =============================================================================
# Response Models
# =============================================================================


@dataclass
class FlexRequestResponse:
    """Response from SendRequest endpoint."""

    status: str
    reference_code: Optional[str] = None
    url: Optional[str] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    @property
    def is_success(self) -> bool:
        return self.status.lower() == "success"


@dataclass
class FlexStatementResponse:
    """Response from GetStatement endpoint."""

    status: str
    xml_data: Optional[str] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None

    @property
    def is_success(self) -> bool:
        return self.status.lower() == "success"


@dataclass
class DateRange:
    """Custom date range for flex queries."""

    from_date: date
    to_date: date

    def __post_init__(self):
        """Validate date range constraints."""
        if self.from_date > self.to_date:
            raise FlexDateRangeError(f"from_date ({self.from_date}) must be before to_date ({self.to_date})")

        delta = self.to_date - self.from_date
        if delta.days > 365:
            raise FlexDateRangeError(f"Date range cannot exceed 365 days (got {delta.days} days)")

        if self.to_date > date.today():
            raise FlexDateRangeError(f"to_date ({self.to_date}) cannot be in the future")

    def to_query_params(self) -> dict:
        """Convert to IBKR API query parameters."""
        return {
            "fd": self.from_date.strftime("%Y%m%d"),
            "td": self.to_date.strftime("%Y%m%d"),
        }


# =============================================================================
# HTTP Client Protocol
# =============================================================================


class FlexHTTPClient(Protocol):
    """Protocol for Flex API HTTP operations - enables testing with mocks."""

    def send_request(
        self,
        token: str,
        query_id: str,
        version: str = "3",
        date_range: Optional[DateRange] = None,
    ) -> str:
        """Send flex request, return XML response."""
        ...

    def get_statement(self, token: str, reference_code: str, version: str = "3") -> str:
        """Get statement, return XML response."""
        ...


# =============================================================================
# HTTP Client Implementation
# =============================================================================


class HTTPFlexClient:
    """
    Real HTTP implementation of Flex API client.

    This class handles the low-level HTTP communication with IBKR's Flex Web Service.
    """

    BASE_URL = "https://ndcdyn.interactivebrokers.com/AccountManagement/FlexWebService"
    USER_AGENT = "ngv_reports_ibkr/1.0"

    def __init__(self, timeout: int = 30):
        """
        Initialize HTTP client.

        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.USER_AGENT})

    def send_request(
        self,
        token: str,
        query_id: str,
        version: str = "3",
        date_range: Optional[DateRange] = None,
    ) -> str:
        """
        Send flex request to IBKR API.

        Args:
            token: Flex Web Service access token
            query_id: Query ID for the flex report
            version: API version (default: "3")
            date_range: Optional custom date range

        Returns:
            XML response string

        Raises:
            requests.HTTPError: On HTTP errors
            requests.Timeout: On timeout
        """
        url = f"{self.BASE_URL}/SendRequest"
        params = {"t": token, "q": query_id, "v": version}

        if date_range:
            params.update(date_range.to_query_params())

        logger.debug(f"Sending flex request: query_id={query_id}, date_range={date_range}")
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    def get_statement(self, token: str, reference_code: str, version: str = "3") -> str:
        """
        Get flex statement from IBKR API.

        Args:
            token: Flex Web Service access token
            reference_code: Reference code from send_request
            version: API version (default: "3")

        Returns:
            XML response string

        Raises:
            requests.HTTPError: On HTTP errors
            requests.Timeout: On timeout
        """
        url = f"{self.BASE_URL}/GetStatement"
        params = {"t": token, "q": reference_code, "v": version}

        logger.debug(f"Getting statement: reference_code={reference_code}")
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.text


# =============================================================================
# Flex Request Service
# =============================================================================


class FlexClient:
    """
    High-level client for IBKR Flex Web Service operations.

    This class orchestrates the full flex report workflow:
    1. Send request to initiate report generation
    2. Poll for statement completion
    3. Retrieve the generated statement

    It handles retries with exponential backoff, error classification,
    and token lifecycle awareness.

    Example:
        >>> client = FlexClient()
        >>> xml_data = client.fetch_flex_report(
        ...     token="your_token",
        ...     query_id="123456",
        ...     date_range=DateRange(date(2024, 1, 1), date(2024, 12, 31))
        ... )
    """

    def __init__(
        self,
        http_client: Optional[FlexHTTPClient] = None,
        max_retries: int = 5,
        base_retry_delay: float = 1.0,
        max_retry_delay: float = 60.0,
        statement_poll_delay: float = 2.0,
    ):
        """
        Initialize flex client.

        Args:
            http_client: HTTP client (defaults to HTTPFlexClient)
            max_retries: Maximum retry attempts for API calls
            base_retry_delay: Base delay in seconds for exponential backoff
            max_retry_delay: Maximum delay between retries
            statement_poll_delay: Initial delay before fetching statement
        """
        self.http_client = http_client or HTTPFlexClient()
        self.max_retries = max_retries
        self.base_retry_delay = base_retry_delay
        self.max_retry_delay = max_retry_delay
        self.statement_poll_delay = statement_poll_delay

    def _calculate_retry_delay(self, attempt: int, base_delay: Optional[float] = None) -> float:
        """
        Calculate retry delay with exponential backoff and jitter.

        Args:
            attempt: Current attempt number (0-indexed)
            base_delay: Base delay override

        Returns:
            Delay in seconds
        """
        base = base_delay or self.base_retry_delay
        delay = base * (2**attempt)
        delay = min(delay, self.max_retry_delay)
        # Add jitter (0.5x to 1.5x)
        jitter = 0.5 + random.random()
        return delay * jitter

    def _parse_send_request_response(self, xml_text: str) -> FlexRequestResponse:
        """Parse XML response from SendRequest endpoint."""
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError as e:
            raise FlexRequestError(f"Failed to parse XML response: {e}")

        status_elem = root.find("Status")
        ref_code_elem = root.find("ReferenceCode")
        url_elem = root.find("Url")
        error_code_elem = root.find("ErrorCode")
        error_msg_elem = root.find("ErrorMessage")

        return FlexRequestResponse(
            status=status_elem.text if status_elem is not None else "Fail",
            reference_code=ref_code_elem.text if ref_code_elem is not None else None,
            url=url_elem.text if url_elem is not None else None,
            error_code=error_code_elem.text if error_code_elem is not None else None,
            error_message=error_msg_elem.text if error_msg_elem is not None else None,
        )

    def _parse_statement_response(self, xml_text: str) -> FlexStatementResponse:
        """Parse XML response from GetStatement endpoint."""
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError as e:
            raise FlexStatementError(f"Failed to parse XML response: {e}")

        # Check for error response (FlexStatementResponse wrapper)
        if root.tag == "FlexStatementResponse":
            status_elem = root.find("Status")
            error_code_elem = root.find("ErrorCode")
            error_msg_elem = root.find("ErrorMessage")

            return FlexStatementResponse(
                status=status_elem.text if status_elem is not None else "Fail",
                error_code=error_code_elem.text if error_code_elem is not None else None,
                error_message=error_msg_elem.text if error_msg_elem is not None else None,
            )

        # Success - entire XML is the statement (FlexQueryResponse or similar)
        return FlexStatementResponse(
            status="Success",
            xml_data=xml_text,
        )

    def _raise_for_error(self, error_code: Optional[str], error_message: Optional[str]):
        """
        Raise appropriate exception based on error code.

        Args:
            error_code: IBKR error code
            error_message: Error message from API
        """
        msg = f"{error_code}: {error_message}" if error_code else error_message or "Unknown error"

        if error_code in TOKEN_ERROR_CODES:
            if error_code == FlexErrorCode.TOKEN_EXPIRED:
                raise FlexTokenExpiredError(msg)
            raise FlexTokenError(msg)

        if error_code in RETRYABLE_ERROR_CODES:
            retry_after = 10.0 if error_code == FlexErrorCode.RATE_LIMITED else 5.0
            raise FlexRetryableError(msg, error_code=error_code, retry_after=retry_after)

        raise FlexRequestError(msg, error_code=error_code)

    def send_flex_request(
        self,
        token: str,
        query_id: str,
        date_range: Optional[DateRange] = None,
    ) -> str:
        """
        Send flex request and return reference code.

        Args:
            token: Flex Web Service token
            query_id: Query ID for the flex report
            date_range: Optional custom date range

        Returns:
            Reference code for retrieving statement

        Raises:
            FlexRequestError: On API errors
            FlexTokenError: On token-related errors
            FlexRetryableError: On transient errors (after max retries)
        """
        last_error: Optional[Exception] = None

        for attempt in range(self.max_retries):
            try:
                xml_response = self.http_client.send_request(
                    token=token,
                    query_id=query_id,
                    date_range=date_range,
                )
                response = self._parse_send_request_response(xml_response)

                if response.is_success:
                    logger.info(f"Flex request sent successfully: reference_code={response.reference_code}")
                    return response.reference_code

                # API returned an error
                self._raise_for_error(response.error_code, response.error_message)

            except FlexRetryableError as e:
                last_error = e
                delay = self._calculate_retry_delay(attempt, e.retry_after)
                logger.warning(f"Attempt {attempt + 1}/{self.max_retries} failed (retryable): {e}. Retrying in {delay:.1f}s")
                if attempt < self.max_retries - 1:
                    time.sleep(delay)

            except (FlexTokenError, FlexTokenExpiredError):
                # Token errors should not be retried
                raise

            except requests.RequestException as e:
                last_error = e
                delay = self._calculate_retry_delay(attempt)
                logger.warning(f"Attempt {attempt + 1}/{self.max_retries} failed (network): {e}. Retrying in {delay:.1f}s")
                if attempt < self.max_retries - 1:
                    time.sleep(delay)

            except Exception as e:
                last_error = e
                delay = self._calculate_retry_delay(attempt)
                logger.warning(f"Attempt {attempt + 1}/{self.max_retries} failed: {e}. Retrying in {delay:.1f}s")
                if attempt < self.max_retries - 1:
                    time.sleep(delay)

        raise FlexRequestError(f"Failed after {self.max_retries} attempts: {last_error}")

    def get_flex_statement(self, token: str, reference_code: str) -> str:
        """
        Get flex statement XML.

        Args:
            token: Flex Web Service token
            reference_code: Reference code from send_flex_request

        Returns:
            XML statement data

        Raises:
            FlexStatementError: On API errors
            FlexRetryableError: On transient errors (after max retries)
        """
        last_error: Optional[Exception] = None

        for attempt in range(self.max_retries):
            try:
                xml_response = self.http_client.get_statement(token=token, reference_code=reference_code)
                response = self._parse_statement_response(xml_response)

                if response.is_success:
                    logger.info("Flex statement retrieved successfully")
                    return response.xml_data

                # API returned an error
                self._raise_for_error(response.error_code, response.error_message)

            except FlexRetryableError as e:
                last_error = e
                delay = self._calculate_retry_delay(attempt, e.retry_after)
                logger.warning(f"Attempt {attempt + 1}/{self.max_retries} failed (retryable): {e}. Retrying in {delay:.1f}s")
                if attempt < self.max_retries - 1:
                    time.sleep(delay)

            except (FlexTokenError, FlexTokenExpiredError):
                raise

            except requests.RequestException as e:
                last_error = e
                delay = self._calculate_retry_delay(attempt)
                logger.warning(f"Attempt {attempt + 1}/{self.max_retries} failed (network): {e}. Retrying in {delay:.1f}s")
                if attempt < self.max_retries - 1:
                    time.sleep(delay)

            except Exception as e:
                last_error = e
                delay = self._calculate_retry_delay(attempt)
                logger.warning(f"Attempt {attempt + 1}/{self.max_retries} failed: {e}. Retrying in {delay:.1f}s")
                if attempt < self.max_retries - 1:
                    time.sleep(delay)

        raise FlexStatementError(f"Failed after {self.max_retries} attempts: {last_error}")

    def fetch_flex_report(
        self,
        token: str,
        query_id: str,
        date_range: Optional[DateRange] = None,
    ) -> str:
        """
        Complete flex report fetch: send request + get statement.

        This is the high-level API that most consumers should use.

        Args:
            token: Flex Web Service token
            query_id: Query ID for the flex report
            date_range: Optional custom date range

        Returns:
            XML statement data

        Raises:
            FlexClientError: On any API error
        """
        reference_code = self.send_flex_request(token, query_id, date_range)

        # Wait for IBKR to generate the report
        logger.debug(f"Waiting {self.statement_poll_delay}s for statement generation")
        time.sleep(self.statement_poll_delay)

        return self.get_flex_statement(token, reference_code)
