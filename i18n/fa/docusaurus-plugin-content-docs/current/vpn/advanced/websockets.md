---
title: "Disguise Connections as Web Traffic with Shadowsocks-over-WebSockets"
sidebar_label: "WebSockets"
---

*کارخواه Outline نسخه ۱.۱۵.۰ به بالا.*

این آموزش گام‌به‌گام راهنمایی مشروح مرحله‌به‌مرحله‌ای را ارائه می‌دهد تا به شما کمک کند
Shadowsocks-over-WebSockets را، تکنیک قدرتمندی برای دور زدن سانسور در
محیط‌هایی که اتصال‌های معمول Shadowsocks مسدود است، اجرا کنید. با بسته‌بندی کردن
ترافیک Shadowsocks درون WebSockets، می‌توانید آن را به‌عنوان ترافیک وب استاندارد مخفی کنید و
تاب‌آوری و دسترس‌پذیری را بهبود دهید.

## مرحله ۱: پیکربندی و اجرای سرور Outline {#step_1_configure_and_run_an_outline_server}

فایل `config.yaml` جدیدی را با پیکربندی‌های زیر بسازید:

```yaml
web:
  servers:
    - id: server1
        listen: 127.0.0.1:<WEB_SERVER_PORT>

services:
  - listeners:
      - type: websocket-stream
        web_server: server1
        path: /<TCP_PATH>
      - type: websocket-packet
        web_server: server1
        path: /<UDP_PATH>
    keys:
      - id: 1
        cipher: chacha20-ietf-poly1305
        secret: <SHADOWSOCKS_SECRET>
```

جدیدترین
[`outline-ss-server`](https://github.com/Jigsaw-Code/outline-ss-server/releases)
را بارگیری کنید و آن را بااستفاده از پیکربندی ساخته‌شده اجرا کنید:

```sh
outline-ss-server -config=config.yaml
```

## مرحله ۲: افشا کردن سرور وب {#step_2_expose_the_web_server}

برای اینکه سرور وب WebSocket شما دردسترس عموم قرار گیرد، باید آن را
در اینترنت افشا کنید و
[امنیت لایه انتقال (TLS)](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security) را پیکربندی کنید.
برای دست‌یافتن به این امر چندین گزینه دارید. می‌توانید از سرور وب محلی‌ای مثل
[Caddy](https://caddyserver.com/)،‏ [nginx](https://nginx.org/)، یا
[Apache](https://httpd.apache.org/) استفاده کنید تا مطمئن شوید دارای گواهینامه «امنیت لایه انتقال» معتبری است، یا
از سرویس تونل‌زنی مثل [تونل
Cloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
یا [ngrok](https://ngrok.com/) استفاده کنید.

### نمونه استفاده از TryCloudflare {#example_using_trycloudflare}

برای این نمونه، بااستفاده از
[TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/)
ساختن تونل سریع را نمایش می‌دهیم. این کار روشی راحت و ایمن را ارائه می‌کند تا
سرور وب محلی‌تان بدون اینکه درگاه‌های ورودی‌اش باز شود افشا شود.

1. بارگیری و نصب
[`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).

2. ساختن تونلی که به درگاه سرور وب محلی‌تان هدایت می‌کند:

```sh
cloudflared tunnel --url http://127.0.0.1:<WEB_SERVER_PORT>
```

‫Cloudflare زیردامنه‌ای را ارائه می‌دهد (برای نمونه،
`acids-iceland-davidson-lb.trycloudflare.com`) تا به نقطه پایانی WebSocket دسترسی پیدا کند
و به «امنیت لایه انتقال» به‌طور خودکار رسیدگی شود. این زیردامنه را یادداشت کنید زیرا
بعداً به آن نیاز خواهید داشت.

## مرحله ۳: ساختن کلید دسترسی پویا {#step_3_create_a_dynamic_access_key}

بااستفاده از قالب [پیکربندی کلید دسترسی](../management/config)، فایل YAML مربوط به کلید دسترسی کارخواه را برای کاربرانتان تولید کنید
و نقطه‌های پایانی WebSocket را که قبلاً
در سمت سرور پیکربندی شده است به آن اضافه کنید:

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN>/<TCP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>

  udp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN>/<UDP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>
```

پس‌از تولید فایل YAML مربوط به کلید دسترسی پویا، باید آن را به
کاربرانتان بدهید. این فایل را می‌توانید در سرویس میزبانی وب ثابت میزبانی کنید یا آن را به‌صورت پویا
تولید کنید. درباره چگونگی استفاده از [کلیدهای دسترسی
پویا](../management/dynamic-access-keys) بیشتر بدانید.

## مرحله ۴: اتصال با کارخواه Outline {#step_4_connect_with_the_outline_client}

از یکی از برنامه‌های [کارخواه Outline](../../download-links) (نسخه ۱.۱۵.۰ یا بالاتر) رسمی استفاده کنید
و کلید دسترسی پویایی را که به‌تازگی ساخته‌اید به‌عنوان
ورودی سرور اضافه کنید. روی **اتصال** کلیک کنید تا تونل زدن به سرور خود را بااستفاده از
پیکربندی Shadowsocks-over-Websocket آغاز کنید.

از ابزاری مثل [IPInfo](https://ipinfo.io) استفاده کنید تا تأیید کنید اکنون
اینترنت را با سرور Outline مرور می‌کنید.
