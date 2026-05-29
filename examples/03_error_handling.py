#!/usr/bin/env python3
"""
Example 3: Error Handling — demonstrate all exception types and how to catch them.

Usage:
    export SMSLLT_APIKEY=***    python examples/03_error_handling.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from smsllt import SmslltClient
from smsllt.exceptions import (
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


def demo_error_scenarios(apikey: str):
    """Demonstrate various error scenarios and their handling."""
    client = SmslltClient(apikey=apikey)

    # ── 1. Invalid auth ─────────────────────────────
    print("1️⃣  Testing invalid authentication...")
    try:
        bad_client = SmslltClient(apikey="invalid-key-12345")
        bad_client.get_balance()
    except AuthenticationError as e:
        print(f"   ✅ Correctly caught AuthenticationError: {e}")
    except SmslltError as e:
        print(f"   ⚠️ Caught generic error (server may respond differently): {e}")

    # ── 2. Invalid parameters ───────────────────────
    print("\n2️⃣  Testing invalid parameters...")
    try:
        client.get_services(country_code="INVALID_COUNTRY_CODE_XYZ")
        print("   ⚠️ No error — server accepted invalid country code")
    except SmslltError as e:
        print(f"   ✅ Caught: {type(e).__name__}: {e}")

    # ── 3. Non-existent service ─────────────────────
    print("\n3️⃣  Testing non-existent service...")
    try:
        client.get_number(service_id=99999, country_code="JP")
        print("   ⚠️ Unexpectedly got a number for service_id=99999")
    except NoNumberAvailableError as e:
        print(f"   ✅ Caught NoNumberAvailableError: {e}")
    except SmslltError as e:
        print(f"   ⚠️ Caught: {type(e).__name__}: {e}")

    # ── 4. SMS not received yet ─────────────────────
    print("\n4️⃣  Testing SMS not received (invalid request_id)...")
    try:
        client.get_sms(request_id="nonexistent-12345")
    except SmsNotReceivedError as e:
        print(f"   ✅ Caught SmsNotReceivedError: {e}")
    except SmslltError as e:
        print(f"   ⚠️ Caught: {type(e).__name__}: {e}")

    # ── 5. Release invalid request ──────────────────
    print("\n5️⃣  Testing release on invalid request_id...")
    try:
        client.release_number(request_id="nonexistent-12345")
        print("   ⚠️ No error — server accepted")
    except SmslltError as e:
        print(f"   ✅ Caught: {type(e).__name__}: {e}")

    # ── 6. Catch-all pattern ────────────────────────
    print("\n6️⃣  Demonstrating catch-all error handling pattern:")
    print("""
    try:
        result = client.get_number(service_id=86, country_code="JP")
        sms = client.wait_for_sms(result["request_id"])
        print(f"Code: {sms['sms_code']}")
    except NoNumberAvailableError:
        print("No numbers available — try another country or service")
    except SmsNotReceivedError:
        print("SMS not received in time")
    except InsufficientBalanceError:
        print("Balance too low — please top up")
    except AuthenticationError:
        print("Invalid API key")
    except RateLimitError:
        print("Too many requests — slow down")
    except SmslltError as e:
        print(f"API error: {e}")
    finally:
        if 'result' in locals():
            client.release_number(result['request_id'])
    """)

    client.close()


def main():
    apikey = os.environ.get("SMSLLT_APIKEY")
    if not apikey:
        print("⚠️  SMSLLT_APIKEY not set. Running demo with fake key to show error patterns.")
        print("   Set it for real API interaction: export SMSLLT_APIKEY='***'\n")
        apikey = "demo-fake-key"

    demo_error_scenarios(apikey)
    print("\n✅ Error handling demo complete!")


if __name__ == "__main__":
    main()