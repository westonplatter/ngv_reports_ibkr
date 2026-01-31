"""Tests for flex_client module."""

from datetime import date, timedelta
from unittest.mock import Mock, patch

import pytest
import requests

from ngv_reports_ibkr.flex_client import (
    DateRange,
    FlexClient,
    FlexClientError,
    FlexDateRangeError,
    FlexRequestError,
    FlexRequestResponse,
    FlexRetryableError,
    FlexStatementError,
    FlexStatementResponse,
    FlexTokenError,
    FlexTokenExpiredError,
    HTTPFlexClient,
)

from tests.fixtures import (
    create_get_statement_error,
    create_get_statement_success,
    create_send_request_error,
    create_send_request_success,
)


class TestDateRange:
    """Tests for DateRange dataclass."""

    def test_valid_date_range(self):
        """Test creating valid date range."""
        dr = DateRange(from_date=date(2026, 1, 1), to_date=date(2026, 1, 31))
        assert dr.from_date == date(2026, 1, 1)
        assert dr.to_date == date(2026, 1, 31)

    def test_date_range_to_query_params(self):
        """Test conversion to query parameters."""
        dr = DateRange(from_date=date(2026, 1, 1), to_date=date(2026, 1, 31))
        params = dr.to_query_params()
        assert params == {"fd": "20260101", "td": "20260131"}

    def test_date_range_exceeds_365_days(self):
        """Test that date range > 365 days raises error."""
        with pytest.raises(FlexDateRangeError, match="cannot exceed 365 days"):
            DateRange(from_date=date(2024, 1, 1), to_date=date(2025, 2, 1))

    def test_date_range_from_after_to(self):
        """Test that from_date after to_date raises error."""
        with pytest.raises(FlexDateRangeError, match="must be before"):
            DateRange(from_date=date(2026, 2, 1), to_date=date(2026, 1, 1))

    def test_date_range_future_date(self):
        """Test that future to_date raises error."""
        future = date.today() + timedelta(days=10)
        with pytest.raises(FlexDateRangeError, match="cannot be in the future"):
            DateRange(from_date=date.today(), to_date=future)

    def test_date_range_exactly_365_days(self):
        """Test that exactly 365 days is valid."""
        today = date.today()
        start = today - timedelta(days=365)
        dr = DateRange(from_date=start, to_date=today)
        assert (dr.to_date - dr.from_date).days == 365


class TestFlexRequestResponse:
    """Tests for FlexRequestResponse dataclass."""

    def test_success_response(self):
        """Test successful response."""
        resp = FlexRequestResponse(status="Success", reference_code="12345")
        assert resp.is_success
        assert resp.reference_code == "12345"

    def test_failure_response(self):
        """Test failure response."""
        resp = FlexRequestResponse(
            status="Fail",
            error_code="1003",
            error_message="Invalid query",
        )
        assert not resp.is_success
        assert resp.error_code == "1003"


class TestFlexStatementResponse:
    """Tests for FlexStatementResponse dataclass."""

    def test_success_response(self):
        """Test successful response with XML data."""
        resp = FlexStatementResponse(status="Success", xml_data="<FlexQueryResponse/>")
        assert resp.is_success
        assert resp.xml_data == "<FlexQueryResponse/>"

    def test_failure_response(self):
        """Test failure response."""
        resp = FlexStatementResponse(
            status="Fail",
            error_code="1019",
            error_message="Statement in progress",
        )
        assert not resp.is_success


class TestHTTPFlexClient:
    """Tests for HTTPFlexClient."""

    def test_user_agent_header(self):
        """Test that User-Agent header is set."""
        client = HTTPFlexClient()
        assert "User-Agent" in client.session.headers
        assert "ngv_reports_ibkr" in client.session.headers["User-Agent"]

    @patch("requests.Session.get")
    def test_send_request_basic(self, mock_get):
        """Test basic send request."""
        mock_response = Mock()
        mock_response.text = create_send_request_success()
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = HTTPFlexClient()
        result = client.send_request(token="test_token", query_id="123456")

        assert "<Status>Success</Status>" in result
        mock_get.assert_called_once()
        call_kwargs = mock_get.call_args[1]
        assert call_kwargs["params"]["t"] == "test_token"
        assert call_kwargs["params"]["q"] == "123456"
        assert call_kwargs["params"]["v"] == "3"

    @patch("requests.Session.get")
    def test_send_request_with_date_range(self, mock_get):
        """Test send request with date range."""
        mock_response = Mock()
        mock_response.text = create_send_request_success()
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = HTTPFlexClient()
        date_range = DateRange(from_date=date(2026, 1, 1), to_date=date(2026, 1, 15))
        result = client.send_request(token="test_token", query_id="123456", date_range=date_range)

        call_kwargs = mock_get.call_args[1]
        assert call_kwargs["params"]["fd"] == "20260101"
        assert call_kwargs["params"]["td"] == "20260115"

    @patch("requests.Session.get")
    def test_get_statement(self, mock_get):
        """Test get statement."""
        mock_response = Mock()
        mock_response.text = create_get_statement_success()
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = HTTPFlexClient()
        result = client.get_statement(token="test_token", reference_code="REF123")

        assert "<FlexQueryResponse" in result
        call_kwargs = mock_get.call_args[1]
        assert call_kwargs["params"]["q"] == "REF123"


class TestFlexClient:
    """Tests for FlexClient high-level operations."""

    @pytest.fixture
    def mock_http_client(self):
        """Create mock HTTP client."""
        return Mock()

    @pytest.fixture
    def flex_client(self, mock_http_client):
        """Create FlexClient with mocked HTTP."""
        return FlexClient(
            http_client=mock_http_client,
            max_retries=3,
            base_retry_delay=0.01,  # Fast retries for testing
            statement_poll_delay=0.01,
        )

    def test_send_flex_request_success(self, flex_client, mock_http_client):
        """Test successful send request."""
        mock_http_client.send_request.return_value = create_send_request_success("REF12345")

        ref_code = flex_client.send_flex_request(token="token123", query_id="654321")

        assert ref_code == "REF12345"
        mock_http_client.send_request.assert_called_once()

    def test_send_flex_request_with_date_range(self, flex_client, mock_http_client):
        """Test send request with custom date range."""
        mock_http_client.send_request.return_value = create_send_request_success("REF99999")

        date_range = DateRange(from_date=date(2026, 1, 1), to_date=date(2026, 1, 15))
        ref_code = flex_client.send_flex_request(
            token="token123",
            query_id="654321",
            date_range=date_range,
        )

        assert ref_code == "REF99999"
        call_kwargs = mock_http_client.send_request.call_args[1]
        assert call_kwargs["date_range"] == date_range

    def test_send_flex_request_invalid_token(self, flex_client, mock_http_client):
        """Test invalid token error (no retry)."""
        mock_http_client.send_request.return_value = create_send_request_error("1015", "Invalid token")

        with pytest.raises(FlexTokenError, match="1015"):
            flex_client.send_flex_request(token="bad_token", query_id="654321")

        # Should not retry for token errors
        assert mock_http_client.send_request.call_count == 1

    def test_send_flex_request_expired_token(self, flex_client, mock_http_client):
        """Test expired token error (no retry)."""
        mock_http_client.send_request.return_value = create_send_request_error("1012", "Token expired")

        with pytest.raises(FlexTokenExpiredError, match="1012"):
            flex_client.send_flex_request(token="expired_token", query_id="654321")

        assert mock_http_client.send_request.call_count == 1

    def test_send_flex_request_retry_on_server_busy(self, flex_client, mock_http_client):
        """Test retry on server busy error."""
        # Fail twice, succeed on third
        mock_http_client.send_request.side_effect = [
            create_send_request_error("1009", "Server busy"),
            create_send_request_error("1009", "Server busy"),
            create_send_request_success("REF_FINALLY"),
        ]

        ref_code = flex_client.send_flex_request(token="token123", query_id="654321")

        assert ref_code == "REF_FINALLY"
        assert mock_http_client.send_request.call_count == 3

    def test_send_flex_request_max_retries_exceeded(self, flex_client, mock_http_client):
        """Test failure after max retries."""
        mock_http_client.send_request.return_value = create_send_request_error("1009", "Server busy")

        with pytest.raises(FlexRequestError, match="Failed after 3 attempts"):
            flex_client.send_flex_request(token="token123", query_id="654321")

        assert mock_http_client.send_request.call_count == 3

    def test_send_flex_request_network_error_retry(self, flex_client, mock_http_client):
        """Test retry on network errors."""
        mock_http_client.send_request.side_effect = [
            requests.RequestException("Connection failed"),
            create_send_request_success("REF_RECOVERED"),
        ]

        ref_code = flex_client.send_flex_request(token="token123", query_id="654321")

        assert ref_code == "REF_RECOVERED"
        assert mock_http_client.send_request.call_count == 2

    def test_get_flex_statement_success(self, flex_client, mock_http_client):
        """Test successful get statement."""
        mock_http_client.get_statement.return_value = create_get_statement_success()

        xml_data = flex_client.get_flex_statement(token="token123", reference_code="REF123")

        assert "<FlexQueryResponse" in xml_data
        assert "U1234567" in xml_data

    def test_get_flex_statement_retry_in_progress(self, flex_client, mock_http_client):
        """Test retry when statement generation is in progress."""
        mock_http_client.get_statement.side_effect = [
            create_get_statement_error("1019", "Statement generation in progress"),
            create_get_statement_success(),
        ]

        xml_data = flex_client.get_flex_statement(token="token123", reference_code="REF123")

        assert "<FlexQueryResponse" in xml_data
        assert mock_http_client.get_statement.call_count == 2

    def test_fetch_flex_report_full_workflow(self, flex_client, mock_http_client):
        """Test complete fetch workflow."""
        mock_http_client.send_request.return_value = create_send_request_success("REF_WORKFLOW")
        mock_http_client.get_statement.return_value = create_get_statement_success()

        xml_data = flex_client.fetch_flex_report(token="token123", query_id="654321")

        assert "<FlexQueryResponse" in xml_data
        mock_http_client.send_request.assert_called_once()
        mock_http_client.get_statement.assert_called_once()

    def test_fetch_flex_report_with_date_range(self, flex_client, mock_http_client):
        """Test fetch with custom date range."""
        mock_http_client.send_request.return_value = create_send_request_success("REF_DATES")
        mock_http_client.get_statement.return_value = create_get_statement_success()

        date_range = DateRange(from_date=date(2026, 1, 1), to_date=date(2026, 1, 15))
        xml_data = flex_client.fetch_flex_report(
            token="token123",
            query_id="654321",
            date_range=date_range,
        )

        assert "<FlexQueryResponse" in xml_data
        call_kwargs = mock_http_client.send_request.call_args[1]
        assert call_kwargs["date_range"] == date_range


class TestExceptionHierarchy:
    """Tests for exception class hierarchy."""

    def test_flex_client_error_is_base(self):
        """Test that FlexClientError is the base exception."""
        assert issubclass(FlexRequestError, FlexClientError)
        assert issubclass(FlexStatementError, FlexClientError)
        assert issubclass(FlexTokenError, FlexClientError)
        assert issubclass(FlexRetryableError, FlexClientError)
        assert issubclass(FlexDateRangeError, FlexClientError)

    def test_flex_token_expired_is_token_error(self):
        """Test that FlexTokenExpiredError inherits from FlexTokenError."""
        assert issubclass(FlexTokenExpiredError, FlexTokenError)

    def test_exception_with_error_code(self):
        """Test exception with error code."""
        exc = FlexRequestError("Test error", error_code="1003")
        assert exc.error_code == "1003"
        assert "Test error" in str(exc)

    def test_retryable_error_with_retry_after(self):
        """Test retryable error with retry_after."""
        exc = FlexRetryableError("Server busy", error_code="1009", retry_after=10.0)
        assert exc.retry_after == 10.0
        assert exc.error_code == "1009"
