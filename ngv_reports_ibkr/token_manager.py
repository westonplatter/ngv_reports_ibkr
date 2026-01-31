"""
Token lifecycle management for IBKR Flex Web Service.

IBKR Flex tokens have a 6-hour lifetime from when they are issued.
This module provides tracking and notification capabilities for token expiry.

Note: Tokens cannot be programmatically refreshed - users must manually
generate new tokens via the IBKR Account Management portal.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Callable, Dict, Optional

from loguru import logger

from ngv_reports_ibkr.flex_client import FlexTokenExpiredError


# Type alias for notification callbacks
TokenExpiryCallback = Callable[[str, "TokenInfo"], None]


@dataclass
class TokenInfo:
    """
    Token metadata for lifecycle tracking.

    Attributes:
        token: The flex token string (masked in logs for security)
        account_id: Associated account identifier
        created_at: When the token was registered
        expires_at: When the token will expire
        ttl_hours: Token time-to-live in hours
    """

    token: str
    account_id: str
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime = field(init=False)
    ttl_hours: int = 6

    def __post_init__(self):
        """Calculate expiry time based on TTL."""
        self.expires_at = self.created_at + timedelta(hours=self.ttl_hours)

    @property
    def is_expired(self) -> bool:
        """Check if token has expired."""
        return datetime.now() >= self.expires_at

    @property
    def time_remaining(self) -> timedelta:
        """Get remaining time before expiry."""
        return self.expires_at - datetime.now()

    @property
    def minutes_remaining(self) -> float:
        """Get remaining time in minutes."""
        return self.time_remaining.total_seconds() / 60

    @property
    def is_expiring_soon(self) -> bool:
        """Check if token expires within 30 minutes."""
        return 0 < self.minutes_remaining <= 30

    @property
    def masked_token(self) -> str:
        """Return masked token for logging (show first/last 4 chars)."""
        if len(self.token) <= 8:
            return "****"
        return f"{self.token[:4]}...{self.token[-4:]}"

    def __repr__(self) -> str:
        """Safe representation without exposing full token."""
        return (
            f"TokenInfo(account_id={self.account_id!r}, "
            f"token={self.masked_token!r}, "
            f"minutes_remaining={self.minutes_remaining:.1f})"
        )


class TokenManager:
    """
    Manages IBKR Flex token lifecycle with expiry tracking and notifications.

    The TokenManager tracks when tokens were issued and provides:
    - Expiry checking before API calls
    - Warning notifications when tokens are expiring soon
    - Callback hooks for notifying users when action is needed

    Since IBKR tokens cannot be programmatically refreshed, this manager
    focuses on awareness and notification rather than automatic renewal.

    Example:
        >>> def notify_user(account_id: str, token_info: TokenInfo):
        ...     print(f"Token for {account_id} expires in {token_info.minutes_remaining:.0f} min!")
        ...
        >>> manager = TokenManager(on_expiring_soon=notify_user)
        >>> manager.register_token("my_token_123", "U1234567")
        >>> token = manager.get_valid_token("U1234567")  # Triggers callback if expiring soon
    """

    DEFAULT_TTL_HOURS = 6
    EXPIRY_WARNING_MINUTES = 30

    def __init__(
        self,
        ttl_hours: int = DEFAULT_TTL_HOURS,
        on_expiring_soon: Optional[TokenExpiryCallback] = None,
        on_expired: Optional[TokenExpiryCallback] = None,
    ):
        """
        Initialize token manager.

        Args:
            ttl_hours: Token time-to-live in hours (default: 6)
            on_expiring_soon: Callback when token has <30 min remaining
            on_expired: Callback when token has expired
        """
        self.ttl_hours = ttl_hours
        self.on_expiring_soon = on_expiring_soon
        self.on_expired = on_expired
        self._tokens: Dict[str, TokenInfo] = {}
        self._warned_expiring: set = set()  # Track which tokens we've warned about

    def register_token(self, token: str, account_id: str) -> TokenInfo:
        """
        Register a token with expiry tracking.

        Args:
            token: The flex token string
            account_id: Associated account ID

        Returns:
            TokenInfo with expiry metadata
        """
        token_info = TokenInfo(
            token=token,
            account_id=account_id,
            ttl_hours=self.ttl_hours,
        )
        self._tokens[account_id] = token_info
        self._warned_expiring.discard(account_id)

        logger.info(
            f"Registered token for account {account_id}, "
            f"expires at {token_info.expires_at.strftime('%Y-%m-%d %H:%M:%S')} "
            f"({self.ttl_hours} hours)"
        )
        return token_info

    def get_token_info(self, account_id: str) -> Optional[TokenInfo]:
        """
        Get token info for an account.

        Args:
            account_id: Account to lookup

        Returns:
            TokenInfo if found, None otherwise
        """
        return self._tokens.get(account_id)

    def get_valid_token(self, account_id: str) -> str:
        """
        Get a valid (non-expired) token for an account.

        This method:
        1. Checks if the token exists
        2. Checks if it has expired (triggers on_expired callback)
        3. Checks if it's expiring soon (triggers on_expiring_soon callback)

        Args:
            account_id: Account to lookup

        Returns:
            The token string if valid

        Raises:
            FlexTokenExpiredError: If token has expired or doesn't exist
        """
        token_info = self._tokens.get(account_id)

        if token_info is None:
            logger.error(f"No token found for account {account_id}")
            raise FlexTokenExpiredError(f"No token registered for account {account_id}")

        if token_info.is_expired:
            logger.error(
                f"Token for account {account_id} expired "
                f"{-token_info.minutes_remaining:.1f} minutes ago"
            )
            if self.on_expired:
                self.on_expired(account_id, token_info)
            raise FlexTokenExpiredError(
                f"Token for account {account_id} expired at "
                f"{token_info.expires_at.strftime('%Y-%m-%d %H:%M:%S')}"
            )

        if token_info.is_expiring_soon and account_id not in self._warned_expiring:
            logger.warning(
                f"Token for account {account_id} expiring soon: "
                f"{token_info.minutes_remaining:.1f} minutes remaining"
            )
            self._warned_expiring.add(account_id)
            if self.on_expiring_soon:
                self.on_expiring_soon(account_id, token_info)

        logger.debug(
            f"Token for account {account_id} valid, "
            f"{token_info.minutes_remaining:.1f} minutes remaining"
        )
        return token_info.token

    def is_token_valid(self, account_id: str) -> bool:
        """
        Check if account has a valid (non-expired) token.

        Args:
            account_id: Account to check

        Returns:
            True if token exists and is not expired
        """
        token_info = self._tokens.get(account_id)
        return token_info is not None and not token_info.is_expired

    def is_token_expiring_soon(self, account_id: str) -> bool:
        """
        Check if token is expiring within 30 minutes.

        Args:
            account_id: Account to check

        Returns:
            True if token exists and expires within 30 minutes
        """
        token_info = self._tokens.get(account_id)
        return token_info is not None and token_info.is_expiring_soon

    def remove_token(self, account_id: str) -> bool:
        """
        Remove a token from tracking.

        Args:
            account_id: Account to remove

        Returns:
            True if token was removed, False if not found
        """
        if account_id in self._tokens:
            del self._tokens[account_id]
            self._warned_expiring.discard(account_id)
            logger.info(f"Removed token for account {account_id}")
            return True
        return False

    def clear_all(self) -> int:
        """
        Remove all tracked tokens.

        Returns:
            Number of tokens removed
        """
        count = len(self._tokens)
        self._tokens.clear()
        self._warned_expiring.clear()
        logger.info(f"Cleared {count} tokens from manager")
        return count

    def get_all_accounts(self) -> list:
        """
        Get list of all registered account IDs.

        Returns:
            List of account IDs
        """
        return list(self._tokens.keys())

    def get_status_report(self) -> Dict[str, dict]:
        """
        Get status report for all tracked tokens.

        Returns:
            Dict mapping account_id to status info
        """
        report = {}
        for account_id, token_info in self._tokens.items():
            report[account_id] = {
                "is_valid": not token_info.is_expired,
                "is_expiring_soon": token_info.is_expiring_soon,
                "minutes_remaining": token_info.minutes_remaining,
                "expires_at": token_info.expires_at.isoformat(),
                "created_at": token_info.created_at.isoformat(),
            }
        return report
