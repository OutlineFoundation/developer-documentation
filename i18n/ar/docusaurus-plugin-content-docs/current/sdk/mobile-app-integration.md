---
title: "Add Outline SDK to Your Mobile App"
sidebar_label: "Mobile App Integration"
---

يوضّح هذا المستند كيفية تكامل Outline SDK مع التطبيقات على الأجهزة الجوّالة،
مركِّزًا على مكتبة `MobileProxy`، ما يتيح إدارة سلِسة ومبسَّطة
للخادم الوكيل على الجهاز.

‫`MobileProxy` هي مكتبة مستنِدة إلى لغة Go ومصمَّمة لتسهيل عمليات دمج
وظائف الخادم الوكيل في التطبيقات على الأجهزة الجوّالة. وتستخدم [Go
Mobile](https://go.dev/wiki/Mobile) لإنشاء المكتبات على الأجهزة الجوّالة، ما يسمح لك
بإعداد مكتبات الشبكات في تطبيقك لتنظيم الزيارات عبر الخادم الوكيل
على الجهاز.

**تطبيق بدون MobileProxy**

![تطبيق يعرض محتوى بدون MobileProxy](/images/mobileproxy-before.png)

**تطبيق يتضمّن MobileProxy**

![تطبيق يعرض محتوى ويتضمن MobileProxy](/images/mobileproxy-after.png)

## الخطوة 1: إنشاء مكتبات MobileProxy على الأجهزة الجوّالة

عليك استخدام [GoMobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile) لتجميع
رمز Go البرمجي في مكتبات على نظامَي التشغيل Android وiOS.

1. 

عليك إنشاء نسخة طبق الأصل من مستودع Outline SDK:

2. 

يجب إنشاء برامج GoMobile الثنائية باستخدام [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies):

#### إتاحة استخدام شبكة Psiphon

يمكنك إتاحة استخدام شبكة [Psiphon](https://psiphon.ca/) باتّباع
الخطوات الإضافية التالية:

    - التواصل مع فريق دعم Psiphon لاستخدام الإعدادات المطلوبة للوصول إلى
الشبكة، وقد يتطلب ذلك توقيع عقد معيّن.

    - إضافة إعدادات Psiphon المستلَمة إلى القسم `fallback` ضِمن
إعدادات `SmartDialer`.

    - 

بإمكانك إنشاء Mobile Proxy باستخدام علامة `-tags psiphon` على النحو التالي:

يجب وضع علامة `-tags psiphon`، لأنّ قاعدة رموز Psiphon
مرخَّصة بموجب ترخيص GPL والذي قد يفرض قيودًا
على رمزك البرمجي. لذا قد تحتاج إلى الحصول على ترخيص
خاص من مطوّري Psiphon.

3. 

يمكنك إنشاء المكتبات على الأجهزة الجوّالة وإضافتها إلى مشروعك على النحو التالي:

### Android

ضِمن &quot;استوديو Android&quot;، انقر على **File >‏ Import Project…** لاستيراد حزمة `out/mobileproxy.aar` التي تم إنشاؤها. ولمزيد من المساعدة، يمكنك الاطّلاع على المقالة [الإنشاء والنشر على Android](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1) في Go Mobile.

### iOS

اسحب حزمة `out/mobileproxy.xcframework` إلى مشروع Xcode. ولمزيد
من المساعدة، يمكنك الاطّلاع على المقالة [الإنشاء والنشر على iOS](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1) في
Go Mobile.

## الخطوة 2: تشغيل MobileProxy

عليك إعداد الخادم الوكيل `MobileProxy` على الجهاز وبدء تشغيله خلال وقت تشغيل تطبيقك.
ويمكنك إمّا استخدام إعدادات بروتوكول نقل ثابت أو &quot;الخادم الوكيل الذكي&quot; لاختيار
استراتيجية ديناميكية.

- 

**إعدادات بروتوكول النقل الثابت**: يمكنك استخدام دالة `RunProxy` مع عنوان
محلي وإعدادات وبروتوكول النقل.

### Android

### iOS

- 

**الخادم الوكيل الذكي**: يختار هذا الخادم استراتيجيات نظام أسماء النطاقات وبروتوكول أمان طبقة النقل (TLS)
بناءً على نطاقات اختبار معيّنة. ويجب تحديد استراتيجية
الإعدادات في ملف بتنسيق YAML
([مثال](https://github.com/Jigsaw-Code/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml)).

### Android

### iOS

## الخطوة 3: ضبط عملاء HTTP ومكتبات إنشاء الشبكات

عليك إعداد مكتبات الشبكات لاستخدام عنوان الخادم الوكيل ومنفذه على الجهاز.

### Dart/Flutter HttpClient

عليك إعداد الخادم الوكيل باستخدام
[`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html).

### OkHttp (Android)

عليك إعداد الخادم الوكيل باستخدام
[`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/).

### ‫JVM (Java وKotlin)

يجب إعداد الخادم الوكيل لاستخدام [سمات
النظام](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html):

### Android WebView

يمكنك تطبيق إعدادات الخادم الوكيل على كل طُرق عرض الويب في تطبيقك
باستخدام
مكتبة [`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController):

### iOS WebView

في أجهزة iOS 17 والإصدارات الأحدث، يمكنك إضافة إعدادات الخادم الوكيل إلى `WKWebView` باستخدام
[سمة `WKWebsiteDataStore`](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration):

## إعداد متقدّم: إنشاء مكتبة مخصّصة للأجهزة الجوّالة

في حالات الاستخدام المتقدّم، يمكنك إنشاء المكتبات على الأجهزة الجوّالة بنفسك على النحو الآتي:

1. **إنشاء مكتبة Go**: عليك أولاً تطوير حزمة Go عن طريق تغليف وظائف حزمة تطوير البرامج (SDK)
المطلوبة.

2. **إنشاء مكتبات على الأجهزة الجوّالة**: يجب استخدام `gomobile bind` لإنشاء "أرشيف
Android" ‏(AAR) و"أُطُر عمل Apple" ‏(Apple Frameworks)، على سبيل المثال:

    - [أرشيف Android من Outline](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [إطار عمل Apple من Outline](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **التكامل مع التطبيق**: أضِف المكتبة التي تم إنشاؤها إلى التطبيق
على الأجهزة الجوّالة.
