---
title: "Configure Access Keys"
sidebar_label: "Configure Access Keys"
---

يستخدم Outline إعدادات مستنِدة إلى YAML لتحديد مَعلمات شبكة VPN والتعامل مع
زيارات TCP أو UDP. ويمكن استخدام هذه الإعدادات مع إعدادات أخرى على عدة مستويات،
ما يتيح عمليات إعداد مرنة وقابلة للتوسيع.

ويُحدِّد الإعداد من المستوى الأعلى إعدادات
[TunnelConfig](../reference/access-key-config#tunnelconfig).

## أمثلة

ستظهر إعدادات Shadowsocks بالشكل التالي:

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

يمكنك ملاحظة كيف يمكننا حاليًا تشغيل TCP وUDP على منافذ أو نقاط نهاية مختلفة
ببادئات مختلفة.

يمكنك استخدام علامات ارتساء YAML ومفتاح دمج `<<` لتجنُّب التكرار كالتالي:

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

يمكن حاليًا إنشاء استراتيجيات وتطبيق تقنية الاتصال بعدة خوادم كالتالي:

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

في حال حظر بروتوكولات "التمويه" مثل بروتوكول Shadowsocks، يمكنك
استخدام إعدادات Shadowsocks-over-Websocket. ويمكنك الاطّلاع على [مثال على إعدادات
الخادم](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml)
لمعرفة كيفية نشره. وستظهر الإعدادات المرتبطة بالعميل كالتالي:

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

يُرجى العِلم بأنّه يمكن استخدام نقطة نهاية Websocket والاستفادة
منها في تفادي الحظر استنادًا إلى نظام أسماء النطاقات كالتالي:

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

للتأكّد من التوافق مع مختلف إصدارات "عميل Outline"، يُرجى استخدام
خيار `first-supported` في الإعدادات. وتكمُن أهمية هذا الإجراء
عند إضافة استراتيجيات وميزات جديدة إلى Outline؛ لأنّه قد لا يكون كل المستخدمين
حدَّثوا تطبيق "عميل Outline" إلى أحدث إصدار. ومن خلال استخدام `first-supported`، يمكنك
توفير إعداد واحد يعمل بسلاسة على كل المنصات
وإصدارات "عميل Outline" مع ضمان التوافق مع الأنظمة القديمة وتوفير تجربة متّسقة
للمستخدم.

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
