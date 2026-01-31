"""Tests for token_manager module."""

from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from ngv_reports_ibkr.flex_client import FlexTokenExpiredError
from ngv_reports_ibkr.token_manager import TokenInfo, TokenManager


class TestTokenInfo:
    """Tests for TokenInfo dataclass."""

    def test_token_creation(self):
        """Test creating TokenInfo."""
        token = TokenInfo(token="abc123", account_id="U1234567")
        assert token.token == "abc123"
        assert token.account_id == "U1234567"
        assert token.ttl_hours == 6

    def test_token_expiry_calculation(self):
        """Test that expires_at is calculated correctly."""
        token = TokenInfo(token="abc123", account_id="U1234567", ttl_hours=6)
        expected_expiry = token.created_at + timedelta(hours=6)
        assert token.expires_at == expected_expiry

    def test_token_is_not_expired_when_fresh(self):
        """Test fresh token is not expired."""
        token = TokenInfo(token="abc123", account_id="U1234567")
        assert not token.is_expired

    def test_token_is_expired(self):
        """Test expired token detection."""
        # Create token that was created 7 hours ago
        old_time = datetime.now() - timedelta(hours=7)
        token = TokenInfo(
            token="abc123",
            account_id="U1234567",
            created_at=old_time,
            ttl_hours=6,
        )
        assert token.is_expired

    def test_token_time_remaining(self):
        """Test time remaining calculation."""
        token = TokenInfo(token="abc123", account_id="U1234567", ttl_hours=6)
        # Should be approximately 6 hours (minus tiny test execution time)
        assert token.time_remaining.total_seconds() > 5.9 * 3600

    def test_token_minutes_remaining(self):
        """Test minutes remaining property."""
        token = TokenInfo(token="abc123", account_id="U1234567", ttl_hours=1)
        # Should be approximately 60 minutes
        assert 59 < token.minutes_remaining <= 60

    def test_token_is_expiring_soon_when_near_expiry(self):
        """Test is_expiring_soon when within 30 minutes of expiry."""
        # Create token that expires in 20 minutes
        old_time = datetime.now() - timedelta(hours=5, minutes=40)
        token = TokenInfo(
            token="abc123",
            account_id="U1234567",
            created_at=old_time,
            ttl_hours=6,
        )
        assert token.is_expiring_soon

    def test_token_not_expiring_soon_when_fresh(self):
        """Test is_expiring_soon returns False when plenty of time left."""
        token = TokenInfo(token="abc123", account_id="U1234567", ttl_hours=6)
        assert not token.is_expiring_soon

    def test_token_masked_token(self):
        """Test token masking for logs."""
        token = TokenInfo(token="abcdefghijklmnop", account_id="U1234567")
        assert token.masked_token == "abcd...mnop"

    def test_token_masked_short_token(self):
        """Test masking of short token."""
        token = TokenInfo(token="short", account_id="U1234567")
        assert token.masked_token == "****"

    def test_token_repr_does_not_expose_token(self):
        """Test __repr__ doesn't expose full token."""
        token = TokenInfo(token="secrettoken12345", account_id="U1234567")
        repr_str = repr(token)
        assert "secrettoken12345" not in repr_str
        assert "secr...2345" in repr_str


class TestTokenManager:
    """Tests for TokenManager."""

    @pytest.fixture
    def manager(self):
        """Create TokenManager for testing."""
        return TokenManager(ttl_hours=6)

    def test_register_token(self, manager):
        """Test registering a token."""
        token_info = manager.register_token("mytoken123", "U1234567")
        assert token_info.token == "mytoken123"
        assert token_info.account_id == "U1234567"

    def test_get_token_info(self, manager):
        """Test getting token info."""
        manager.register_token("mytoken123", "U1234567")
        token_info = manager.get_token_info("U1234567")
        assert token_info is not None
        assert token_info.token == "mytoken123"

    def test_get_token_info_not_found(self, manager):
        """Test getting token info for nonexistent account."""
        token_info = manager.get_token_info("NONEXISTENT")
        assert token_info is None

    def test_get_valid_token(self, manager):
        """Test getting valid token."""
        manager.register_token("mytoken123", "U1234567")
        token = manager.get_valid_token("U1234567")
        assert token == "mytoken123"

    def test_get_valid_token_raises_for_nonexistent(self, manager):
        """Test get_valid_token raises for nonexistent account."""
        with pytest.raises(FlexTokenExpiredError, match="No token registered"):
            manager.get_valid_token("NONEXISTENT")

    def test_get_valid_token_raises_for_expired(self, manager):
        """Test get_valid_token raises for expired token."""
        # Register then manually expire
        manager.register_token("mytoken123", "U1234567")
        # Manually set created_at to 7 hours ago
        manager._tokens["U1234567"].created_at = datetime.now() - timedelta(hours=7)
        manager._tokens["U1234567"].expires_at = datetime.now() - timedelta(hours=1)

        with pytest.raises(FlexTokenExpiredError, match="expired"):
            manager.get_valid_token("U1234567")

    def test_is_token_valid(self, manager):
        """Test is_token_valid."""
        manager.register_token("mytoken123", "U1234567")
        assert manager.is_token_valid("U1234567")
        assert not manager.is_token_valid("NONEXISTENT")

    def test_is_token_expiring_soon(self, manager):
        """Test is_token_expiring_soon."""
        manager.register_token("mytoken123", "U1234567")
        # Fresh token should not be expiring soon
        assert not manager.is_token_expiring_soon("U1234567")

        # Manually set to expire in 20 minutes
        manager._tokens["U1234567"].expires_at = datetime.now() + timedelta(minutes=20)
        assert manager.is_token_expiring_soon("U1234567")

    def test_remove_token(self, manager):
        """Test removing a token."""
        manager.register_token("mytoken123", "U1234567")
        assert manager.is_token_valid("U1234567")

        result = manager.remove_token("U1234567")
        assert result is True
        assert not manager.is_token_valid("U1234567")

    def test_remove_token_nonexistent(self, manager):
        """Test removing nonexistent token."""
        result = manager.remove_token("NONEXISTENT")
        assert result is False

    def test_clear_all(self, manager):
        """Test clearing all tokens."""
        manager.register_token("token1", "U1111111")
        manager.register_token("token2", "U2222222")
        manager.register_token("token3", "U3333333")

        count = manager.clear_all()
        assert count == 3
        assert len(manager.get_all_accounts()) == 0

    def test_get_all_accounts(self, manager):
        """Test getting all accounts."""
        manager.register_token("token1", "U1111111")
        manager.register_token("token2", "U2222222")

        accounts = manager.get_all_accounts()
        assert len(accounts) == 2
        assert "U1111111" in accounts
        assert "U2222222" in accounts

    def test_get_status_report(self, manager):
        """Test getting status report."""
        manager.register_token("token1", "U1111111")

        report = manager.get_status_report()
        assert "U1111111" in report
        assert report["U1111111"]["is_valid"] is True
        assert report["U1111111"]["is_expiring_soon"] is False
        assert "minutes_remaining" in report["U1111111"]
        assert "expires_at" in report["U1111111"]


class TestTokenManagerCallbacks:
    """Tests for TokenManager callback functionality."""

    def test_on_expiring_soon_callback(self):
        """Test on_expiring_soon callback is triggered."""
        callback = Mock()
        manager = TokenManager(ttl_hours=6, on_expiring_soon=callback)

        manager.register_token("mytoken123", "U1234567")
        # Set to expire in 20 minutes
        manager._tokens["U1234567"].expires_at = datetime.now() + timedelta(minutes=20)

        # First call should trigger callback
        manager.get_valid_token("U1234567")
        callback.assert_called_once()

        # Get the call arguments
        call_args = callback.call_args[0]
        assert call_args[0] == "U1234567"
        assert call_args[1].token == "mytoken123"

    def test_on_expiring_soon_callback_only_once(self):
        """Test on_expiring_soon callback is only triggered once per token."""
        callback = Mock()
        manager = TokenManager(ttl_hours=6, on_expiring_soon=callback)

        manager.register_token("mytoken123", "U1234567")
        manager._tokens["U1234567"].expires_at = datetime.now() + timedelta(minutes=20)

        # Multiple calls should only trigger once
        manager.get_valid_token("U1234567")
        manager.get_valid_token("U1234567")
        manager.get_valid_token("U1234567")

        assert callback.call_count == 1

    def test_on_expiring_soon_resets_on_new_token(self):
        """Test callback resets when new token is registered."""
        callback = Mock()
        manager = TokenManager(ttl_hours=6, on_expiring_soon=callback)

        # First token
        manager.register_token("mytoken1", "U1234567")
        manager._tokens["U1234567"].expires_at = datetime.now() + timedelta(minutes=20)
        manager.get_valid_token("U1234567")

        # Re-register with new token
        manager.register_token("mytoken2", "U1234567")
        manager._tokens["U1234567"].expires_at = datetime.now() + timedelta(minutes=20)
        manager.get_valid_token("U1234567")

        # Should have been called twice
        assert callback.call_count == 2

    def test_on_expired_callback(self):
        """Test on_expired callback is triggered."""
        callback = Mock()
        manager = TokenManager(ttl_hours=6, on_expired=callback)

        manager.register_token("mytoken123", "U1234567")
        # Set to already expired
        manager._tokens["U1234567"].expires_at = datetime.now() - timedelta(hours=1)

        with pytest.raises(FlexTokenExpiredError):
            manager.get_valid_token("U1234567")

        callback.assert_called_once()
        call_args = callback.call_args[0]
        assert call_args[0] == "U1234567"

    def test_no_callback_when_not_set(self):
        """Test no errors when callbacks are not set."""
        manager = TokenManager(ttl_hours=6)

        manager.register_token("mytoken123", "U1234567")
        manager._tokens["U1234567"].expires_at = datetime.now() + timedelta(minutes=20)

        # Should work without callbacks
        token = manager.get_valid_token("U1234567")
        assert token == "mytoken123"
