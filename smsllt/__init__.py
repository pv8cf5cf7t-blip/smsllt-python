"""
smsllt Python SDK
~~~~~~~~~~~~~~~~~

Python SDK for smsllt.com SMS verification API.
Full type-annotated client with retry, rate limiting, and comprehensive error handling.

Basic usage::

    from smsllt import SmslltClient

    client = SmslltClient(apikey="your-api-key")

    # Get balance
    balance = client.get_balance()

    # Get available countries
    countries = client.get_countries()

    # Get services and pricing
    services = client.get_services(country_code="JP")

    # Get a phone number
    result = client.get_number(service_id=86, country_code="JP")
    request_id = result["request_id"]
    phone = result["number"]

    # Wait for SMS
    sms = client.get_sms(request_id)

    # Release the number
    client.release_number(request_id)
"""

from __future__ import annotations

import logging
import platform
import time
from typing import Any, Dict, List, Optional, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import (
    AuthenticationError,
    InsufficientBalanceError,
    InvalidParameterError,
    NetworkError,
    NoNumberAvailableError,
    RateLimitError,
    RequestTimeoutError,
    ServerError,
    SmslltError,
    SmsNotReceivedError,
)

__version__ = "1.0.0"
__author__ = "smsllt-sdk contributors"
__all__ = ["SmslltClient"]

logger = logging.getLogger("smsllt")

# ──────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────

DEFAULT_BASE_URL = "https://smsllt.com"
DEFAULT_TIMEOUT = 30  # seconds
DEFAULT_RETRIES = 3
DEFAULT_RATE_LIMIT_INTERVAL = 0.5  # seconds between requests

_T = Dict[str, Any]


def _map_status_code(status_code: int, message: str) -> SmslltError:
    """Map HTTP status codes to appropriate exception classes."""
    if status_code == 401 or status_code == 403:
        return AuthenticationError(message, status_code)
    elif status_code == 429:
        return RateLimitError(message, status_code)
    elif 400 <= status_code < 500:
        if "balance" in message.lower() or "insufficient" in message.lower():
            return InsufficientBalanceError(message, status_code)
        return InvalidParameterError(message, status_code)
    elif 500 <= status_code < 600:
        return ServerError(message, status_code)
    return SmslltError(message, status_code)


class SmslltClient:
    """Client for the smsllt.com SMS verification API.

    Provides full access to all smsllt.com API endpoints including
    balance queries, country/service lookups, number provisioning,
    SMS retrieval, bulk SMS, and account management.

    Args:
        apikey: Your smsllt.com API key (found in account settings).
        base_url: Override the base URL (default: https://smsllt.com).
        timeout: Request timeout in seconds (default: 30).
        retries: Number of retries on connection errors (default: 3).
        rate_limit_interval: Seconds between requests for rate limiting (default: 0.5).
        session: Optional pre-configured requests.Session.

    Example::

        client = SmslltClient(apikey="your-key")
        balance = client.get_balance()
    """

    def __init__(
        self,
        apikey: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
        rate_limit_interval: float = DEFAULT_RATE_LIMIT_INTERVAL,
        session: Optional[requests.Session] = None,
    ) -> None:
        if not apikey:
            raise ValueError("apikey is required. Find it in your smsllt.com account settings.")

        self.apikey = apikey
        self.username = username
        self.password = password
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.rate_limit_interval = rate_limit_interval
        self._last_request_time: float = 0.0

        # Auth token (populated by login())
        self._token: Optional[str] = None

        # Session setup with retry
        if session is None:
            self._session = requests.Session()
            retry_strategy = Retry(
                total=retries,
                backoff_factor=0.5,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["GET"],
                raise_on_status=False,
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            self._session.mount("https://", adapter)
            self._session.mount("http://", adapter)
        else:
            self._session = session

        self._session.headers.update({
            "User-Agent": f"smsllt-python/{__version__} ({platform.system()} {platform.machine()})",
        })

    # ──────────────────────────────────────────────────────────────
    # Internal helpers
    # ──────────────────────────────────────────────────────────────

    def _rate_limit(self) -> None:
        """Enforce minimum interval between API calls."""
        elapsed = time.monotonic() - self._last_request_time
        if elapsed < self.rate_limit_interval:
            time.sleep(self.rate_limit_interval - elapsed)

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        use_token: bool = False,
    ) -> _T:
        """Execute an HTTP request with error handling.

        Args:
            method: HTTP method (GET/POST).
            path: API path relative to base_url.
            params: Query parameters.
            json_data: JSON body for POST requests.
            use_token: Whether to use Bearer token auth instead of apikey.

        Returns:
            Parsed JSON response as dict.

        Raises:
            SmslltError: On API or network errors.
        """
        self._rate_limit()

        url = f"{self.base_url}{path}"
        headers: Dict[str, str] = {}

        if use_token and self._token:
            headers["Authorization"] = f"Bearer {self._token}"
            headers["Content-Type"] = "application/json"
        elif json_data is not None:
            headers["Content-Type"] = "application/json"

        # Merge apikey into params for GET requests
        if params is None:
            params = {}
        if not use_token:
            params["apikey"] = self.apikey

        logger.debug("%s %s params=%s", method, url, params)

        try:
            if method.upper() == "GET":
                resp = self._session.get(
                    url, params=params, timeout=self.timeout, headers=headers
                )
            elif method.upper() == "POST":
                resp = self._session.post(
                    url, params=params, json=json_data, timeout=self.timeout, headers=headers
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            self._last_request_time = time.monotonic()

        except requests.exceptions.Timeout:
            raise RequestTimeoutError(f"Request timed out after {self.timeout}s")
        except requests.exceptions.ConnectionError as e:
            raise NetworkError(f"Connection error: {e}")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Request failed: {e}")

        # Handle HTTP errors
        if not resp.ok:
            error_msg = resp.text[:500] if resp.text else "Unknown error"
            raise _map_status_code(resp.status_code, error_msg)

        # Try JSON parse
        try:
            data: _T = resp.json()
        except ValueError:
            # Some endpoints may return plain text
            return {"raw": resp.text}  # type: ignore[return-value]

        # Check for API-level errors
        if isinstance(data, dict):
            if data.get("code") and data.get("code") != 0 and data.get("code") != 200:
                msg = data.get("msg", data.get("message", "API error"))
                if data["code"] == 401:
                    raise AuthenticationError(msg)
                raise SmslltError(msg)
            # Some responses have a "success" field
            if "success" in data and data["success"] is False:
                msg = data.get("message", data.get("msg", "Request failed"))
                raise SmslltError(msg)

        return data

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> _T:
        """Convenience for GET requests."""
        return self._request("GET", path, params=params)

    def _post(self, path: str, params: Optional[Dict[str, Any]] = None,
              json_data: Optional[Dict[str, Any]] = None) -> _T:
        """Convenience for POST requests."""
        return self._request("POST", path, params=params, json_data=json_data)

    # ──────────────────────────────────────────────────────────────
    # Account & Authentication
    # ──────────────────────────────────────────────────────────────

    def login(self) -> Dict[str, Any]:
        """Log in with username/password to obtain a Bearer token.

        Requires ``username`` and ``password`` to be provided at client init.
        After login, the token is stored internally and used for
        payment-related endpoints.

        Returns:
            dict with keys: ``token``, ``user`` (contains ``apikey``).

        Raises:
            ValueError: If username/password not provided.
            AuthenticationError: If credentials are invalid.
        """
        if not self.username or not self.password:
            raise ValueError(
                "username and password are required for login(). "
                "Provide them when creating SmslltClient."
            )
        data = self._post(
            "/api/auth/login",
            json_data={"username": self.username, "password": self.password},
        )
        self._token = data.get("token")
        return data

    def get_balance(self) -> float:
        """Get current account balance.

        Returns:
            Account balance as a float (in USD).

        Example::

            balance = client.get_balance()
            print(f"Balance: ${balance:.2f}")
        """
        data = self._get("/v2/api/getBalance")
        # Response may be {"balance": "12.50"} or just a number
        if isinstance(data, dict):
            balance = data.get("balance", data.get("data", 0))
        else:
            balance = data
        return float(balance)

    # ──────────────────────────────────────────────────────────────
    # Countries & Services
    # ──────────────────────────────────────────────────────────────

    def get_countries(self) -> List[Dict[str, Any]]:
        """Get list of supported countries.

        Returns:
            List of country dicts, each with keys like ``country_code``, ``name``, etc.

        Example::

            for c in client.get_countries():
                print(c["country_code"], c.get("name"))
        """
        data = self._get("/v2/api/countries")
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return data.get("data", data.get("countries", []))
        return []

    def get_services(
        self,
        country_code: Optional[str] = None,
        query: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> Dict[str, Any]:
        """Get available services and their pricing.

        Args:
            country_code: Filter by country code (e.g., "JP", "US").
            query: Search keyword for service name.
            page: Page number for pagination.
            page_size: Number of results per page.

        Returns:
            dict with keys like ``services``, ``total``, ``page``, etc.
            Each service has ``service_id``, ``name``, ``price``, and more.

        Example::

            services = client.get_services(country_code="JP")
            for svc in services.get("data", services.get("services", [])):
                print(f"{svc['name']}: ${svc['price']}")
        """
        params: Dict[str, Any] = {"page": page, "page_size": page_size}
        if country_code:
            params["country_code"] = country_code
        if query:
            params["q"] = query

        return self._get("/v2/api/getServices", params=params)

    # ──────────────────────────────────────────────────────────────
    # Number Management
    # ──────────────────────────────────────────────────────────────

    def get_number(
        self,
        service_id: Union[int, str],
        country_code: str,
    ) -> Dict[str, Any]:
        """Request a phone number for the specified service and country.

        Args:
            service_id: Service ID from get_services().
            country_code: Country code (e.g., "JP", "US", "HK").

        Returns:
            dict with ``request_id`` (activation ID) and ``number`` (phone number).

        Raises:
            NoNumberAvailableError: If no numbers available.
            InsufficientBalanceError: If balance too low.

        Example::

            result = client.get_number(service_id=86, country_code="JP")
            print(f"Number: {result['number']} | ID: {result['request_id']}")
        """
        data = self._get("/v2/api/getNumber", params={
            "service_id": service_id,
            "country_code": country_code,
        })
        if not data or (isinstance(data, dict) and not data.get("request_id")):
            raise NoNumberAvailableError(
                f"No numbers available for service_id={service_id}, country_code={country_code}"
            )
        return data

    def get_sms(self, request_id: Union[str, int]) -> Dict[str, Any]:
        """Retrieve SMS code for a given activation.

        If the SMS has not arrived yet, the response will contain a "wait"
        status. You should poll this endpoint periodically.

        Args:
            request_id: The activation request ID from get_number().

        Returns:
            dict with ``sms_code`` (the verification code) when received,
            or status information if still waiting.

        Raises:
            SmsNotReceivedError: If SMS has not been received yet.

        Example::

            import time
            for _ in range(30):
                try:
                    sms = client.get_sms(request_id)
                    print(f"Code: {sms['sms_code']}")
                    break
                except SmsNotReceivedError:
                    time.sleep(2)
        """
        data = self._get("/v2/api/getSms", params={"request_id": request_id})
        # Check for "wait" status
        if isinstance(data, dict):
            sms_code = data.get("sms_code")
            if sms_code is None or sms_code == "" or sms_code == "wait":
                raise SmsNotReceivedError(
                    f"SMS not yet received for request_id={request_id}",
                )
        return data

    def wait_for_sms(
        self,
        request_id: Union[str, int],
        poll_interval: float = 3.0,
        max_wait: float = 180.0,
    ) -> Dict[str, Any]:
        """Poll for SMS until received or timeout.

        Convenience method that repeatedly calls get_sms().

        Args:
            request_id: The activation request ID.
            poll_interval: Seconds between polls (default: 3).
            max_wait: Maximum total wait time in seconds (default: 180).

        Returns:
            dict with ``sms_code``.

        Raises:
            RequestTimeoutError: If SMS not received within max_wait.
        """
        deadline = time.monotonic() + max_wait
        while time.monotonic() < deadline:
            try:
                return self.get_sms(request_id)
            except SmsNotReceivedError:
                time.sleep(poll_interval)
        raise RequestTimeoutError(
            f"SMS not received for request_id={request_id} within {max_wait}s"
        )

    def release_number(
        self, request_id: Union[str, int], status: str = "reject"
    ) -> Dict[str, Any]:
        """Release/blacklist a phone number.

        Call this when you no longer need the number or the activation failed.

        Args:
            request_id: The activation request ID.
            status: Either "reject" (blacklist) or "finish" (mark as complete).

        Returns:
            API response dict.

        Example::

            client.release_number(request_id)
            client.release_number(request_id, status="finish")
        """
        return self._get("/v2/api/setStatus", params={
            "request_id": request_id,
            "status": status,
        })

    def get_again_number(self, request_id: Union[str, int]) -> Dict[str, Any]:
        """Re-activate / get another SMS for an existing request.

        Args:
            request_id: The activation request ID.

        Returns:
            API response dict.
        """
        return self._get("/v2/api/getAgainNmuber", params={"request_id": request_id})

    # ──────────────────────────────────────────────────────────────
    # History
    # ──────────────────────────────────────────────────────────────

    def sms_history(
        self,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Get SMS activation history.

        Args:
            page: Page number.
            page_size: Results per page.

        Returns:
            dict with history records.
        """
        return self._get("/v2/api/smsHistory", params={
            "page": page,
            "page_size": page_size,
        })

    # ──────────────────────────────────────────────────────────────
    # Keyword-based SMS (通用短信)
    # ──────────────────────────────────────────────────────────────

    def get_keyword_number(
        self,
        phone: str,
        card_type: Optional[str] = None,
        dedupe: bool = True,
    ) -> Dict[str, Any]:
        """Get a number using keyword-based SMS (通用短信取号).

        Args:
            phone: Phone number for receiving SMS.
            card_type: Optional card type filter.
            dedupe: Whether to deduplicate.

        Returns:
            API response dict.
        """
        params: Dict[str, Any] = {"phone": phone}
        if card_type:
            params["cardType"] = card_type
        if not dedupe:
            params["dedupe"] = "0"
        return self._get("/v2/api/getKeywordNumber", params=params)

    def get_keyword_sms(self, phone: str, keyword: str) -> Dict[str, Any]:
        """Fetch SMS by keyword filter.

        Args:
            phone: Phone number.
            keyword: Keyword to filter SMS content.

        Returns:
            dict with matching SMS content.
        """
        return self._get("/v2/api/getKeywordSms", params={
            "phone": phone,
            "keyword": keyword,
        })

    def del_keyword_number(self, phone: str) -> Dict[str, Any]:
        """Release a keyword-based number.

        Args:
            phone: Phone number to release.

        Returns:
            API response dict.
        """
        return self._get("/v2/api/delKeywordNumber", params={"phone": phone})

    def keyword_sms_history(self, page: int = 1) -> Dict[str, Any]:
        """Get keyword SMS history.

        Args:
            page: Page number.

        Returns:
            dict with history records.
        """
        return self._get("/v2/api/keywordSmsHistory", params={"page": page})

    # ──────────────────────────────────────────────────────────────
    # Bulk SMS
    # ──────────────────────────────────────────────────────────────

    def bulk_sms(
        self,
        tel_list: List[str],
        text: str,
        msg_type: Optional[str] = None,
        sender: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send bulk SMS messages.

        Args:
            tel_list: List of phone numbers (comma-separated string also accepted).
            text: SMS content.
            msg_type: Optional message type identifier.
            sender: Optional sender ID.

        Returns:
            API response dict.

        Example::

            client.bulk_sms(
                tel_list=["+8613800138000", "+8613800138001"],
                text="Your verification code: 123456",
            )
        """
        params: Dict[str, Any] = {
            "tel_list": tel_list if isinstance(tel_list, str) else ",".join(tel_list),
            "text": text,
        }
        if msg_type:
            params["type"] = msg_type
        if sender:
            params["from"] = sender

        return self._get("/v2/api/bulksms", params=params)

    # ──────────────────────────────────────────────────────────────
    # Payments (requires login)
    # ──────────────────────────────────────────────────────────────

    def make_payment(
        self,
        amount: float,
        method: str = "TRC20 USDT",
    ) -> Dict[str, Any]:
        """Create a payment/recharge request.

        Requires prior login() call.

        Args:
            amount: Payment amount in USD.
            method: Payment method (default: "TRC20 USDT").

        Returns:
            Payment response dict.
        """
        if not self._token:
            raise AuthenticationError(
                "Not authenticated. Call login() first with username/password."
            )
        return self._post(
            "/api/payments",
            json_data={"amount": amount, "method": method},
            use_token=True,
        )

    # ──────────────────────────────────────────────────────────────
    # Utility
    # ──────────────────────────────────────────────────────────────

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._session.close()

    def __enter__(self) -> "SmslltClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def __repr__(self) -> str:
        return (
            f"SmslltClient(base_url={self.base_url!r}, "
            f"authenticated={bool(self._token)})"
        )


# ──────────────────────────────────────────────────────────────────
# Convenience function
# ──────────────────────────────────────────────────────────────────

def wait_for_sms(
    client: SmslltClient,
    request_id: Union[str, int],
    poll_interval: float = 3.0,
    max_wait: float = 180.0,
) -> Dict[str, Any]:
    """Standalone helper to wait for an SMS code.

    Equivalent to ``client.wait_for_sms(request_id, poll_interval, max_wait)``.

    Args:
        client: An initialized SmslltClient.
        request_id: Activation request ID.
        poll_interval: Seconds between polls.
        max_wait: Maximum wait time.

    Returns:
        dict with ``sms_code``.
    """
    return client.wait_for_sms(request_id, poll_interval, max_wait)