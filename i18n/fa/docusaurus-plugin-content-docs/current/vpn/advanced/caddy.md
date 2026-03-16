---
title: "‫HTTPS خودکار با Caddy"
sidebar_label: "‫HTTPS خودکار با Caddy"
---

این راهنما توضیح می‌دهد چطور از [Caddy](https://caddyserver.com/)، سرور وب قدرتمند
و کاربرپسند، استفاده کنید تا راه‌اندازی سرور Outline خود را بهبود دهید. قابلیت‌های
[اچ‌تی‌تی‌پی‌اس خودکار](https://caddyserver.com/docs/automatic-https) Caddy و
پیکربندی انعطاف‌پذیر آن، Caddy را به انتخابی عالی برای ارائه سرور Outline شما
بدل می‌کند، به‌ویژه وقتی از حمل‌ونقل WebSocket استفاده می‌کنید.

## ‫Caddy چیست؟ {#what_is_caddy}

‫Caddy سرور وب متن‌بازی است که به‌خاطر استفاده آسان، اچ‌تی‌تی‌پی‌اس،
و پشتیبانی پروتکل‌های مختلف معروف است. پیکربندی‌های سرور وب را ساده می‌کند و
ویژگی‌هایی مثل موارد زیر را ارائه می‌دهد:

- **اچ‌تی‌تی‌پی‌اس خودکار:** Caddy به‌طور خودکار گواهینامه‌های «امنیت لایه انتقال»
را دریافت و تمدید می‌کند تا اتصالات ایمن را تضمین کند.

- **پشتیبانی HTTP/3:**‏ Caddy جدیدترین پروتکل HTTP/3 را برای
ترافیک وب سریع‌تر و کارآمدتر پشتیبانی می‌کند.

- **توسعه‌پذیر با افزایه‌ها:** Caddy می‌تواند با افزونه‌ها توسعه یابد تا
عملکردهای مختلفی را، ازجمله پراکسی معکوس و متوازن کردن بارگیری، پشتیبانی کند.

## مرحله ۱: پیش‌نیازها {#step_1_prerequisites}

- بارگیری و نصب کردن [`xcaddy`](https://github.com/caddyserver/xcaddy)

## مرحله ۲: پیکربندی دامنه {#step_2_configure_your_domain}

پیش‌از راه‌اندازی کردن Caddy، مطمئن شوید نام دامنه‌تان به‌درستی پیکربندی شده است تا
به نشانی IP سرورتان هدایت کند.

- **تنظیم کردن ساختارهای A/AAAA:** به سیستم ارائه‌دهنده ساناد خود وارد شوید و ساختارهای A و AAAA را
برای دامنه‌تان تنظیم کنید تا به‌ترتیب به نشانی‌های «پروتکل اینترنتی نسخه ۴» و «پروتکل اینترنتی نسخه ۶» سرورتان
هدایت شود.

- **تأیید کردن ساختارهای ساناد:** ساختارهای سانادی را تأیید کنید که به‌درستی با
جستجوی معتبری تنظیم شده‌اند:

```sh
curl "https://cloudflare-dns.com/dns-query?name=<DOMAIN_NAME>&type=A" \
  -H "accept: application/dns-json"
```

## مرحله ۳: ساختن و اجرای ساختار سفارشی Caddy {#build-and-run}

بااستفاده از`xcaddy` می‌توانید دودویی سفارشی `caddy` بسازید که شامل واحد اصلی سرور Outline
و واحدهای دیگر افزونه سرور که به آن‌ها نیاز دارید باشد.

```sh
xcaddy build \
  # The example uses a YAML config, so include a YAML config adapter module.
  --with github.com/iamd3vil/caddy_yaml_adapter \
  # The Outline core server module.
  --with github.com/OutlineFoundation/outline-ss-server/outlinecaddy
```

## مرحله ۴: پیکربندی و اجرای سرور Caddy با Outline {#step_4_configure_and_run_the_caddy_server_with_outline}

فایل `config.yaml` جدیدی را با پیکربندی‌های زیر بسازید:

```yaml
apps:
  http:
    servers:
      server1:
        listen:
          - ":443"
        routes:
          - match:
            - host:
              - <DOMAIN_NAME>
            - path:
              - /<TCP_PATH>
            handle:
            - handler: websocket2layer4
              type: stream
              connection_handler: ss1
          - match:
            - host:
              - <DOMAIN_NAME>
            - path:
              - /<UDP_PATH>
            handle:
              - handler: websocket2layer4
                type: packet
                connection_handler: ss1
  outline:
    shadowsocks:
      replay_history: 10000
    connection_handlers:
      - name: ss1
        handle:
          handler: shadowsocks
          keys:
            - id: user-1
              cipher: chacha20-ietf-poly1305
              secret: <SHADOWSOCKS_SECRET>
```

این پیکربندی نشان‌دهنده راهبرد Shadowsocks-over-WebSockets است که با
سرور وبی در درگاه `443` می‌شنود و ترافیک‌های شکسته‌شده Shadowsocks به‌صورت TCP و UDP را
به‌ترتیب در مسیرهای `TCP_PATH` و `UDP_PATH`
می‌پذیرد.

اجرا کردن سرور Caddy توسعه‌یافته با Outline بااستفاده از پیکربندی ساخته‌شده:

```sh
caddy run --config config.yaml --adapter yaml --watch
```

نمونه‌های بیشتر برای پیکربندی را می‌توانید در [outline-ss-server/outlinecaddy GitHub
repo](https://github.com/OutlineFoundation/outline-ss-server/tree/master/outlinecaddy/examples) ببینید.

## مرحله ۵: ساختن کلید دسترسی پویا {#step_5_create_a_dynamic_access_key}

بااستفاده از قالب [پیکربندی پیشرفته](../management/config)، فایل YAML مربوط به کلید دسترسی کارخواه را برای کاربرانتان تولید کنید
و نقطه‌های پایانی WebSocket را
که قبلاً در سمت سرور پیکربندی شده است به آن اضافه کنید:

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN_NAME>/<TCP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>

  udp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN_NAME>/<UDP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>
```

پس‌از تولید فایل YAML مربوط به کلید دسترسی پویا، باید آن را به
کاربرانتان بدهید. این فایل را می‌توانید در سرویس میزبانی وب ثابت میزبانی کنید یا آن را به‌صورت پویا
تولید کنید. درباره چگونگی استفاده از [کلیدهای دسترسی
پویا](../management/dynamic-access-keys) بیشتر بدانید.

## مرحله ۶: اتصال با کارخواه Outline {#step_6_connect_with_the_outline_client}

از یکی از برنامه‌های [کارخواه Outline](../../download-links) (نسخه ۱.۱۵.۰ یا بالاتر) رسمی استفاده کنید
و کلید دسترسی پویایی را که به‌تازگی ساخته‌اید به‌عنوان
ورودی سرور اضافه کنید. روی **اتصال** کلیک کنید تا تونل زدن به سرور خود را بااستفاده از
پیکربندی Shadowsocks-over-Websocket آغاز کنید.

از ابزاری مثل [IPInfo](https://ipinfo.io) استفاده کنید تا تأیید کنید اکنون
اینترنت را با سرور Outline مرور می‌کنید.
