---
title: "پیکربندی کلید دسترسی"
sidebar_label: "پیکربندی کلید دسترسی"
---

‫Outline از پیکربندی برپایه YAML استفاده می‌کند تا پارامترهای وی‌پی‌ان را تعیین کند و
به ترافیک TCP/UDP رسیدگی کند. این پیکربندی ترکیب‌پذیری را در چندین سطح پشتیبانی می‌کند
و راه‌اندازی‌های توسعه‌پذیر و منعطف را فعال می‌کند.

پیکربندی سطح بالا
[TunnelConfig](../reference/access-key-config#tunnelconfig) را مشخص می‌کند.

## مثال‌ها {#examples}

پیکربندی معمول Shadowsocks به این شکل است:

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks
    endpoint: ss.example.com:80
    cipher: chacha20-ietf-poly1305
    secret: SECRET
    prefix: "POST "  # HTTP request

  udp:
    $type: shadowsocks
    endpoint: ss.example.com:53
    cipher: chacha20-ietf-poly1305
    secret: SECRET
    prefix: "\u0097\u00a7\u0001\u0000\u0000\u0001\u0000\u0000\u0000\u0000\u0000\u0000"  # DNS query
```

ببینید اکنون چطور می‌توانیم TCP و UDP را در درگاه‌ها یا نقطه‌های پایانی مختلف و با
پیشوندهای مختلف اجرا کنیم.

می‌توانید از لنگرهای YAML و کلید ادغام `<<` استفاده کنید تا از موارد تکراری پرهیز کنید:

```yaml
transport:
  $type: tcpudp

  tcp:
    <<: &shared
      $type: shadowsocks
      endpoint: ss.example.com:4321
      cipher: chacha20-ietf-poly1305
      secret: SECRET
    prefix: "POST "

  udp: *shared
```

اکنون نوشتن راهبردها و پیکربندی کردن چندپراکسی امکان‌پذیر شده است:

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: dial
      address: exit.example.com:4321
      dialer:
        $type: shadowsocks
        address: entry.example.com:4321
        cipher: chacha20-ietf-poly1305
        secret: ENTRY_SECRET

    cipher: chacha20-ietf-poly1305
    secret: EXIT_SECRET

  udp: *shared
```

درصورت مسدود شدن پروتکل‌های «شبیه هیچ‌چیز» مثل Shadowsocks، می‌توانید
از Shadowsocks-over-Websockets استفاده کنید. برای نحوه استفاده از آن، [پیکربندی
نمونه سرور](https://github.com/OutlineFoundation/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml)
را ببینید. پیکربندی کارخواه به این شکل است:

```yaml
transport:
  $type: tcpudp
  tcp:
    $type: shadowsocks
    endpoint:
        $type: websocket
        url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/tcp
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET

  udp:
    $type: shadowsocks
    endpoint:
        $type: websocket
        url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/udp
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET
```

توجه کنید که نقطه پایانی Websocket هم به‌نوبه خود می‌تواند نقطه پایانی‌ای داشته باشد که
می‌تواند بالا برده شود تا مسدودیت برپایه ساناد را دور بزند:

```yaml
transport:
  $type: tcpudp
  tcp:
    $type: shadowsocks
    endpoint:
        $type: websocket
        url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/tcp
        endpoint: cloudflare.net:443
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET

  udp:
    $type: shadowsocks
    endpoint:
        $type: websocket
        url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/udp
        endpoint: cloudflare.net:443
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET
```

برای اطمینان از سازگاری درسراسر نسخه‌های مختلف کارخواه Outline، از گزینه
`first-supported` در پیکربندی خود استفاده کنید. این امر اهمیت ویژه‌ای دارد
زیرا ویژگی‌ها و راهبردهای جدیدی به Outline اضافه شده است، و ممکن است همه کاربران
جدیدترین نرم‌افزار کارخواه را نداشته باشند. بااستفاده از `first-supported`، می‌توانید
پیکربندی تکی ایجاد کنید که بدون وقفه درسراسر نسخه‌های پلاتفرم‌ها
و کارخواهان کار کند و مطمئن شوید که سازگاری با نسخه قدیمی انجام می‌شود و تجربه
کاربر یکپارچه است.

```yaml
transport:
  $type: tcpudp
  tcp:
    $type: shadowsocks
    endpoint:
      $type: first-supported
      options:
        - $type: websocket
          url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/tcp
        - ss.example.com:4321
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET

  udp:
    $type: shadowsocks
    endpoint:
      $type: first-supported
      options:
        - $type: websocket
          url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/udp
        - ss.example.com:4321
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET
```
