#!/usr/bin/env python3
"""
Example 2: Get a Number and Receive SMS — full activation flow.

Usage:
    export SMSLLT_APIKEY="your..."
    python examples/02_get_number_and_sms.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from smsllt import SmslltClient
from smsllt.exceptions import NoNumberAvailableError, SmsNotReceivedError


def main():
    apikey = os.environ.get("SMSLLT_APIKEY")
    if not apikey:
        print("Please set SMSLLT_APIKEY environment variable")
        sys.exit(1)

    with SmslltClient(apikey=apikey) as client:
        # Configuration — adjust these!
        SERVICE_ID = 86        # Example: change to your target service ID
        COUNTRY_CODE = "JP"    # Country code

        print("=" * 50)
        print("📱 SMS Activation Flow")
        print("=" * 50)

        # Step 1: Get balance
        balance = client.get_balance()
        print(f"\n💰 Balance: ${balance:.2f}")

        # Step 2: Get a number
        print(f"\n🔢 Requesting number for service_id={SERVICE_ID} in {COUNTRY_CODE}...")
        try:
            result = client.get_number(service_id=SERVICE_ID, country_code=COUNTRY_CODE)
            request_id = result["request_id"]
            number = result["number"]
            print(f"   ✅ Got number: {number}")
            print(f"   📋 Request ID: {request_id}")
        except NoNumberAvailableError:
            print("   ❌ No numbers available for this service/country.")
            return

        # Step 3: Wait for SMS (with manual polling for demo)
        print(f"\n⏳ Waiting for SMS (polling every 3s, max 60s)...")
        try:
            sms = client.wait_for_sms(request_id, poll_interval=3, max_wait=60)
            sms_code = sms.get("sms_code", "???")
            print(f"   ✅ SMS received! Code: {sms_code}")
        except SmsNotReceivedError:
            print("   ⚠️ SMS not yet received (timeout)")

        # Step 4: Release the number
        print(f"\n🗑️  Releasing number...")
        client.release_number(request_id, status="finish")
        print("   ✅ Number released.")

        print("\n🎉 Flow complete!")


if __name__ == "__main__":
    main()