---
title: "تحديد خصائص التشويش الشبكي وتجاوزه عن بُعد باستخدام Outline SDK"
sidebar_label: "تحديد خصائص التشويش الشبكي وتجاوزه عن بُعد باستخدام Outline SDK"
---

يوضّح هذا الدليل كيفية استخدام أدوات سطر الأوامر في حزمة تطوير البرامج (SDK) الخاصة بتطبيق Outline لفهم التشويش على الشبكة وتجنُّبه من منظور بعيد. ستتعرّف على كيفية استخدام أدوات حزمة تطوير البرامج (SDK) لقياس التشويش الشبكي واختبار استراتيجيات التحايل وتحليل النتائج. سيركّز هذا الدليل على أدوات `resolve` و`fetch` و`http2transport`.

## بدء استخدام أدوات Outline SDK

يمكنك بدء استخدام أدوات Outline SDK مباشرةً من سطر الأوامر.

### حلّ مشكلة نظام أسماء النطاقات

تتيح لك الأداة `resolve` إجراء عمليات بحث في نظام أسماء النطاقات باستخدام برنامج تعيين محدّد.

لحلّ سجلّ A الخاص بنطاق:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type A 1.2.3.4.nip.io
```

لحلّ سجلّ CNAME، اتّبِع الخطوات التالية:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type CNAME www.google.com
```

### جلب صفحة ويب

يمكن استخدام أداة `fetch` لاسترداد محتوى صفحة ويب.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest https://example.com
```

يمكنه أيضًا فرض استخدام QUIC في الاتصال.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -proto=h3 https://www.youtube.com
```

### استخدام خادم وكيل محلي

تنشئ أداة `http2transport` خادم وكيل محليًا لتوجيه الزيارات من خلاله.
لبدء وكيل محلي باستخدام نقل Shadowsocks، اتّبِع الخطوات التالية:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/http2transport@latest -localAddr 127.0.0.1:8080 -transport "ss://{your_shadowsocks_credentials}"
```

يمكنك بعد ذلك استخدام هذا الخادم الوكيل مع أدوات أخرى، مثل curl:

```sh
curl -p -x http://127.0.0.1:8080 https://ipinfo.io
```

## تحديد استراتيجيات التحايل

تتيح حزمة تطوير البرامج (SDK) الخاصة بـ Outline تحديد استراتيجيات مختلفة للتحايل
يمكن دمجها لتجاوز أشكال مختلفة من التشويش على الشبكة. يمكنك الاطّلاع على مواصفات هذه الاستراتيجيات في [مستندات Go](https://pkg.go.dev/github.com/OutlineFoundation/outline-sdk/x@v0.0.3/configurl).

### استراتيجيات قابلة للتعديل

يمكن الجمع بين هذه الاستراتيجيات لإنشاء تقنيات تحايل أكثر فعالية.

* **معالجة نظام أسماء النطاقات عبر بروتوكول HTTPS باستخدام تجزئة بروتوكول أمان طبقة النقل (TLS)**: `doh:name=cloudflare-dns.com&address=cloudflare.net:443 | tlsfrag:1`

* **SOCKS5-over-TLS مع إخفاء هوية النطاق**: `tls:sni=decoy.example.com&certname=[HOST] | socks5:[HOST]:[PORT]`

* **توجيه متعدد المسارات باستخدام Shadowsocks**: `ss://[USERINFO1]@[HOST1]:[PORT1] | ss://[USERINFO2]@[HOST2]:[PORT2] | ss://[USERINFO3]@[HOST3]:[PORT3]`

## الوصول عن بُعد والقياس

لقياس تداخل الشبكة كما يتم رصده في مناطق مختلفة، يمكنك استخدام خوادم وكيل بعيدة. يمكنك العثور على خوادم وكيلة بعيدة أو إنشاؤها للاتصال بها.

### خيارات الوصول عن بُعد

باستخدام أداة `fetch`، يمكنك اختبار الاتصالات عن بُعد بطرق مختلفة.

#### خادم Outline

الاتصال عن بُعد بخادم Outline عادي باستخدام نقل Shadowsocks

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "ss://{remote_shadowsocks_credentials}" https://ipinfo.io | jq
```

#### SOCKS5 عبر SSH

إنشاء وكيل SOCKS5 باستخدام نفق SSH

```sh
ssh -D 127.0.0.1:1080 -C -N $USER@$HOST:$PORT
```

الاتصال بهذا النفق باستخدام fetch

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "socks5://localhost:1080" https://ipinfo.io | jq
```

## دراسة حالة: تجاوز الحظر المفروض على YouTube في إيران

في ما يلي مثال عملي على رصد التداخل في الشبكة وتجاوزه.

### اكتشاف الكتلة

عند محاولة جلب صفحة YouTube الرئيسية من خلال خادم وكيل إيراني، تنتهي مهلة الطلب، ما يشير إلى الحظر.

```sh
export TRANSPORT="ss://{remote_shadowsocks_credentials}"
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)" https://www.youtube.com
```

يتعذّر تنفيذ هذا الأمر بسبب انتهاء المهلة.

### التجاوز باستخدام تجزئة بروتوكول أمان طبقة النقل (TLS)

من خلال إضافة تجزئة TLS إلى النقل، يمكننا تجاوز هذا الحظر.

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)|tlsfrag:1" https://www.youtube.com | grep -oe '<title>.*</title>'
```

يستردّ هذا الأمر بنجاح عنوان صفحة YouTube الرئيسية، وهو
`<title>YouTube</title>`.

### التجاوز باستخدام تجزئة TLS وDNS-over-HTTPS

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|tlsfrag:1|doh:name=cloudflare-dns.com&address=www.cloudflare.net" https://www.youtube.com | grep -oe '<title>.*</title>'
```

يؤدي ذلك أيضًا إلى عرض القيمة `<title>YouTube</title>` بنجاح.

### تجاوز القيود باستخدام خادم Outline

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|ss://<your_shadowsocks_credentials>" https://www.youtube.com | grep -oe '<title>.*</title>'
```

ويعرض هذا الإجراء أيضًا القيمة `<title>YouTube</title>`.

## المزيد من التحليلات والمراجع

للمناقشات والأسئلة، يُرجى الانتقال إلى [مجموعة مناقشة حزمة تطوير البرامج (SDK) الخاصة بخدمة Outline](https://github.com/OutlineFoundation/outline-sdk/discussions).
