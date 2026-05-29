#!/usr/bin/env python3
"""
Example 4: Login and Payments — authenticate and make a payment.

Usage:
    export SMSLLT_APIKEY=***    SMSLLT_USERNAME=*** SMSLLT_PASSWORD=***    python examples/04_login_and_payment.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from smsllt import SmslltClient
from smsllt.exceptions import AuthenticationError


def main():
    apikey = os.environ.get("SMSLLT_APIKEY")
    username = os.environ.get("SMSLLT_USERNAME")
    password = os.environ.get("SMSLLT_PASSWORD")

    if not all([apikey, username, password]):
        print("Please set all required environment variables:")
        print("  export SMSLLT_APIKEY='***'")
        print("  export SMSLLT_USERNAME='***'")
        print("  export SMSLLT_PASSWORD='***'")
        sys.exit(1)

    client = SmslltClient(
        apikey=apikey,
        username=username,
        password=password,
    )

    print("=" * 50)
    print("🔐 Login & Payment Demo")
    print("=" * 50)

    # ── Login ────────────────────────────────────────
    print("\n1️⃣  Logging in...")
    try:
        user_data = client.login()
        user = user_data.get("user", {})
        print(f"   ✅ Logged in as: {user.get('username', 'unknown')}")
        print(f"   📧 Email: {user.get('email', 'N/A')}")
        print(f"   🔑 API Key: {user.get('apikey', 'N/A')[:20]}...")
        print(f"   🔐 Token: {user_data.get('token', '')[:30]}...")
    except AuthenticationError as e:
        print(f"   ❌ Authentication failed: {e}")
        client.close()
        return

    # ── Balance before ───────────────────────────────
    print("\n2️⃣  Current balance:")
    balance = client.get_balance()
    print(f"   💰 ${balance:.2f}")

    # ── Create payment (example — comment out to avoid real charge) ──
    print("\n3️⃣  Creating payment (SKIPPED — uncomment code to execute):")
    print("""
    # ⚠️ Uncomment below to actually create a payment:
    #
    # try:
    #     payment = client.make_payment(amount=10.0, method="TRC20 USDT")
    #     print(f"   ✅ Payment created:")
    #     print(f"      Amount: ${payment.get('amount')}")
    #     print(f"      Method: {payment.get('method')}")
    # except SmslltError as e:
    #     print(f"   ❌ Payment failed: {e}")
    """)

    # ── History ──────────────────────────────────────
    print("\n4️⃣  Recent activation history:")
    try:
        history = client.sms_history(page=1, page_size=5)
        records = history.get("data", history.get("records", history.get("list", [])))
        if records:
            for r in records[:5]:
                rid = r.get("request_id", r.get("id", "?"))
                num = r.get("number", r.get("phone", "?"))
                svc = r.get("service", r.get("service_name", "?"))
                print(f"   [{rid}] {num} — {svc}")
        else:
            print("   (no history)")
    except Exception as e:
        print(f"   ⚠️ Could not fetch history: {e}")

    client.close()
    print("\n✅ Login demo complete!")


if __name__ == "__main__":
    main()