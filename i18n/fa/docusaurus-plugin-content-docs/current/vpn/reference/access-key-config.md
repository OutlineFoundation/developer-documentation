---
title: "Access Key Configuration Reference"
sidebar_label: "Access Key Config"
---

## تونل‌ها

### TunnelConfig

تونل بالاترین سطح شیء در پیکربندی Outline است. نشان می‌دهد چطور
باید وی‌پی‌ان پیکربندی شود.

**قالب:** [ExplicitTunnelConfig](#explicittunnelconfig)‏ |
[‫LegacyShadowsocksConfig](#legacyshadowsocksconfig)‏ |
[‫LegacyShadowsocksURI](#legacyshadowsocksuri)

### ExplicitTunnelConfig

**قالب:** *ساختار*

**فیلدها:**

- ‫`transport` ‏([TransportConfig](#transportconfig)): حمل‌ونقلی که برای
تبادل بسته‌ها با مقصدِ هدف‌یابی‌شده استفاده می‌شود

- ‫`error` (*ساختار*): اطلاعاتی که برای مراوده با کاربر استفاده می‌شود، درصورتی‌که
خطای سرویس (مثل منقضی شدن کلید، مصرف بیش‌ازحد سهمیه) اتفاق بیفتد

    - ‫`message` (*رشته*): پیام کاربرپسندی که برای نمایش داده شدن به کاربر است

    - ‫`details` (*رشته*): پیامی برای نمایش داده شدن به کاربر وقتی جزئیات
خطا را باز می‌کند. برای عیب‌یابی مفید است.

فیلدهای `error` و `transport` به‌صورت متقابل انحصاری‌اند.

نمونه موفق:

```yaml
transport:
  $type: tcpudp
  tcp:
    ...  # Stream Dialer for TCP
  udp:
    ...  # Packet Listener for UDP
```

نمونه خطا:

```yaml
error:
  message: Quota exceeded
  details: Used 100GB out of 100GB
```

## حمل‌ونقل‌ها

### TransportConfig

مشخص می‌کند چطور بسته‌ها باید با مقصد هدف‌یابی‌شده تبادل شوند.

**قالب:** [میانا](#interface)

انواع میاناهای پشتیبانی‌شده:

- ‫`tcpudp`:‏ [TCPUDPConfig](#tcpudpconfig)

### TCPUDPConfig

‫TCPUDPConfig اجازه می‌دهد تا راهبردهای TCP و UDP به‌طور جداگانه تنظیم شوند.

**قالب:** *ساختار*

**فیلدها:**

- ‫`tcp`‏ ([DialerConfig](#dialerconfig)): «شماره‌گیر جاری‌سازی» برای استفاده برای اتصالات
TCP.

- ‫`udp`‏ ([PacketListenerConfig](#packetlistenerconfig)): «شنونده بسته»
برای استفاده با بسته‌های UDP.

نمونه ارسال TCP و UDP به نقطه‌های پایانی مختلف:

```yaml
tcp:
  $type: shadowsocks
  endpoint: ss.example.com:80
  <<: &cipher
    cipher: chacha20-ietf-poly1305
    secret: SECRET
  prefix: "POST "

udp:
  $type: shadowsocks
  endpoint: ss.example.com:53
  <<: *cipher
```

## نقطه‌های پایانی

نقطه‌های پایانی اتصالات به نقطه پایانی ثابتی را تبیین می‌کنند. «شماره‌گیرها»
در اولویت هستند زیرا به بهینه‌سازی‌های نقطه پایانی خاص اجازه می‌دهند. نقطه‌های پایانی «جاری‌سازی»
و «بسته» وجود دارند.

### EndpointConfig

**قالب:** *رشته* | [میانا](#interface)

نقطه پایانی *رشته* عبارت از نشانی «میزبان:درگاه» مربوط به نقطه پایانی انتخابی است. اتصال
بااستفاده از «شماره‌گیر» پیش‌فرض تبیین شد.

انواع میانای پشتیبانی‌شده برای نقاط پایانی جریان‌سازی و بسته:

- ‫`dial`‏: [DialEndpointConfig](#dialendpointconfig)

- ‫`first-supported`‏: [FirstSupportedConfig](#firstsupportedconfig)

- ‫`websocket`‏: [WebsocketEndpointConfig](#websocketendpointconfig)

- ‫`shadowsocks`‏: [ShadowsocksConfig](#shadowsocksconfig)

### DialEndpointConfig

اتصالات را با شماره‌گیری یک نشانی ثابت تبیین می‌کند. می‌تواند شماره‌گیری را بگیرد که
اجازه می‌دهد راهبردها نوشته شود.

**قالب:** *ساختار*

**فیلدها:**

- ‫`address` (*رشته*): نشانی نقطه پایان برای شماره‌گیری

- ‫`dialer`‏ ([DialerConfig](#dialerconfig)): شماره‌گیر برای استفاده در شماره‌گیری
نشانی

### WebsocketEndpointConfig

تونل‌ها ازطریق Websockets اتصالات را برای نقطه پایانی جاری‌سازی و بسته‌بندی می‌کنند.

برای جاری‌سازی اتصالات، هر نوشته به پیام Websockets تبدیل می‌شود. برای
اتصالات بسته، هر بسته به پیام Websockets تبدیل می‌شود.

**قالب:** *ساختار*

**فیلدها:**

- ‫`url` (*رشته*): نشانی وب برای نقطه پایانی Websockets. طرح‌واره باید
`https` یا `wss` برای Websockets ازطریق «امنیت لایه انتقال» باشد و `http` یا `ws` برای متن ساده
Websocket باشد.

- ‫`endpoint`‏ ([EndpointConfig](#endpointconfig)): سرور وب نقطه پایانی به
اتصال به. اگر وجود نداشته باشد، به نشانی مشخص‌شده در این نشانی وب متصل می‌شود.

## شماره‌گیرها

شماره‌گیرها اتصالاتی را که به نشانی نقطه پایان داده شده است تبیین می‌کنند. شماره‌گیرهای جاری‌سازی و
بسته وجود دارد.

### DialerConfig

**قالب:** *تهی* | [میانا](#interface)

شماره‌گیر *تهی* (غایب) یعنی «شماره‌گیر» پیش‌فرضی که از اتصالات مستقیم TCP
برای «جریان‌سازی» و از اتصالات مستقیم UDP برای «بسته‌ها» استفاده می‌کند.

انواع میانای پشتیبانی‌شده برای شماره‌گیرهای جریان‌سازی و بسته:

- ‫`first-supported`‏: [FirstSupportedConfig](#firstsupportedconfig)

- ‫`shadowsocks`‏: [ShadowsocksConfig](#shadowsocksconfig)

## شنوندگان بسته

«شنونده بسته» اتصال بسته نامحدودی را تبیین می‌کند که می‌تواند برای
ارسال بسته‌ها به چندین مقصد استفاده شود.

### PacketListenerConfig

**قالب:** *تهی* | [میانا](#interface)

«شنونده بسته» *تهی * (غایب) یعنی «شنونده بسته» پیش‌فرضی که
«شنونده بسته UDP» است.

انواع میاناهای پشتیبانی‌شده:

- ‫`first-supported`‏: [FirstSupportedConfig](#firstsupportedconfig)

- ‫`shadowsocks`‏: [ShadowsocksPacketListenerConfig](#shadowsocksconfig)

## راهبردها

### Shadowsocks

#### LegacyShadowsocksConfig

‫LegacyShadowsocksConfig معرف تونلی است که از Shadowsocks به‌عنوان
حمل‌ونقل استفاده می‌کند. و قالب قدیمی را برای سازگاری با نسخه قدیمی اجرا می‌کند.

**قالب:** *ساختار*

**فیلدها:**

- ‫`server` (*رشته*): میزبانی است برای اتصال به

- ‫`server_port` (*شماره*): شماره درگاهی است برای اتصال به

- ‫`method` (*رشته*): [رمز
‫AEAD](https://shadowsocks.org/doc/aead.html#aead-ciphers) برای استفاده

- ‫`password` (*رشته*): برای تولید کلید رمزگذاری استفاده می‌شود

- ‫`prefix` (*رشته*): [مبدل شدن
پیشوند](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/) برای استفاده.
در جاری‌سازی و اتصال‌های بسته‌ای پشتیبانی شده است.

نمونه:

```yaml
server: example.com
server_port: 4321
method: chacha20-ietf-poly1305
password: SECRET
prefix: "POST "
```

#### LegacyShadowsocksURI

‫LegacyShadowsocksURI معرف تونلی است که از Shadowsocks به‌عنوان حمل‌ونقل استفاده می‌کند.
و قالب قدیمی نشانی وب را برای سازگاری با نسخه قدیمی اجرا می‌کند.

**قالب:** *رشته*

[قالب نشانی وب قدیمی
Shadowsocks](https://shadowsocks.org/doc/configs.html#uri-and-qr-code) و [طرح نشانی وب
SIP002](https://shadowsocks.org/doc/sip002.html) را ببینید. افزایه‌ها را پشتیبانی نمی‌کنیم.

نمونه:

```yaml
ss://chacha20-ietf-poly1305:SECRET@example.com:443?prefix=POST%20
```

#### ShadowsocksConfig

‫ShadowsocksConfig می‌تواند نماینده «شماره‌گیرهای جاری‌سازی یا بسته» باشد و همچنین
شنونده بسته‌ای که از Shadowsocks استفاده می‌کند.

**قالب:** *ساختار*

**فیلدها:**

- ‫`endpoint`‏ ([EndpointConfig](#endpointconfig)): نقطه پایانی Shadowsocks به
اتصال به

- ‫`cipher` (*رشته*): [رمز
‫AEAD](https://shadowsocks.org/doc/aead.html#aead-ciphers) برای استفاده

- ‫`secret` (*رشته*): برای تولید کلید رمزگذاری استفاده می‌شود

- ‫`prefix` (*رشته*، اختیاری): [مبدل شدن
پیشوند](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/) برای استفاده.
در جاری‌سازی و اتصال‌های بسته‌ای پشتیبانی شده است.

نمونه:

```yaml
endpoint: example.com:80
cipher: chacha20-ietf-poly1305
secret: SECRET
prefix: "POST "
```

## تعریف‌های متا

### FirstSupportedConfig

از اولین پیکربندی‌ای که این برنامه پشتیبانی می‌کند استفاده می‌کند. این کار راهی است برای
ترکیب کردن پیکربندی‌های جدید وقتی نسخه قدیمی دارد با پیکربندی‌های قدیمی سازگار می‌شود.

**قالب:** *ساختار*

**فیلدها:**

- ‫`options`‏ ([EndpointConfig[]](#endpointconfig)‏ |
[‫DialerConfig[]](#dialerconfig)‏ |
[‫PacketListenerConfig[]](#packetlistenerconfig)): فهرست گزینه‌ها برای
درنظر گرفتن

نمونه:

```yaml
options:
  - $type: websocket
    url: wss://example.com/SECRET_PATH
  - ss.example.com:4321
```

### میانا

میاناها اجازه می‌دهند تا یکی از چندین اجراها انتخاب شوند. میانا برای مشخص کردن نوعی که پیکربندی ارائه می‌کند، از فیلد
‫`$type` استفاده می‌کند.

نمونه:

```yaml
$type: shadowsocks
endpoint: example.com:4321
cipher: chacha20-ietf-poly1305
secret: SECRET
```
