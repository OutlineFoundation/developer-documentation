---
title: "Deploy with Automatic HTTPS Using Caddy"
sidebar_label: "HTTPS with Caddy"
---

يوضِّح هذا الدليل كيفية استخدام [Caddy](https://caddyserver.com/)، وهو خادم ويب فعّال
وسهل الاستخدام لتحسين عملية إعداد خادم Outline. إنّ إمكانات
[بروتوكول HTTPS التلقائي](https://caddyserver.com/docs/automatic-https) لخادم الويب Caddy و
إعداداته السهلة تجعل منه الخيار الأمثل لتشغيل خادم
Outline، خصوصًا في حال استخدام نقطة اتصال WebSocket.

## ما هو خادم Caddy؟

‫Caddy هو خادم ويب مفتوح المصدر معروف بسهولة استخدامه وتوافقه مع بروتوكول HTTPS التلقائي
وغيره من البروتوكولات الأخرى، إلى جانب تسهيل عملية ضبط خادم الويب و
توفير ميزات مثل ما يلي:

- **بروتوكول HTTPS التلقائي:** يحصل خادم Caddy على شهادات بروتوكول أمان طبقة النقل (TLS)
ويجدِّدها لضمان توفير اتصالات آمنة.

- **التوافق مع HTTP/3:** يتوافق Caddy مع بروتوكول HTTP/3 الأحدث لتوفير زيارات للويب
أسرع وأكثر فعالية.

- **قابلية التوسّع من خلال المكوّنات الإضافية:** يمكن توسيع نطاق خادم Caddy باستخدام المكوّنات الإضافية لإتاحة
وظائف متعدّدة، بما في ذلك خدمة الخادم الوكيل العكسي وموازنة الحمل.

## الخطوة 1: المتطلبات الأساسية

- يجب تنزيل وتثبيت [`xcaddy`](https://github.com/caddyserver/xcaddy)

## الخطوة 2: ضبط النطاق

قبل بدء استخدام Caddy، يُرجى التأكُّد من أنّ اسم النطاق تم ضبطه بشكل صحيح ليشير
إلى عنوان IP الخاص بالخادم.

- **ضبط سجلّات AAAA وA:** عليك تسجيل الدخول إلى مزوّد نظام أسماء النطاقات وضبط سجلّات AAAA
وA الخاصة بنطاقك للإشارة إلى عناوين الإصدار الرابع من بروتوكول الإنترنت (IPv4) والإصدار السادس من بروتوكول الإنترنت (IPv6) الخاصة بالخادم
على التوالي.

- **التأكُّد من سجلّات نظام أسماء النطاقات:** يجب التأكُّد من أنّ سجلّات نظام أسماء النطاقات تم ضبطها بشكل صحيح
من خلال إجراء بحث موثوق:

```sh
curl "https://cloudflare-dns.com/dns-query?name=<DOMAIN_NAME>&type=A" \
  -H "accept: application/dns-json"
```

## الخطوة 3: إنشاء إصدار Caddy مخصّص وتشغيله

باستخدام `xcaddy`، يمكنك إنشاء برنامج `caddy` ثنائي مخصّص يتضمّن الوحدة
الأساسية لخادم Outline ووحدات إضافات الخادم الأخرى التي سنحتاج إليها.

```sh
xcaddy build \
  # The example uses a YAML config, so include a YAML config adapter module.
  --with github.com/iamd3vil/caddy_yaml_adapter \
  # The Outline core server module.
  --with github.com/Jigsaw-Code/outline-ss-server/outlinecaddy
```

## الخطوة 4: ضبط خادم Caddy وتشغيله مع Outline

عليك إنشاء ملف `config.yaml` جديد بالإعدادات التالية:

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

يعبّر هذا الإعداد عن استراتيجية إعدادات Shadowsocks-over-WebSocket مع خادم
ويب يشير إلى منفذ `443`، والذي يقبل الزيارات المغلّفة عبر بروتوكول Shadowsocks باستخدام منفذَي TCP وUDP على المسارَين `TCP_PATH` و`UDP_PATH`
على التوالي.

عليك تشغيل خادم Caddy المرتبط بـ Outline باستخدام الإعدادات المُنشأة:

```sh
caddy run --config config.yaml --adapter yaml --watch
```

ويمكنك الاطّلاع على المزيد من الأمثلة عن الإعدادات في مستودع GitHub على [outline-ss-server/outlinecaddy](https://github.com/Jigsaw-Code/outline-ss-server/tree/master/outlinecaddy/examples).

## الخطوة 5: إنشاء مفتاح وصول ديناميكي

يجب إنشاء ملف YAML يتضمّن مفتاح وصول يمكن استخدامه في تطبيق &quot;عميل Outline&quot; للمستخدمين باستخدام تنسيق [الإعدادات
المتقدّمة](../management/config)، ثم تضمين نقاط نهاية WebSocket التي تم
ضبطها سابقًا في جهة الخادم:

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

بعد إنشاء ملف YAML الذي يتضمّن مفتاح الوصول الديناميكي، عليك نشره
للمستخدمين. ويمكنك استضافة الملف على خدمة استضافة ويب ثابتة أو إنشاؤه
بشكل ديناميكي. مزيد من المعلومات حول كيفية استخدام [مفاتيح الوصول
الديناميكية](../management/dynamic-access-keys)

## الخطوة 6: الربط بتطبيق &quot;عميل Outline&quot;

يجب استخدام أحد تطبيقات [عميل Outline](../../download-links)
الرسمية (الإصدار 1.15.0 والإصدارات الأحدث) ثم إضافة مفتاح الوصول الديناميكي المُنشأ حديثًا
ليعمل كإدخال للخادم. عليك النقر على **اتصال** لبدء الاتصال النفَقي بخادمك باستخدام
الإعداد Shadowsocks-over-Websocket.

يمكنك استخدام أداة مثل [IPInfo](https://ipinfo.io) للتأكُّد من أنّه يتم حاليًا تصفُّح
الإنترنت من خلال خادم Outline الخاص بك.
