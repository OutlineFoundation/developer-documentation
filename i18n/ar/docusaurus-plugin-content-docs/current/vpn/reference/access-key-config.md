---
title: "Access Key Configuration Reference"
sidebar_label: "Access Key Config"
---

## الاتصالات النفَقية

### TunnelConfig

الاتصال النفَقي هو العنصر الأعلى مستوى في إعدادات Outline؛ وذلك لأنه يحدِّد كيفية
ضبط شبكة VPN.

**التنسيق:** [ExplicitTunnelConfig](#explicittunnelconfig) |
‫[LegacyShadowsocksConfig](#legacyshadowsocksconfig) |
‫[LegacyShadowsocksURI](#legacyshadowsocksuri)

### ExplicitTunnelConfig

**التنسيق:** *struct*

**الحقول:**

- ‫`transport` ([TransportConfig](#transportconfig)): بروتوكول نقل البيانات المستخدَم في
تبادل الحِزم مع الوجهة النهائية

- ‫`error` (*struct*): المعلومات التي تصل المستخدِم في حال حدوث
خطأ بالخدمة (مثل انتهاء صلاحية المفتاح أو استهلاك الحصة المخصّصة)

    - ‫`message` (*string*): رسالة ودية تُعرض للمستخدِم

    - ‫`details` (*string*): رسالة تُعرض عندما يفتح المستخدم تفاصيل
الخطأ، وهي مفيدة في تحديد المشاكل وحلّها

يستبعد كلُّ من الحقلَين `error` و`transport` الآخر.

أمثلة ناجحة:

أمثلة بها أخطاء:

## بروتوكولات نقل البيانات

### TransportConfig

تحدِّد كيفية تبادُل الحِزم مع الوجهة النهائية.

**التنسيق:** [Interface](#interface)

أنواع Interface المتوافقة:

- `tcpudp`: [TCPUDPConfig](#tcpudpconfig)

### TCPUDPConfig

يمكن استخدام TCPUDPConfig لضبط استراتيجيات منفصلة لمنفذَي TCP وUDP.

**التنسيق:** *struct*

**الحقول:**

- ‫`tcp` ([DialerConfig](#dialerconfig)): هو "برنامج اتصال البث" المستخدَم في اتصالات
TCP.

- ‫`udp` ([PacketListenerConfig](#packetlistenerconfig)): هو "متتبِّع الحِزم"
المستخدَم في حِزم UDP.

مثال على إرسال حِزم TCP وUDP إلى نقاط نهاية مختلفة:

## نقاط النهاية

تنشئ نقاط النهاية اتصالات تؤدي إلى نقطة نهاية ثابتة. وهذا الخيار مفضَّل على
"برامج الاتصال"؛ لأنّه يتيح إجراء تحسينات خاصة بنقاط النهاية. وتنقسم نقاط النهاية إلى "نقاط نهاية للبث"
و"نقاط نهاية للحِزم".

### EndpointConfig

**التنسيق:** *string* | ‏[Interface](#interface)

نقطة النهاية *string* هي العنوان من المضيف إلى المنفذ لنقطة النهاية المحدّدة. ويتم إنشاء
الاتصال باستخدام "برنامج الاتصال" التلقائي.

أنواع Interface المتوافقة مع "نقاط نهاية البث" و"نقاط نهاية الحِزم":

- `dial`: [DialEndpointConfig](#dialendpointconfig)

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `websocket`: [WebsocketEndpointConfig](#websocketendpointconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

### DialEndpointConfig

يستخدم برنامج اتصال يتيح إنشاء الاستراتيجيات للاتصال
بعنوان ثابت.

**التنسيق:** *struct*

**الحقول:**

- ‫`address` (*string*): عنوان نقطة النهاية المستخدَم للاتصال

- ‫`dialer` ([DialerConfig](#dialerconfig)): برنامج الاتصال المستخدَم للاتصال
بالعنوان

### WebsocketEndpointConfig

تعمل الاتصالات النفَقية على بثّ وتجميع الاتصالات في حِزم وإرسالها إلى نقطة نهاية عبر بروتوكولات Websocket.

لبثّ الاتصالات، يتم تحويل كل نص إلى رسالة Websocket. ولتجميع
الاتصالات في حِزم، يتم تحويل كل حزمة إلى رسالة Websocket.

**التنسيق:** *struct*

**الحقول:**

- ‫`url` (*string*): هو عنوان URL لنقطة نهاية Websocket. ويجب أن يكون المخطَّط
`https` أو `wss` لاتصال Websocket عبر بروتوكول TLS، و`http` أو `ws` لنص Websocket
عادي.

- ‫`endpoint` ([EndpointConfig](#endpointconfig)): نقطة نهاية خادم الويب التي يتم
الاتصال بها. وفي حال غيابها، تتصل نقطة النهاية بالعنوان المرتبط بعنوان URL.

## برامج الاتصال

تنشئ برامج الاتصال اتصالات بعنوان نقطة نهاية معيّنة. وتنقسم برامج الاتصال إلى نوعَين: "برامج اتصال البثّ"
و"برامج اتصال الحِزم".

### DialerConfig

**التنسيق:** *null* | ‏[Interface](#interface)

يكون "برنامج الاتصال" التلقائي بتنسيق *القيمة الفارغة (null)*، ويستخدم اتصالات TCP
المباشرة في "برامج اتصال البثّ" واتصالات UDP المباشرة في "برامج اتصال الحِزم".

أنواع Interface المتوافقة مع "برامج اتصال البثّ" و"برامج اتصال الحِزم":

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

## متتبِّعات الحِزم

يُنشئ "متتبِّع الحِزم" اتصالاً من خلال الحِزم غير المحدودة والذي يمكن أن يُستخدم
لإرسال حِزم إلى وجهات متعددة.

### PacketListenerConfig

**التنسيق:** *null* | ‏[Interface](#interface)

يكون "متتبِّع الحِزم" التلقائي بتنسيق *القيمة الفارغة (null)*، وهو
"متتبِّع حِزم" خاص ببروتوكول UDP.

أنواع Interface المتوافقة:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksPacketListenerConfig](#shadowsocksconfig)

## الاستراتيجيات

### Shadowsocks

#### LegacyShadowsocksConfig

يمثِّل الإعداد LegacyShadowsocksConfig "اتصالاً نفَقيًا" يستخدم Shadowsocks
على أنّه بروتوكول نقل البيانات. ويُطبِّق هذا الإعداد التنسيق القديم للتوافق مع الأنظمة القديمة.

**التنسيق:** *struct*

**الحقول:**

- ‫`server` (*string*): المضيف الذي يتم الاتصال به

- ‫`server_port` (*number*): رقم المنفذ الذي يتم الاتصال به

- ‫`method` (*string*): [رمز AEAD](https://shadowsocks.org/doc/aead.html#aead-ciphers) المستخدَم

- ‫`password` (*string*): يُستخدَم لإنشاء مفتاح التشفير

- ‫`prefix` (*string*): طريقة [إخفاء
البادئات](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/) المستخدَمة
وتتوافق مع اتصالات البثّ والحِزم.

مثال:

#### LegacyShadowsocksURI

يُمثّل الإعداد LegacyShadowsocksURI "اتصالاً نفَقيًا" يستخدم بروتوكول Shadowsocks
كنقطة اتصال.
ويُطبِّق هذا الإعداد تنسيق عنوان URL القديم للتوافق مع الأنظمة القديمة.

**التنسيق:** *string*

يُرجى الاطّلاع على [تنسيق URI لبروتوكول Shadowsocks
القديم](https://shadowsocks.org/doc/configs.html#uri-and-qr-code) و[مخطَّط URI رقم
SIP002](https://shadowsocks.org/doc/sip002.html)، مع العِلم أنّنا لا نوفِّر المكوّنات الإضافية.

مثال:

#### ShadowsocksConfig

يُمثِّل الإعداد ShadowsocksConfig "برامج اتصال البثّ" أو "برامج اتصال الحِزم" وأيضًا "متتبِّع
الحِزم" الذي يستخدِم Shadowsocks.

**التنسيق:** *struct*

**الحقول:**

- ‫`endpoint` ([EndpointConfig](#endpointconfig)): نقطة نهاية Shadowsocks
التي يتم الاتصال بها

- ‫`cipher` (*string*): [رمز AEAD](https://shadowsocks.org/doc/aead.html#aead-ciphers) المستخدَم

- ‫`secret` (*string*): يُستخدَم لإنشاء مفتاح التشفير

- ‫`prefix` (*string*، اختياري): طريقة [إخفاء
البادئات](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/) المستخدَمة
وتتوافق مع اتصالات البثّ والحِزم.

مثال:

## أنواع الكائن الوصفي

### FirstSupportedConfig

يستخدم هذا الإعداد أول إعداد متوافق مع التطبيق. وهو طريقة
تُستخدم لتضمين الإعدادات الجديدة مع مواصلة التوافق مع الإعدادات القديمة.

**التنسيق:** *struct*

**الحقول:**

- ‫`options` ([EndpointConfig[]](#endpointconfig) |
‫[DialerConfig[]](#dialerconfig) |
‫[PacketListenerConfig[]](#packetlistenerconfig)): قائمة بالخيارات
المتاحة

مثال:

### الواجهة (Interface)

تُتيح الواجهات اختيار أحد عمليات الاستخدام المتعددة. وتستخدم هذه الواجهات الحقل
`$type` لتحديد نوع الإعدادات التي تُمثّلها.

مثال:
