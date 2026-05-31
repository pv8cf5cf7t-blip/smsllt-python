<p align="center">
  <img src="https://img.shields.io/pypi/v/smsllt?label=PyPI&color=blue" alt="PyPI version">
  <img src="https://img.shields.io/pypi/pyversions/smsllt?color=green" alt="Python versions">
  <img src="https://img.shields.io/pypi/dm/smsllt?color=orange" alt="Downloads">
  <img src="https://img.shields.io/github/license/pv8cf5cf7t-blip/smsllt-python?color=brightgreen" alt="License MIT">
  <img src="https://img.shields.io/github/stars/pv8cf5cf7t-blip/smsllt-python?style=social" alt="GitHub stars">
  <img src="https://img.shields.io/badge/SMS-Verification-blue?logo=messages" alt="SMS Verification">
  <img src="https://img.shields.io/badge/Virtual-Numbers-purple?logo=phone" alt="Virtual Numbers">
  <img src="https://img.shields.io/badge/Payment-USDT-brightgreen?logo=tether" alt="USDT Payment">
  <img src="https://img.shields.io/badge/Countries-12+-orange?logo=airplane" alt="12+ Countries">
  <img src="https://img.shields.io/badge/Services-200K+-red?logo=checkmarx" alt="200K+ Services">
</p>

<h1 align="center">📱 smsllt-python</h1>

<p align="center">
  <strong>Official Python SDK for <a href="https://smsllt.com">smsllt.com</a> — The Global SMS Verification Platform</strong><br>
  <em>200,000+ services · 12+ countries · USDT Payment · Virtual Phone Numbers</em>
</p>

<p align="center">
  <a href="#english">🇬🇧 English</a> &nbsp;|&nbsp;
  <a href="#中文">🇨🇳 中文</a> &nbsp;|&nbsp;
  <a href="https://smsllt.com">🌐 smsllt.com</a> &nbsp;|&nbsp;
  <a href="https://pypi.org/project/smsllt/">📦 PyPI</a> &nbsp;|&nbsp;
  <a href="#quick-start">⚡ Quick Start</a>
</p>

<hr>

<p align="center">
  <b>Need a virtual phone number for SMS verification?</b> 🎯<br>
  smsllt provides <b>temporary phone numbers</b> to receive SMS online for <b>Discord, Telegram, ChatGPT, WhatsApp, Google, Microsoft, Tinder, TikTok</b> and 200,000+ other services across 12+ countries. Pay with <b>USDT</b> (TRC20). No monthly subscription — pay only for what you use.
</p>

<p align="center">
  <a href="https://smsllt.com" target="_blank">
    <img src="https://img.shields.io/badge/🚀_Get_Started-smsllt.com-FF6B6B?style=for-the-badge&logo=vercel&logoColor=white&labelColor=333" alt="Get Started">
  </a>
</p>

---

<a id="english"></a>
## 🇬🇧 English

**smsllt-python** is the official Python SDK for [smsllt.com](https://smsllt.com) — a global **SMS verification platform** offering virtual phone numbers for receiving SMS online. Full API coverage, type annotations, automatic retries, rate limiting, and rich error handling.

> 🏆 **Why smsllt?** 200K+ services covered across 12+ countries. Pay with **USDT (TRC20)**. No KYC. Instant delivery. SMS verification codes received in seconds.

### ✨ Features

| Category | Feature |
|----------|---------|
| 🔌 **Full API** | Balance, countries, services, get/release numbers, SMS polling, bulk SMS, keyword SMS, history, payments |
| 🧠 **Smart Retry** | Exponential backoff — handles transient network/server errors automatically |
| ⏱️ **Rate Limiting** | Configurable interval between API calls to avoid 429 errors |
| 🛡️ **Rich Exceptions** | `AuthenticationError`, `InsufficientBalanceError`, `NoNumberAvailableError`, etc. |
| 📝 **Fully Typed** | Complete type hints for IDE autocompletion (VS Code, PyCharm) |
| 🔄 **Context Manager** | `with SmslltClient(...) as client:` — automatic cleanup |
| 📩 **SMS Polling** | `wait_for_sms()` — poll until verification code arrives |

### 📊 Supported Services (Highlights)

<details open>
<summary><b>Click to expand — 200K+ services available</b></summary>

| Service | Category | Popular Countries | Typical Price |
|---------|----------|-------------------|---------------|
| 📞 **Discord** | Social | US, JP, UK, HK | from $0.03 |
| 💬 **Telegram** | Messaging | US, HK, IN, ID | from $0.50 |
| 🤖 **ChatGPT / OpenAI** | AI | JP, US, SG | from $0.28 |
| 📱 **WhatsApp** | Messaging | US, IN, BR | from $0.10 |
| 🔍 **Google** | Tech | US, JP, KR | from $0.05 |
| 🪟 **Microsoft** | Tech | US, GB, AU | from $0.05 |
| 🐦 **Twitter / X** | Social | US, JP, UK | from $0.03 |
| 🎵 **TikTok** | Social | US, JP, KR | from $0.05 |
| 🔥 **Tinder** | Dating | US, GB, AU | from $0.05 |
| 📧 **Gmail** | Email | US, IN, ID | from $0.05 |
| 🛒 **Amazon** | E-commerce | US, JP, DE | from $0.10 |
| 🚗 **Uber** | Transport | US, BR, MX | from $0.10 |

> 💡 **Use `client.get_services()` for real-time pricing and full service list.**

</details>

### 🌍 Supported Countries

| Flag | Country | Code | Available Numbers |
|------|---------|------|-------------------|
| 🇺🇸 | United States | US | ✅ |
| 🇬🇧 | United Kingdom | GB | ✅ |
| 🇯🇵 | Japan | JP | ✅ |
| 🇭🇰 | Hong Kong | HK | ✅ |
| 🇰🇷 | South Korea | KR | ✅ |
| 🇩🇪 | Germany | DE | ✅ |
| 🇮🇳 | India | IN | ✅ |
| 🇮🇩 | Indonesia | ID | ✅ |
| 🇧🇷 | Brazil | BR | ✅ |
| 🇦🇺 | Australia | AU | ✅ |
| 🇸🇬 | Singapore | SG | ✅ |
| 🇲🇽 | Mexico | MX | ✅ |

> 🌏 *12+ countries and growing. Check `get_countries()` for the latest list.*

### 💰 Pricing & Payment

- **Pay-as-you-go** — no monthly fees, no hidden costs
- **USDT (TRC20)** cryptocurrency payment — fast, global, low fees
- **Prices vary by service and country** — e.g., Discord from $0.03, Telegram from $0.50
- **Auto top-up** available for high-volume users

```python
# Check real-time pricing
services = client.get_services(country_code="JP")
for svc in services.get("data", services.get("services", [])):
    print(f"{svc['name']}: ${svc['price']}")

# Check your balance anytime
balance = client.get_balance()
print(f"Balance: ${balance:.2f}")
```

### 🚀 Installation

```bash
pip install smsllt
```

Or install from source:

```bash
git clone https://github.com/pv8cf5cf7t-blip/smsllt-python.git
cd smsllt-python
pip install -e .
```

**Requirements:** Python 3.9+, `requests>=2.25`

<a id="quick-start"></a>
### ⚡ Quick Start

```python
from smsllt import SmslltClient

# 1. Get your API key from https://smsllt.com (Account → API Key)
client = SmslltClient(apikey="your-api-key-here")

# 2. Check your balance
balance = client.get_balance()
print(f"💰 Balance: ${balance:.2f}")

# 3. Browse available countries
countries = client.get_countries()
for c in countries[:5]:
    print(f"  🌍 {c.get('country_code')}: {c.get('name', c.get('country_name'))}")

# 4. Find Telegram numbers in the US
svc = client.get_services(country_code="US", query="Telegram")
for s in svc.get("data", svc.get("services", []))[:3]:
    print(f"  📱 [{s.get('service_id')}] {s.get('name')}: ${s.get('price')}")

# 5. Get a phone number & receive SMS
result = client.get_number(service_id=86, country_code="US")
print(f"📞 Number: {result['number']}")

# Wait for SMS (polls every 3s, max 180s)
sms = client.wait_for_sms(result["request_id"], poll_interval=3, max_wait=180)
print(f"✅ SMS Code: {sms['sms_code']}")

# 6. Release the number when done
client.release_number(result["request_id"])
print("🔒 Number released.")
```

### 🎯 Real-World Examples

#### Discord Account Verification

```python
# Get a US number for Discord verification
result = client.get_number(service_id=86, country_code="US")

# Enter result['number'] on Discord signup page
# Wait for the verification code
sms = client.wait_for_sms(result["request_id"])
print(f"Discord verification code: {sms['sms_code']}")

client.release_number(result["request_id"])
```

#### ChatGPT / OpenAI Registration

```python
# OpenAI often works best with Japanese numbers
result = client.get_number(service_id=150, country_code="JP")

# Use result['number'] on OpenAI's signup page
sms = client.wait_for_sms(result["request_id"], max_wait=300)
print(f"OpenAI verification code: {sms['sms_code']}")

client.release_number(result["request_id"])
```

#### Telegram Registration

```python
# Telegram — try HK numbers for best pricing
result = client.get_number(service_id=88, country_code="HK")
print(f"Telegram number: {result['number']}")

sms = client.wait_for_sms(result["request_id"])
print(f"Telegram code: {sms['sms_code']}")

client.release_number(result["request_id"])
```

### 🔧 Advanced Usage

#### Context Manager

```python
with SmslltClient(apikey="your-key") as client:
    balance = client.get_balance()
    result = client.get_number(service_id=86, country_code="JP")
    sms = client.wait_for_sms(result["request_id"])
    # Session auto-closes on exit — no cleanup needed!
```

#### Login & USDT Payment

```python
client = SmslltClient(
    apikey="your-key",
    username="your-username",
    password="your-password",
)

# Login to get Bearer token for payment API
user_info = client.login()
print(f"✅ Logged in as: {user_info['user'].get('username')}")

# Top up with USDT (TRC20)
payment = client.make_payment(amount=10.0, method="TRC20 USDT")
print(f"💳 Payment: {payment}")
```

#### Error Handling

```python
from smsllt.exceptions import (
    InsufficientBalanceError,
    NoNumberAvailableError,
    SmsNotReceivedError,
)

try:
    result = client.get_number(service_id=86, country_code="JP")
    sms = client.wait_for_sms(result["request_id"])
except NoNumberAvailableError:
    print("No numbers available — try a different country")
except InsufficientBalanceError:
    print("Balance too low — top up at smsllt.com")
except SmsNotReceivedError:
    print("SMS didn't arrive — try again")
    client.release_number(result["request_id"], status="reject")
```

#### Bulk SMS

```python
# Send bulk SMS to multiple numbers
client.bulk_sms(
    tel_list=["+1234567890", "+1987654321"],
    text="Your verification code is 123456",
    msg_type="text",
    sender="SMSLLT",
)
```

### 📚 API Reference

#### Account

| Method | Description |
|--------|-------------|
| `get_balance()` | Get account balance (USD) |
| `login()` | Login with username/password for payment API |

#### Lookups

| Method | Description |
|--------|-------------|
| `get_countries()` | List all supported countries |
| `get_services(country_code, query, page, page_size)` | List services with real-time pricing |

#### Number Management

| Method | Description |
|--------|-------------|
| `get_number(service_id, country_code)` | Request a virtual phone number |
| `get_sms(request_id)` | Retrieve SMS verification code |
| `wait_for_sms(request_id, poll_interval, max_wait)` | Poll until SMS code received |
| `release_number(request_id, status)` | Release/blacklist number |
| `get_again_number(request_id)` | Re-activate number for another SMS |

#### History

| Method | Description |
|--------|-------------|
| `sms_history(page, page_size)` | Get activation history |

#### Keyword SMS (通用短信)

| Method | Description |
|--------|-------------|
| `get_keyword_number(phone, card_type, dedupe)` | Get keyword-based number |
| `get_keyword_sms(phone, keyword)` | Fetch SMS by keyword |
| `del_keyword_number(phone)` | Release keyword number |
| `keyword_sms_history(page)` | Keyword SMS history |

#### Bulk SMS

| Method | Description |
|--------|-------------|
| `bulk_sms(tel_list, text, msg_type, sender)` | Send bulk SMS |

#### Payments

| Method | Description |
|--------|-------------|
| `make_payment(amount, method)` | Create payment (requires login) |

### 🚨 Exception Hierarchy

```python
from smsllt.exceptions import (
    SmslltError,              # Base exception
    AuthenticationError,      # 401/403 — invalid API key
    InsufficientBalanceError, # Balance too low
    NoNumberAvailableError,   # No numbers for service/country
    SmsNotReceivedError,      # SMS hasn't arrived yet
    RateLimitError,           # 429 — too many requests
    ServerError,              # 5xx — server issue
    NetworkError,             # Connection problem
    InvalidParameterError,    # Bad parameters
    RequestTimeoutError,      # Request timed out
)
```

### 🔍 SEO Keywords

`sms verification`, `virtual phone number`, `temporary phone number`, `receive sms online`, `sms verification api`, `python sdk`, `virtual numbers`, `smsllt`, `接码平台`, `虚拟号码`, `sms activation`, `phone verification`, `sms code`, `otp verification`, `usdt payment sms`, `discord sms verification`, `telegram virtual number`, `chatgpt phone verification`, `openai sms`, `whatsapp virtual number`, `bulk sms`, `sms api`, `temporary number for verification`

### 📄 License

MIT — see [LICENSE](LICENSE) file.

---

<a id="中文"></a>
## 🇨🇳 中文

**smsllt-python** 是 [smsllt.com](https://smsllt.com) 海外接码平台的官方 Python SDK。覆盖全部 API，支持类型注解、自动重试、速率限制和完善的错误处理。

> 🏆 **为什么选择 smsllt？** 20万+服务覆盖12国，支持 **USDT (TRC20)** 加密货币支付，无需实名，即时获取验证码。

### ✨ 功能亮点

| 类别 | 功能 |
|------|------|
| 🔌 **完整 API** | 余额、国家、服务、取号、查码、释放、群发、通用短信、历史、充值 |
| 🧠 **智能重试** | 指数退避机制，自动处理网络波动 |
| ⏱️ **速率控制** | 可配置 API 调用间隔，避免 429 限流 |
| 🛡️ **异常分类** | `AuthenticationError`、`InsufficientBalanceError` 等细分异常 |
| 📝 **全类型注解** | IDE 自动补全（VS Code、PyCharm） |
| 🔄 **上下文管理** | `with` 语句自动释放资源 |
| 📩 **短信轮询** | `wait_for_sms()` 自动等待验证码 |

### 📊 热门服务价格参考

| 服务 | 类别 | 常用国家 | 参考价格 |
|------|------|----------|----------|
| 📞 Discord | 社交 | 美国、日本、英国、香港 | $0.03 起 |
| 💬 Telegram | 通讯 | 美国、香港、印度 | $0.50 起 |
| 🤖 ChatGPT / OpenAI | AI | 日本、美国、新加坡 | $0.28 起 |
| 📱 WhatsApp | 通讯 | 美国、印度、巴西 | $0.10 起 |
| 🔍 Google | 科技 | 美国、日本、韩国 | $0.05 起 |
| 🪟 Microsoft | 科技 | 美国、英国、澳洲 | $0.05 起 |
| 🐦 Twitter / X | 社交 | 美国、日本、英国 | $0.03 起 |
| 🎵 TikTok | 社交 | 美国、日本、韩国 | $0.05 起 |
| 🔥 Tinder | 交友 | 美国、英国、澳洲 | $0.05 起 |

> 💡 **使用 `get_services()` 查询实时价格，200K+ 服务可选。**

### 💰 支付方式

- **按量付费** — 无月费，无隐藏费用
- **USDT (TRC20)** — 加密货币支付，全球通用，低手续费
- **自动充值** — 高频用户支持自动续费

### 🚀 安装

```bash
pip install smsllt
```

或从源码安装：

```bash
git clone https://github.com/pv8cf5cf7t-blip/smsllt-python.git
cd smsllt-python
pip install -e .
```

**环境要求：** Python 3.9+，`requests>=2.25`

### ⚡ 快速上手

```python
from smsllt import SmslltClient

# 1. 从 smsllt.com 账户页面获取 API 密钥
client = SmslltClient(apikey="你的API密钥")

# 2. 查询余额
balance = client.get_balance()
print(f"💰 余额: ${balance:.2f}")

# 3. 查看支持的国家
countries = client.get_countries()
for c in countries[:5]:
    print(f"  🌍 {c.get('country_code')}: {c.get('name', c.get('country_name'))}")

# 4. 搜索 Telegram 服务
svc = client.get_services(country_code="US", query="Telegram")
for s in svc.get("data", svc.get("services", []))[:3]:
    print(f"  📱 [{s.get('service_id')}] {s.get('name')}: ${s.get('price')}")

# 5. 获取手机号并接收短信
result = client.get_number(service_id=86, country_code="US")
print(f"📞 号码: {result['number']}")

# 等待短信（每3秒轮询，最长等180秒）
sms = client.wait_for_sms(result["request_id"], poll_interval=3, max_wait=180)
print(f"✅ 验证码: {sms['sms_code']}")

# 6. 使用完毕释放号码
client.release_number(result["request_id"])
print("🔒 号码已释放")
```

### 🎯 实战场景

#### Discord 注册验证

```python
# 获取美国号码用于 Discord 验证
result = client.get_number(service_id=86, country_code="US")

# 在 Discord 注册页面输入 result['number']
sms = client.wait_for_sms(result["request_id"])
print(f"Discord 验证码: {sms['sms_code']}")

client.release_number(result["request_id"])
```

#### ChatGPT / OpenAI 注册

```python
# OpenAI 推荐使用日本号码
result = client.get_number(service_id=150, country_code="JP")

sms = client.wait_for_sms(result["request_id"], max_wait=300)
print(f"OpenAI 验证码: {sms['sms_code']}")

client.release_number(result["request_id"])
```

#### Telegram 注册

```python
# Telegram 推荐香港号码，性价比最高
result = client.get_number(service_id=88, country_code="HK")
print(f"Telegram 号码: {result['number']}")

sms = client.wait_for_sms(result["request_id"])
print(f"Telegram 验证码: {sms['sms_code']}")

client.release_number(result["request_id"])
```

### 🔧 进阶用法

#### 上下文管理器

```python
with SmslltClient(apikey="你的密钥") as client:
    balance = client.get_balance()
    result = client.get_number(service_id=86, country_code="JP")
    sms = client.wait_for_sms(result["request_id"])
    # 退出 with 块时自动清理资源
```

#### 登录与 USDT 充值

```python
client = SmslltClient(
    apikey="你的密钥",
    username="你的用户名",
    password="你的密码",
)

user_info = client.login()
print(f"✅ 已登录: {user_info['user'].get('username')}")

# USDT (TRC20) 充值
payment = client.make_payment(amount=10.0, method="TRC20 USDT")
print(f"💳 充值: {payment}")
```

#### 错误处理

```python
from smsllt.exceptions import (
    InsufficientBalanceError,
    NoNumberAvailableError,
    SmsNotReceivedError,
)

try:
    result = client.get_number(service_id=86, country_code="JP")
    sms = client.wait_for_sms(result["request_id"])
except NoNumberAvailableError:
    print("当前无可用号码，试试其他国家")
except InsufficientBalanceError:
    print("余额不足，请先在 smsllt.com 充值")
except SmsNotReceivedError:
    print("短信未到达，请重试")
    client.release_number(result["request_id"], status="reject")
```

#### 短信群发

```python
client.bulk_sms(
    tel_list=["+1234567890", "+1987654321"],
    text="您的验证码是 123456",
    msg_type="text",
    sender="SMSLLT",
)
```

### 📚 API 参考

#### 账户

| 方法 | 说明 |
|------|------|
| `get_balance()` | 查询账户余额（美元） |
| `login()` | 用户名密码登录，获取支付 Token |

#### 查询

| 方法 | 说明 |
|------|------|
| `get_countries()` | 获取支持的国家列表 |
| `get_services(country_code, query, page, page_size)` | 获取服务列表及实时价格 |

#### 号码管理

| 方法 | 说明 |
|------|------|
| `get_number(service_id, country_code)` | 获取虚拟手机号码 |
| `get_sms(request_id)` | 获取短信验证码 |
| `wait_for_sms(request_id, poll_interval, max_wait)` | 轮询等待验证码到达 |
| `release_number(request_id, status)` | 释放/拉黑号码 |
| `get_again_number(request_id)` | 重新激活号码接收二次短信 |

#### 历史记录

| 方法 | 说明 |
|------|------|
| `sms_history(page, page_size)` | 获取激活记录 |

#### 通用短信

| 方法 | 说明 |
|------|------|
| `get_keyword_number(phone, card_type, dedupe)` | 通用短信取号 |
| `get_keyword_sms(phone, keyword)` | 按关键词获取短信 |
| `del_keyword_number(phone)` | 释放通用短信号码 |
| `keyword_sms_history(page)` | 通用短信历史记录 |

#### 群发短信

| 方法 | 说明 |
|------|------|
| `bulk_sms(tel_list, text, msg_type, sender)` | 短信群发 |

#### 充值

| 方法 | 说明 |
|------|------|
| `make_payment(amount, method)` | 创建充值订单（需先登录） |

### 🚨 异常类型

```python
from smsllt.exceptions import (
    SmslltError,              # 基础异常
    AuthenticationError,      # 认证失败 (401/403)
    InsufficientBalanceError, # 余额不足
    NoNumberAvailableError,   # 无可用号码
    SmsNotReceivedError,      # 短信尚未到达
    RateLimitError,           # 请求频率超限 (429)
    ServerError,              # 服务器错误 (5xx)
    NetworkError,             # 网络连接错误
    InvalidParameterError,    # 参数错误
    RequestTimeoutError,      # 请求超时
)
```

### 📄 许可证

MIT

---

<p align="center">
  <b>🌐 <a href="https://smsllt.com">smsllt.com</a></b> &nbsp;|&nbsp;
  <b>📦 <a href="https://pypi.org/project/smsllt/">PyPI</a></b> &nbsp;|&nbsp;
  <b>💬 <a href="https://github.com/pv8cf5cf7t-blip/smsllt-python/issues">Issues</a></b>
</p>

<p align="center">
  <sub>Made with ❤️ for developers who need SMS verification worldwide · Pay with USDT · No KYC</sub>
</p>