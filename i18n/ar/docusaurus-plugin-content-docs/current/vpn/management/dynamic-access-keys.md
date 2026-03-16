---
title: "مفاتيح الوصول الديناميكية"
sidebar_label: "مفاتيح الوصول الديناميكية"
---

يوفّر Outline نوعَين من مفاتيح الوصول: الثابتة والديناميكية. يتم ترميز كل
معلومات الاتصال في مفاتيح الوصول الثابتة نفسها، بينما يتم ترميز
موقع معلومات الاتصال في مفاتيح الوصول الديناميكية، ما يتيح لك تخزين تلك المعلومات
بعيدًا وتغييرها عند الحاجة. ويعني هذا أنّه يمكن تعديل
إعدادات الخادم دون الحاجة إلى إنشاء مفاتيح جديدة ونشرها
للمستخدمين. ويوضِّح هذا المستند كيفية استخدام مفاتيح الوصول الديناميكية لإدارة خادم Outline بطريقة أكثر
مرونة وفعالية.

هناك ثلاثة تنسيقات لتحديد معلومات الوصول التي ستستخدِمها
مفاتيح الوصول الديناميكية:

### استخدام رابط `ss://` {#use_an_ss_link}

*الإصدار 1.8.1 من تطبيق "عميل Outline" والإصدارات الأحدث*

يمكنك استخدام رابط `ss://` حالي مباشرةً. وتعتبر هذه الطريقة مثالية إذا كنت
لست بحاجة إلى تغيير الخادم أو المنفذ أو طريقة التشفير بشكل متكرر، ولكنك ما زلت بحاجة إلى
توفُّر إمكانية تعديل عنوان الخادم.

**مثال:**

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

### استخدام عنصر JSON {#use_a_json_object}

*الإصدار 1.8.0 من تطبيق "عميل Outline" والإصدارات الأحدث*

توفّر هذه الطريقة مرونة أكبر لإدارة جميع جوانب اتصال
Outline الخاص بالمستخدمين. ويمكنك تعديل الخادم والمنفذ وكلمة المرور وطريقة
التشفير بهذه الطريقة.

**مثال:**

```json
{
  "server": "outline-server.example.com",
  "server_port": 8388,
  "password": "example",
  "method": "chacha20-ietf-poly1305"
}
```

- ‫**server:** النطاق أو عنوان IP الخاص بخادم VPN

- ‫**server_port:** رقم المنفذ الذي يتم تشغيل خادم VPN فيه

- ‫**password:** كلمة المرور المطلوبة للاتصال بشبكة VPN

- ‫**method:** طريقة التشفير التي تستخدمها شبكة VPN. يُرجى الاطّلاع على
[رموز AEAD](https://shadowsocks.org/doc/aead.html) المتوافقة مع بروتوكول Shadowsocks

### استخدام عنصر YAML {#use_a_yaml_object}

*الإصدار 1.15.0 من تطبيق "عميل Outline" والإصدارات الأحدث*

تشبه هذه الطريقة طريقة JSON السابقة ولكنها توفّر مرونة أكثر
من خلال الاستفادة من تنسيق الإعدادات المتقدّمة لـ Outline. ويمكنك
تعديل الخادم والمنفذ وكلمة المرور وطريقة التشفير والمزيد.

**مثال:**

```yaml
transport:
  $type: tcpudp
  tcp:
    $type: shadowsocks
    endpoint: outline-server.example.com:8388
    cipher: chacha20-ietf-poly1305
    secret: example
  udp:
    $type: shadowsocks
    endpoint: outline-server.example.com:8388
    cipher: chacha20-ietf-poly1305
    secret: example
```

- ‫**transport:** يحدِّد بروتوكولات نقل البيانات التي سيتم استخدامها (TCP وUDP
في هذه الحالة)

- ‫**tcp/udp:** يحدِّد إعدادات كل بروتوكول

    - ‫**$type:** يحدِّد نوع الإعداد، في هذه الحالة shadowsocks

    - ‫**endpoint:** نطاق أو عنوان IP ومنفذ خادم VPN

    - ‫**secret:** كلمة المرور المطلوبة للاتصال بشبكة VPN

    - ‫**cipher:** طريقة التشفير التي تستخدمها شبكة VPN. يُرجى الاطّلاع على
[رموز AEAD](https://shadowsocks.org/doc/aead.html) المتوافقة
مع بروتوكول Shadowsocks

يُرجى الاطّلاع على [إعدادات مفاتيح الوصول](config) لمزيد من التفاصيل حول جميع الطرق
التي يمكنك استخدامها لضبط إمكانية الوصول إلى خادم Outline، بما في ذلك بروتوكولات نقل البيانات ونقاط النهاية
وبرامج الاتصال ومتتبِّعات الحِزم.

## استخراج معلومات الوصول من مفتاح وصول ثابت {#extract_access_information_from_a_static_key}

في حال كان لديك مفتاح وصول ثابت حاليًا، يمكنك استخراج المعلومات لإنشاء
مفتاح وصول ديناميكي استنادًا إلى عناصر JSON أو YAML. وتكون مفاتيح الوصول الثابتة
بالنمط التالي:

```none
SS-URI = "ss://" userinfo "@" hostname ":" port [ "/" ] [ "#" tag ]
userinfo = websafe-base64-encode-utf8(method  ":" password)
           method ":" password
```

مثال:

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

- **الخادم (Server):** `outline-server.example.com`

- **منفذ الخادم (Server Port):** `8388`

- **معلومات المستخدم (User Info):** `Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl` هي معلومات تم فك ترميزها بتنسيق
[base64](https://en.wikipedia.org/wiki/Base64) باستخدام أداة مثل [مجموعة أدوات وحدة تحكُّم
المشرف في Google
للترميز أو فكّه](https://toolbox.googleapps.com/apps/encode_decode/)

    - **طريقة التشفير (Method)**: `chacha20-ietf-poly1305`

    - **كلمة المرور (Password)** `example`

## اختيار منصة استضافة {#choose_a_hosting_platform}

والآن بعد فهم كيفية إنشاء مفاتيح الوصول الديناميكية، من المُهمّ
اختيار منصة استضافة مناسبة لإعدادات مفاتيح الوصول. وعند تنفيذ هذا الإجراء،
يُرجى الأخذ بعين الاعتبار بعض العوامل مثل موثوقية المنصة
وأمانها وسهولة استخدامها ومقاومتها للرقابة. هل ستوفّر هذه المنصة معلومات مفاتيح الوصول باستمرار
بدون فترة توقف عن العمل؟ هل تقدِّم هذه المنصة
إجراءات أمان مناسبة لحماية إعداداتك؟ ما مدى سهولة إدارة
معلومات مفاتيح الوصول على هذه المنصة؟ هل يمكن الوصول إلى تلك المنصة في المناطق
التي يُفرض فيها رقابة على الإنترنت؟

في الحالات التي يكون فيها الوصول إلى المعلومات محدودًا، يمكنك استضافة تلك المعلومات
على المنصات المقاوِمة للرقابة مثل [Google Drive](https://drive.google.com) أو
[pad.riseup.net](https://pad.riseup.net/) أو [Amazon
S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html)
(بإذن وصول من المسار إلى النمط) أو
[Netlify](https://dev.to/alexmercedcoder/delivering-json-data-with-netlify-1j96)
أو [مراكز GitHub
السرية](https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists/creating-gists).
وعليك تقييم احتياجات النشر المحدّدة واختيار منصة تتوافق
مع متطلباتك لتسهيل الاستخدام وتعزيز الأمان.
