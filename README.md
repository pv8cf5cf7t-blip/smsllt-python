# smsllt-python / smsllt Python SDK

[English](#english) | [中文](#中文)

---

<a id="english"></a>
## English

**smsllt-python** is the official Python SDK for [smsllt.com](https://smsllt.com), an SMS verification (接码) platform. Provides full API coverage, type annotations, automatic retries, rate limiting, and rich error handling.

### Features

- ✅ **Full API coverage** — balance, countries, services, get/check/release numbers, bulk SMS, keyword SMS, history, payments
- ✅ **Type-annotated** — full type hints for IDE autocompletion
- ✅ **Automatic retries** — handles transient network/server errors with exponential backoff
- ✅ **Rate limiting** — configurable interval between API calls
- ✅ **Rich exceptions** — specific error types (AuthenticationError, InsufficientBalanceError, NoNumberAvailableError, etc.)
- ✅ **Context manager** — use with `with` statement for automatic cleanup
- ✅ **SMS polling helper** — `wait_for_sms()` with configurable interval and timeout

### Installation

```bash
pip install smsllt
```

Or from source:

```bash
git clone https://github.com/nous-research/smsllt-python.git
cd smsllt-python
pip install -e .
```

### Quick Start

```python
from smsllt import SmslltClient

# Initialize with your API key (from smsllt.com account page)
client = SmslltClient(apikey="your-api-key-here")

# ── Account ────────────────────────────────────────
balance = client.get_balance()
print(f"Balance: ${balance:.2f}")

# ── Countries ──────────────────────────────────────
countries = client.get_countries()
for c in countries[:5]:
    print(f"  {c.get('country_code')}: {c.get('name', c.get('country_name'))}")

# ── Services & Pricing ─────────────────────────────
services = client.get_services(country_code="JP")
svc_list = services.get("data", services.get("services", []))
for svc in svc_list[:5]:
    print(f"  [{svc.get('service_id')}] {svc.get('name')}: ${svc.get('price')}")

# ── Get a Number & Receive SMS ─────────────────────
result = client.get_number(service_id=86, country_code="JP")
request_id = result["request_id"]
print(f"Got number: {result['number']} (request_id={request_id})")

# Wait for the SMS (polls every 3s, max 180s)
try:
    sms = client.wait_for_sms(request_id, poll_interval=3, max_wait=180)
    print(f"SMS code: {sms['sms_code']}")
except Exception:
    print("SMS not received in time")

# Release the number when done
client.release_number(request_id)
```

### Context Manager

```python
with SmslltClient(apikey="your-key") as client:
    balance = client.get_balance()
    # session auto-closed on exit
```

### Login & Payments

```python
client = SmslltClient(
    apikey="your-key",
    username="your-username",
    password="your-password",
)

# Login to get Bearer token
user_info = client.login()
print(f"Logged in as: {user_info['user'].get('username')}")

# Make a payment
payment = client.make_payment(amount=10.0, method="TRC20 USDT")
print(f"Payment: {payment}")
```

### API Reference

#### Account

| Method | Description |
|---------|-------------|
| `get_balance()` | Get account balance (USD) |
| `login()` | Login with username/password for payment API |

#### Lookups

| Method | Description |
|---------|-------------|
| `get_countries()` | List supported countries |
| `get_services(country_code, query, page, page_size)` | List services with pricing |

#### Number Management

| Method | Description |
|---------|-------------|
| `get_number(service_id, country_code)` | Request a phone number |
| `get_sms(request_id)` | Retrieve SMS code |
| `wait_for_sms(request_id, poll_interval, max_wait)` | Poll until SMS received |
| `release_number(request_id, status)` | Release/blacklist number |
| `get_again_number(request_id)` | Re-activate number for another SMS |

#### History

| Method | Description |
|---------|-------------|
| `sms_history(page, page_size)` | Get activation history |

#### Keyword SMS (通用短信)

| Method | Description |
|---------|-------------|
| `get_keyword_number(phone, card_type, dedupe)` | Get keyword-based number |
| `get_keyword_sms(phone, keyword)` | Fetch SMS by keyword |
| `del_keyword_number(phone)` | Release keyword number |
| `keyword_sms_history(page)` | Keyword SMS history |

#### Bulk SMS

| Method | Description |
|---------|-------------|
| `bulk_sms(tel_list, text, msg_type, sender)` | Send bulk SMS |

#### Payments

| Method | Description |
|---------|-------------|
| `make_payment(amount, method)` | Create payment (requires login) |

### Exceptions

```python
from smsllt.exceptions import (
    SmslltError,             # Base
    AuthenticationError,     # 401/403
    InsufficientBalanceError,# Low balance
    NoNumberAvailableError,  # No numbers for service
    SmsNotReceivedError,     # SMS not yet arrived
    RateLimitError,          # 429
    ServerError,             # 5xx
    NetworkError,            # Connection issues
    InvalidParameterError,   # Bad params
    RequestTimeoutError,     # Timeout
)
```

### Service Price Examples

| Service | Country | Price |
|---------|---------|-------|
| Discord | Global | $0.03 |
| Microsoft | Global | $0.05 |
| OpenAI / ChatGPT | Japan | $0.28 |
| Telegram | USA | ~$5.00 |
| Telegram | Hong Kong | ~$1.00 |

*Prices are approximate. Use `get_services()` for real-time pricing.*

### License

MIT

---

<a id="中文"></a>
## 中文

**smsllt-python** 是 [smsllt.com](https://smsllt.com) 接码平台的官方 Python SDK。覆盖全部 API，支持类型注解、自动重试、速率限制和完善的错误处理。

### 功能特性

- ✅ **完整 API 封装** — 余额查询、国家列表、服务价格、取号、查码、释放号码、群发短信、通用短信、历史记录、充值支付
- ✅ **类型注解** — 全类型提示，IDE 自动补全友好
- ✅ **自动重试** — 指数退避处理临时网络/服务器错误
- ✅ **速率限制** — 可配置 API 调用间隔
- ✅ **丰富异常** — 具体错误类型（认证失败、余额不足、无可用号码等）
- ✅ **上下文管理器** — 支持 `with` 语句自动释放连接
- ✅ **短信轮询** — `wait_for_sms()` 可配置轮询间隔和超时

### 安装

```bash
pip install smsllt
```

或从源码安装：

```bash
git clone https://github.com/nous-research/smsllt-python.git
cd smsllt-python
pip install -e .
```

### 快速上手

```python
from smsllt import SmslltClient

# 使用你的 API Key 初始化（在 smsllt.com 账户页面获取）
client = SmslltClient(apikey="你的API密钥")

# ── 查询余额 ──────────────────────────────────────
balance = client.get_balance()
print(f"余额: ${balance:.2f}")

# ── 国家列表 ──────────────────────────────────────
countries = client.get_countries()
for c in countries[:5]:
    print(f"  {c.get('country_code')}: {c.get('name', c.get('country_name'))}")

# ── 服务列表和价格 ─────────────────────────────────
services = client.get_services(country_code="JP")
svc_list = services.get("data", services.get("services", []))
for svc in svc_list[:5]:
    print(f"  [{svc.get('service_id')}] {svc.get('name')}: ${svc.get('price')}")

# ── 获取号码并接收短信 ─────────────────────────────
result = client.get_number(service_id=86, country_code="JP")
request_id = result["request_id"]
print(f"获取号码: {result['number']} (请求ID={request_id})")

# 等待短信（每3秒轮询，最长等180秒）
try:
    sms = client.wait_for_sms(request_id, poll_interval=3, max_wait=180)
    print(f"验证码: {sms['sms_code']}")
except Exception:
    print("超时未收到短信")

# 使用完毕后释放号码
client.release_number(request_id)
```

### 上下文管理器

```python
with SmslltClient(apikey="你的密钥") as client:
    balance = client.get_balance()
    # 退出时自动关闭连接
```

### 登录与充值

```python
client = SmslltClient(
    apikey="你的密钥",
    username="你的用户名",
    password="你的密码",
)

# 登录获取 Bearer Token
user_info = client.login()
print(f"已登录: {user_info['user'].get('username')}")

# 充值
payment = client.make_payment(amount=10.0, method="TRC20 USDT")
print(f"充值结果: {payment}")
```

### API 参考

#### 账户

| 方法 | 说明 |
|-------|------|
| `get_balance()` | 查询账户余额（美元） |
| `login()` | 用户名密码登录，获取支付所需 Token |

#### 查询

| 方法 | 说明 |
|-------|------|
| `get_countries()` | 获取支持的国家列表 |
| `get_services(country_code, query, page, page_size)` | 获取服务列表及价格 |

#### 号码管理

| 方法 | 说明 |
|-------|------|
| `get_number(service_id, country_code)` | 获取手机号码 |
| `get_sms(request_id)` | 获取短信验证码 |
| `wait_for_sms(request_id, poll_interval, max_wait)` | 轮询等待短信 |
| `release_number(request_id, status)` | 释放/拉黑号码 |
| `get_again_number(request_id)` | 重新激活号码接收二次短信 |

#### 历史记录

| 方法 | 说明 |
|-------|------|
| `sms_history(page, page_size)` | 获取激活记录 |

#### 通用短信

| 方法 | 说明 |
|-------|------|
| `get_keyword_number(phone, card_type, dedupe)` | 通用短信取号 |
| `get_keyword_sms(phone, keyword)` | 按关键词获取短信 |
| `del_keyword_number(phone)` | 释放通用短信号码 |
| `keyword_sms_history(page)` | 通用短信历史记录 |

#### 群发短信

| 方法 | 说明 |
|-------|------|
| `bulk_sms(tel_list, text, msg_type, sender)` | 短信群发 |

#### 充值

| 方法 | 说明 |
|-------|------|
| `make_payment(amount, method)` | 创建充值订单（需先登录） |

### 异常类型

```python
from smsllt.exceptions import (
    SmslltError,             # 基础异常
    AuthenticationError,     # 认证失败 (401/403)
    InsufficientBalanceError,# 余额不足
    NoNumberAvailableError,  # 无可用号码
    SmsNotReceivedError,     # 短信尚未到达
    RateLimitError,          # 请求频率超限 (429)
    ServerError,             # 服务器错误 (5xx)
    NetworkError,            # 网络连接错误
    InvalidParameterError,   # 参数错误
    RequestTimeoutError,     # 请求超时
)
```

### 服务价格参考

| 服务 | 国家 | 价格 |
|------|------|------|
| Discord | 全球 | $0.03 |
| Microsoft | 全球 | $0.05 |
| OpenAI / ChatGPT | 日本 | $0.28 |
| Telegram | 美国 | ~$5.00 |
| Telegram | 香港 | ~$1.00 |

*价格为参考值，请使用 `get_services()` 获取实时价格。*

### 许可证

MIT