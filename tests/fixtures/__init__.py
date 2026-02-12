"""Test fixtures for IBKR Flex API responses."""


def create_send_request_success(reference_code: str = "12345678") -> str:
    """Generate successful SendRequest XML response."""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<FlexStatementResponse timestamp="30 January, 2026 12:00 PM EST">
  <Status>Success</Status>
  <ReferenceCode>{reference_code}</ReferenceCode>
  <Url>https://ndcdyn.interactivebrokers.com/AccountManagement/FlexWebService/GetStatement</Url>
</FlexStatementResponse>"""


def create_send_request_error(error_code: str = "1003", error_message: str = "Invalid query") -> str:
    """Generate error SendRequest XML response."""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<FlexStatementResponse timestamp="30 January, 2026 12:00 PM EST">
  <Status>Fail</Status>
  <ErrorCode>{error_code}</ErrorCode>
  <ErrorMessage>{error_message}</ErrorMessage>
</FlexStatementResponse>"""


def create_get_statement_success(account_id: str = "U1234567") -> str:
    """Generate successful GetStatement XML (flex report data)."""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<FlexQueryResponse queryName="TestReport" type="AF">
  <FlexStatements count="1">
    <FlexStatement accountId="{account_id}" fromDate="2026-01-01" toDate="2026-01-30">
      <AccountInformation accountId="{account_id}" currency="USD" name="Test Account"/>
      <Trades>
        <Trade accountId="{account_id}" symbol="AAPL" dateTime="2026-01-15;093000" quantity="100"/>
      </Trades>
    </FlexStatement>
  </FlexStatements>
</FlexQueryResponse>"""


def create_get_statement_error(error_code: str = "1019", error_message: str = "Statement generation in progress") -> str:
    """Generate error GetStatement XML response."""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<FlexStatementResponse timestamp="30 January, 2026 12:00 PM EST">
  <Status>Fail</Status>
  <ErrorCode>{error_code}</ErrorCode>
  <ErrorMessage>{error_message}</ErrorMessage>
</FlexStatementResponse>"""


# Common error responses for testing
SEND_REQUEST_SUCCESS = create_send_request_success()
SEND_REQUEST_INVALID_TOKEN = create_send_request_error("1015", "Invalid token")
SEND_REQUEST_TOKEN_EXPIRED = create_send_request_error("1012", "Token expired")
SEND_REQUEST_SERVER_BUSY = create_send_request_error("1009", "Server is busy, please try again later")
SEND_REQUEST_RATE_LIMITED = create_send_request_error("1018", "Too many requests")

GET_STATEMENT_SUCCESS = create_get_statement_success()
GET_STATEMENT_IN_PROGRESS = create_get_statement_error("1019", "Statement generation in progress")
GET_STATEMENT_SERVER_BUSY = create_get_statement_error("1009", "Server is busy")
