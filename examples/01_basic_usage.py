#!/usr/bin/env python3
"""
Example 1: Basic Usage — get balance, list countries and services.

Usage:
    export SMSLLT_APIKEY="your-api-key"
    python examples/01_basic_usage.py
"""

import os
import sys

# Allow running from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from smsllt import SmslltClient


def main():
    apikey = os.environ.get("SMSLLT_APIKEY")
    if not apikey:
        print("Please set SMSLLT_APIKEY environment variable")
        print("  export SMSLLT_APIKEY='your-api-key'")
        sys.exit(1)

    client = SmslltClient(apikey=apikey)

    # ── Balance ──────────────────────────────────────
    print("=" * 50)
    print("💰 Account Balance")
    print("=" * 50)
    balance = client.get_balance()
    print(f"Balance: ${balance:.2f}")

    # ── Countries ────────────────────────────────────
    print("\n" + "=" * 50)
    print("🌍 Supported Countries (top 10)")
    print("=" * 50)
    countries = client.get_countries()
    for c in countries[:10]:
        code = c.get("country_code", c.get("code", "?"))
        name = c.get("name", c.get("country_name", "?"))
        print(f"  {code:6s} │ {name}")

    # ── Services (Japan) ─────────────────────────────
    print("\n" + "=" * 50)
    print("📱 Services in Japan (top 10)")
    print("=" * 50)
    services = client.get_services(country_code="JP", page_size=50)
    svc_list = services.get("data", services.get("services", []))
    for svc in svc_list[:10]:
        sid = svc.get("service_id", svc.get("id", "?"))
        name = svc.get("name", "?")
        price = svc.get("price", "?")
        print(f"  [{sid:4s}] {name:30s} ${price}")

    # ── Search for Telegram ──────────────────────────
    print("\n" + "=" * 50)
    print("🔍 Search: 'Telegram'")
    print("=" * 50)
    telegram = client.get_services(query="Telegram")
    tg_list = telegram.get("data", telegram.get("services", []))
    for svc in tg_list[:5]:
        sid = svc.get("service_id", svc.get("id", "?"))
        name = svc.get("name", "?")
        price = svc.get("price", "?")
        country = svc.get("country_code", svc.get("country", ""))
        print(f"  [{sid:4s}] {name:30s} ${price:6s} ({country})")

    client.close()
    print("\n✅ Done!")


if __name__ == "__main__":
    main()