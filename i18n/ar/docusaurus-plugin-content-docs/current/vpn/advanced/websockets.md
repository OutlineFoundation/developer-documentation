---
title: "إعدادات Shadowsocks-over-WebSocket"
sidebar_label: "إعدادات Shadowsocks-over-WebSocket"
---

*الإصدار 1.15.0 من تطبيق "عميل Outline" والإصدارات الأحدث*

يقدِّم هذا الدليل التوجيهي جولة تفصيلية لتوضيح كيفية تطبيق
إعدادات Shadowsocks-over-WebSocket، وهي تقنية فعّالة لتفادي الرقابة في
البيئات التي يتم فيها حظر اتصالات Shadowsocks. ومن خلال تغليف
زيارات بروتوكولات Shadowsocks ببروتوكولات WebSocket، يمكنك إخفاء هذه الزيارات كأنّها زيارات عادية لمواقع ويب
، ما يعزِّز المرونة وتسهيل الاستخدام.


:::note
تُتاح إعدادات Shadowsocks-over-WebSocket في الإصدار 1.15.0 من تطبيق "عميل Outline" والإصدارات الأحدث. ويجب تعديل الإعدادات الحالية لإتاحة الإصدارات القديمة من التطبيق.
:::

## الخطوة 1: ضبط خادم Outline وتشغيله {#step_1_configure_and_run_an_outline_server}

عليك إنشاء ملف `config.yaml` جديد بالإعدادات التالية:

```yaml
web:
  servers:
    - id: server1
      listen:
        - "127.0.0.1:<WEB_SERVER_PORT>"

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

:::tip
يُرجى الحفاظ على سرية `path` لتجنُّب إجراء اختبارات عليه، لأنه يعمل كنقطة نهاية سرية. ويُنصح باستخدام مسار طويل تم إنشاؤه عشوائيًا.
:::


يجب تنزيل وتشغيل
[`outline-ss-server`](https://github.com/OutlineFoundation/outline-ss-server/releases) الأحدث
باستخدام الإعدادات التي تم إنشاؤها:

```sh
outline-ss-server -config=config.yaml
```

## الخطوة 2: السماح بالوصول إلى خادم الويب {#step_2_expose_the_web_server}

لجعل خادم ويب WebSocket متاحًا للجميع، يجب السماح بالوصول إليه
على الإنترنت وضبط
[بروتوكول أمان طبقة النقل (TLS)](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security).
ولديك عدة خيارات لتنفيذ هذا الإجراء، منها استخدام خادم ويب محلي مثل
[Caddy](https://caddyserver.com/) أو [nginx](https://nginx.org/) أو
[Apache](https://httpd.apache.org/) مع التأكّد من توفُّر شهادة بروتوكول TLS سارية، أو
استخدام خدمة اتصال نفَقي مثل [Cloudflare
Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
أو [ngrok](https://ngrok.com/).

### مثال على استخدام خدمة TryCloudflare {#example_using_trycloudflare}


:::caution
خدمة TryCloudflare مخصّصة للإصدارات التجريبية ولأغراض الاختبارات فقط.
:::

في هذا المثال، سنستخدم خدمة
[TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/)
في إنشاء اتصال نفَقي سريع. ويوفِّر هذا طريقة سهلة وآمنة للسماح بالوصول إلى
خادم الويب المحلي بدون فتح منافذ على الشبكة للاتصالات الواردة.

1. يجب تنزيل وتثبيت [`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).

2. عليك إنشاء اتصال نفَقي يشير إلى منفذ خادم الويب المحلي:

```sh
cloudflared tunnel --url http://127.0.0.1:<WEB_SERVER_PORT>
```

سيقدّم Cloudflare نطاقًا فرعيًا (مثل:
`acids-iceland-davidson-lb.trycloudflare.com`) للوصول إلى نقطة نهاية بروتوكول WebSocket
والتعامل تلقائيًا مع بروتوكول TLS. يُرجى الاحتفاظ بهذا النطاق الفرعي؛ لأنّك ستحتاجه
بعد ذلك.

## الخطوة 3: إنشاء مفتاح وصول ديناميكي {#step_3_create_a_dynamic_access_key}

عليك إنشاء ملف YAML يتضمّن مفتاح وصول يمكن استخدامه في تطبيق "عميل Outline" للمستخدمين باستخدام تنسيق [إعدادات
مفاتيح الوصول](../management/config)، ثمّ تضمين نقاط نهاية WebSocket التي تم ضبطها
سابقًا في جهة الخادم:

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

بعد إنشاء ملف YAML الذي يتضمّن مفتاح الوصول الديناميكي، يجب نشره
للمستخدمين. ويمكنك استضافة الملف على خدمة استضافة ويب ثابتة أو إنشاؤه
بشكل ديناميكي. مزيد من المعلومات حول كيفية استخدام [مفاتيح الوصول
الديناميكية](../management/dynamic-access-keys)

## الخطوة 4: الربط بتطبيق "عميل Outline" {#step_4_connect_with_the_outline_client}

يجب استخدام أحد تطبيقات [عميل Outline](../../download-links)
الرسمية (الإصدار 1.15.0 والإصدارات الأحدث) ثم إضافة مفتاح الوصول الديناميكي المُنشأ حديثًا
ليعمل كإدخال للخادم. عليك النقر على **ربط** لبدء الاتصال النفَقي بخادمك باستخدام
الإعداد Shadowsocks-over-Websocket.

يمكنك استخدام أداة مثل [IPInfo](https://ipinfo.io) للتأكّد من أنّه يتم حاليًا تصفُّح
الإنترنت من خلال خادم Outline الخاص بك.
