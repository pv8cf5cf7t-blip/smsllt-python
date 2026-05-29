#!/usr/bin/env python3
"""
Example 5: Bulk SMS & Keyword SMS — advanced API features.

Usage:
    export SMSLLT_APIKEY=***    python examples/05_bulk_and_keyword.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from smsllt import SmslltClient
from smsllt.exceptions import SmslltError


def main():
    apikey = os.environ.get("SMSLLT_APIKEY")
    if not apikey:
        print("Please set SMSLLT_APIKEY environment variable")
        print("  export SMSLLT_APIKEY='***'")
        sys.exit(1)

    client = SmslltClient(apikey=apikey)

    print("=" * 50)
    print("📨 Bulk SMS & Keyword SMS Demo")
    print("=" * 50)

    # ── Bulk SMS ─────────────────────────────────────
    print("\n1️⃣  Bulk SMS — sending test message:")
    print("   (Using example numbers — replace with real ones)")
    try:
        result = client.bulk_sms(
            tel_list=["+8613800000000", "+8613800000001"],
            text="Your verification code: 123456 [smsllt SDK test]",
            sender="SMSLLT",
        )
        print(f"   ✅ Result: {result}")
    except SmslltError as e:
        print(f"   ⚠️ {type(e).__name__}: {e}")

    # ── Keyword SMS: Get Number ──────────────────────
    print("\n2️⃣  Keyword SMS — get number:")
    try:
        kw_result = client.get_keyword_number(
            phone="+8613800000000",
            card_type=None,
            dedupe=True,
        )
        print(f"   ✅ Result: {kw_result}")
    except SmslltError as e:
        print(f"   ⚠️ {type(e).__name__}: {e}")

    # ── Keyword SMS: Get SMS by keyword ──────────────
    print("\n3️⃣  Keyword SMS — get SMS with keyword filter:")
    try:
        sms_result = client.get_keyword_sms(
            phone="+8613800000000",
            keyword="verification",
        )
        print(f"   ✅ Result: {sms_result}")
    except SmslltError as e:
        print(f"   ⚠️ {type(e).__name__}: {e}")

    # ── Keyword SMS: Release ─────────────────────────
    print("\n4️⃣  Keyword SMS — release number:")
    try:
        release_result = client.del_keyword_number(phone="+8613800000000")
        print(f"   ✅ Released: {release_result}")
    except SmslltError as e:
        print(f"   ⚠️ {type(e).__name__}: {e}")

    # ── Keyword SMS History ──────────────────────────
    print("\n5️⃣  Keyword SMS — history:")
    try:
        history = client.keyword_sms_history(page=1)
        records = history.get("data", history.get("records", history.get("list", [])))
        if records:
            for r in records[:5]:
                print(f"   {r}")
        else:
            print("   (no keyword SMS history)")
    except SmslltError as e:
        print(f"   ⚠️ {type(e).__name__}: {e}")

    # ── Get Again Number ─────────────────────────────
    print("\n6️⃣  Re-activate number (getAgainNumber):")
    print("   (Requires a valid request_id — using placeholder)")
    try:
        again = client.get_again_number(request_id="YOUR_REQUEST_ID")
        print(f"   ✅ Result: {again}")
    except SmslltError as e:
        print(f"   ⚠️ {type(e).__name__}: {e}")

    client.close()
    print("\n✅ Bulk & Keyword demo complete!")


if __name__ == "__main__":
    main()