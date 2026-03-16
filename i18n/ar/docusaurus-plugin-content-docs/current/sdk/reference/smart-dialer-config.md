---
title: "إعدادات برنامج الاتصال الذكي"
sidebar_label: "إعدادات برنامج الاتصال الذكي"
---

يبحث **برنامج الاتصال الذكي** عن استراتيجية لإزالة حظر نظام أسماء النطاقات وبروتوكول أمان طبقة النقل (TLS) في
قائمة نطاقات تجريبية معيّنة، وذلك من خلال ملف إعداد يحتوي على عدة استراتيجيات
يختار من بينها.

## إعدادات YAML لبرنامج الاتصال الذكي {#yaml_config_for_the_smart_dialer}

يُستخدم ملف إعداد بتنسيق YAML لضبط إعدادات "برنامج الاتصال الذكي"، وفي ما يلي مثال على هذا:

```yaml
dns:
  - system: {}
  - https:
      name: 8.8.8.8
  - https:
      name: 9.9.9.9
tls:
  - ""
  - split:2
  - tlsfrag:1

fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

### إعدادات نظام أسماء النطاقات {#dns_configuration}

- يحدّد حقل `dns` قائمة ببرامج تعيين نظام أسماء النطاقات لاختبارها.

- يمكن أن يكون برنامج تعيين نظام أسماء النطاقات من أحد الأنواع التالية:

    - ‫`system`: يستخدم هذا النوع برنامج التعيين الخاص بالنظام، ويتم تحديده باستخدام عنصر فارغ.

    - ‫`https`: يستخدم هذا النوع برنامج تعيين مشفَّرًا يعتمد على "معالجة نظام أسماء النطاقات عبر بروتوكول HTTPS"‏ (DoH).

    - ‫`tls`: يستخدم هذا النوع برنامج تعيين مشفَّرًا يعتمد على "معالجة نظام أسماء النطاقات عبر بروتوكول TLS" ‏(DoT).

    - ‫`udp`: يستخدم هذا النوع برنامج تعيين يعتمد على بروتوكول UDP.

    - ‫`tcp`: يستخدم هذا النوع برنامج تعيين يعتمد على بروتوكول TCP.

#### برنامج تعيين يعتمد على "معالجة نظام أسماء النطاقات عبر بروتوكول HTTPS"‏ (DoH) {#dns-over-https_resolver_doh}

```yaml
https:
  name: dns.google
  address: 8.8.8.8
```

- ‫`name`: اسم نطاق خادم "معالجة نظام أسماء النطاقات عبر بروتوكول HTTPS"‏ (DoH).

- ‫`address`: الإعداد من المضيف إلى المنفذ لخادم "معالجة نظام أسماء النطاقات عبر بروتوكول HTTPS"‏ (DoH)، والقيمة التلقائية هي `name`:443.

#### برنامج تعيين يعتمد على "معالجة نظام أسماء النطاقات عبر بروتوكول TLS" ‏(DoT). {#dns-over-tls_resolver_dot}

```yaml
tls:
  name: dns.google
  address: 8.8.8.8
```

- ‫`name`: اسم نطاق خادم "معالجة نظام أسماء النطاقات عبر بروتوكول TLS" ‏(DoT).

- ‫`address`: الإعداد من المضيف إلى المنفذ لخادم "معالجة نظام أسماء النطاقات عبر بروتوكول TLS" ‏(DoT)، والقيمة التلقائية هي `name`:853.

#### برنامج تعيين يعتمد على بروتوكول UDP {#udp_resolver}

```yaml
udp:
  address: 8.8.8.8
```

- ‫`address`: الإعداد من المضيف إلى المنفذ لبرنامج تعيين يعتمد على بروتوكول UDP.

#### برنامج تعيين يعتمد على بروتوكول TCP {#tcp_resolver}

```yaml
tcp:
  address: 8.8.8.8
```

- ‫`address`: الإعداد من المضيف إلى المنفذ لبرنامج تعيين يعتمد على بروتوكول TCP.

### إعدادات بروتوكول أمان طبقة النقل (TLS) {#tls_configuration}

- يحدّد حقل `tls` قائمة بأساليب نقل البيانات عبر بروتوكول TLS لاختبارها.

- إنّ كل أسلوب لنقل البيانات عبر بروتوكول TLS هو سلسلة تحدّد أسلوب النقل المطلوب استخدامه.

- على سبيل المثال، يحدّد `override:host=cloudflare.net|tlsfrag:1` أسلوب النقل
الذي يستخدِم التخفي عبر النطاقات مع Cloudflare وتقسيم بروتوكول TLS. ولمزيد من التفاصيل، يمكنك الاطّلاع على
[مستند الإعدادات](https://pkg.go.dev/github.com/OutlineFoundation/outline-sdk/x/configurl#hdr-Config_Format).

### الإعدادات الاحتياطية {#fallback_configuration}

تُستخدَم الإعدادات الاحتياطية في حال تعذُّر اتصال أيّ استراتيجية بدون خادم
وكيل. على سبيل المثال، تعمل هذه الإعدادات على تحديد خادم وكيل احتياطي لإعادة اتصال
المستخدم. ويُرجى العِلم بأنّ استخدام الإعداد الاحتياطي سيؤدي إلى بطء بدء الاتصال، وذلك لتعذُّر استخدام استراتيجيات
نظام أسماء النطاقات/ بروتوكول TLS أو انتهاء المهلة المحدّدة.

يجب أن تكون سلاسل الإعدادات الاحتياطية:

- سلسلة إعدادات `StreamDialer` صالحة مثل تلك المحدّدة في [`configurl`](https://pkg.go.dev/github.com/OutlineFoundation/outline-sdk/x/configurl#hdr-Proxy_Protocols).

- عنصر إعدادات Psiphon صالحًا مثل العنصر الثانوي للحقل `psiphon`.

#### مثال على خادم Shadowsocks {#shadowsocks_server_example}

```yaml
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

#### مثال على خادم SOCKS5 {#socks5_server_example}

```yaml
fallback:
  - socks5://[USERINFO]@[HOST]:[PORT]
```

#### مثال على إعدادات Psiphon {#psiphon_config_example}

لاستخدام شبكة [Psiphon](https://psiphon.ca/):

1. عليك التواصل مع فريق دعم Psiphon لاستخدام الإعدادات المطلوبة للوصول إلى
الشبكة، وقد يتطلب ذلك توقيع عقد معيّن.

2. عليك إضافة إعدادات Psiphon المستلَمة إلى القسم `fallback` ضِمن إعدادات
"برنامج الاتصال الذكي". وبما أنّ تنسيق JSON يتوافق مع YAML، يمكنك نسخ ولصق
إعدادات Psiphon مباشرةً في القسم `fallback` على النحو التالي:

```yaml
fallback:
  - psiphon: {
      "PropagationChannelId": "FFFFFFFFFFFFFFFF",
      "SponsorId": "FFFFFFFFFFFFFFFF",
      "DisableLocalSocksProxy" : true,
      "DisableLocalHTTPProxy" : true,
      ...
    }
```

### كيفية استخدام برنامج الاتصال الذكي {#how_to_use_the_smart_dialer}

لاستخدام برنامج الاتصال الذكي، عليك إنشاء عنصر `StrategyFinder` وطلب
طريقة `NewDialer` وذلك لتحديد قائمة نطاقات الاختبار وملف الإعدادات بتنسيق YAML.
تعرِض الطريقة `NewDialer` العنصر `transport.StreamDialer` الذي يمكن
استخدامه لإنشاء الاتصالات باستخدام الاستراتيجية التي تم العثور عليها. على سبيل المثال:

```go
finder := &smart.StrategyFinder{
    TestTimeout:  5 * time.Second,
    LogWriter:   os.Stdout,
    StreamDialer: &transport.TCPDialer{},
    PacketDialer: &transport.UDPDialer{},
}

configBytes := []byte(`
dns:
  - system: {}
  - https:
      name: 8.8.8.8
  - https:
      name: 9.9.9.9
tls:
  - ""
  - split:2
  - tlsfrag:1
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
`)

dialer, err := finder.NewDialer(
  context.Background(),
  []string{"www.google.com"},
  configBytes
)
if err != nil {
    // Handle error.
}

// Use dialer to create connections.
```

هذا المثال بسيط وقد يلزم تعديله ليتلاءم مع حالة الاستخدام المحدّدة.
