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

## الخطوة 1: إنشاء مكتبات MobileProxy على الأجهزة الجوّالة {#step_1_building_mobileproxy_mobile_libraries}

عليك استخدام [GoMobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile) لتجميع
رمز Go البرمجي في مكتبات على نظامَي التشغيل Android وiOS.

1. عليك إنشاء نسخة طبق الأصل من مستودع Outline SDK:

```sh
git clone https://github.com/Jigsaw-Code/outline-sdk.git
cd outline-sdk/x
```

2. يجب إنشاء برامج GoMobile الثنائية باستخدام [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies):

```sh
go build -o "$(pwd)/out/" golang.org/x/mobile/cmd/gomobile golang.org/x/mobile/cmd/gobind
```

#### إتاحة استخدام شبكة Psiphon {#adding_psiphon_support}

يمكنك إتاحة استخدام شبكة [Psiphon](https://psiphon.ca/) باتّباع
الخطوات الإضافية التالية:

    - التواصل مع فريق دعم Psiphon لاستخدام الإعدادات المطلوبة للوصول إلى
الشبكة، وقد يتطلب ذلك توقيع عقد معيّن.

    - إضافة إعدادات Psiphon المستلَمة إلى القسم `fallback` ضِمن
إعدادات `SmartDialer`.

    - بإمكانك إنشاء Mobile Proxy باستخدام علامة `-tags psiphon` على النحو التالي:

```sh
go build -tags psiphon -o "$(pwd)/out/" golang.org/x/mobile/cmd/gomobile golang.org/x/mobile/cmd/gobind
```

يجب وضع علامة `-tags psiphon`، لأنّ قاعدة رموز Psiphon
مرخَّصة بموجب ترخيص GPL والذي قد يفرض قيودًا
على رمزك البرمجي. لذا قد تحتاج إلى الحصول على ترخيص
خاص من مطوّري Psiphon.

3. يمكنك إنشاء المكتبات على الأجهزة الجوّالة وإضافتها إلى مشروعك على النحو التالي:

### Android {#android}

```sh
PATH="$(pwd)/out:$PATH" gomobile bind -ldflags='-s -w' -target=android -androidapi=21 -o "$(pwd)/out/mobileproxy.aar" github.com/Jigsaw-Code/outline-sdk/x/mobileproxy
```

ضِمن &quot;استوديو Android&quot;، انقر على **File >‏ Import Project…** لاستيراد حزمة `out/mobileproxy.aar` التي تم إنشاؤها. ولمزيد من المساعدة، يمكنك الاطّلاع على المقالة [الإنشاء والنشر على Android](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1) في Go Mobile.

### iOS {#ios}

```sh
PATH="$(pwd)/out:$PATH" gomobile bind -ldflags='-s -w' -target=ios -iosversion=11.0 -o "$(pwd)/out/mobileproxy.xcframework" github.com/Jigsaw-Code/outline-sdk/x/mobileproxy
```

اسحب حزمة `out/mobileproxy.xcframework` إلى مشروع Xcode. ولمزيد
من المساعدة، يمكنك الاطّلاع على المقالة [الإنشاء والنشر على iOS](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1) في
Go Mobile.

## الخطوة 2: تشغيل MobileProxy {#step_2_run_the_mobileproxy}

عليك إعداد الخادم الوكيل `MobileProxy` على الجهاز وبدء تشغيله خلال وقت تشغيل تطبيقك.
ويمكنك إمّا استخدام إعدادات بروتوكول نقل ثابت أو &quot;الخادم الوكيل الذكي&quot; لاختيار
استراتيجية ديناميكية.

- **إعدادات بروتوكول النقل الثابت**: يمكنك استخدام دالة `RunProxy` مع عنوان
محلي وإعدادات وبروتوكول النقل.

### Android {#android_1}

```kotlin
import mobileproxy.*

val dialer = StreamDialer("split:3")

// Use port zero to let the system pick an open port for you.
val proxy = Mobileproxy.runProxy("localhost:0", dialer)
// Configure your networking library using proxy.host() and proxy.port() or proxy.address().
// ...
// Stop running the proxy.
proxy.stop()
```

### iOS {#ios_1}

```swift
import Mobileproxy

let dialer = MobileproxyStreamDialer("split:3")

// Use port zero to let the system pick an open port for you.
let proxy = MobileproxyRunProxy("localhost:0", dialer)
// Configure your networking library using proxy.host() and proxy.port() or proxy.address().
// ...
// Stop running the proxy.
proxy.stop()
```

- **الخادم الوكيل الذكي**: يختار هذا الخادم استراتيجيات نظام أسماء النطاقات وبروتوكول أمان طبقة النقل (TLS)
بناءً على نطاقات اختبار معيّنة. ويجب تحديد استراتيجية
الإعدادات في ملف بتنسيق YAML
([مثال](https://github.com/Jigsaw-Code/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml)).

### Android {#android_2}

```kotlin
val testDomains = Mobileproxy.newListFromLines("www.youtube.com\ni.ytimg.com")
val strategiesConfig = "..."  // Config YAML.
val dialer = Mobileproxy.newSmartStreamDialer(testDomains, strategiesConfig, Mobileproxy.newStderrLogWriter())

// Use port zero to let the system pick an open port for you.
val proxy = Mobileproxy.runProxy("localhost:0", dialer)
// Configure your networking library using proxy.host() and proxy.port() or proxy.address().
// ...
// Stop running the proxy.
proxy.stop()
```

### iOS {#ios_2}

```swift
import Mobileproxy

var dialerError: NSError?
let testDomains = MobileproxyNewListFromLines("www.youtube.com\ni.ytimg.com")
let strategiesConfig = "..."  // Config YAML.
let dialer = MobileproxyNewSmartStreamDialer(
    testDomains,
    strategiesConfig,
    MobileproxyNewStderrLogWriter(),
    &dialerError
)

var proxyError: NSError?
// Use port zero to let the system pick an open port for you.
MobileproxyRunProxy("localhost:0", dialer, &proxyError)
// Configure your networking library using proxy.host() and proxy.port() or proxy.address().
// ...
// Stop running the proxy.
proxy.stop()
```

## الخطوة 3: ضبط عملاء HTTP ومكتبات إنشاء الشبكات {#step_3_configure_http_clients_and_networking_libraries}

عليك إعداد مكتبات الشبكات لاستخدام عنوان الخادم الوكيل ومنفذه على الجهاز.

### Dart/Flutter HttpClient {#dartflutter-httpclient}

عليك إعداد الخادم الوكيل باستخدام
[`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html).

```dart
HttpClient client = HttpClient();
client.findProxy = (Uri uri) {
  return "PROXY " + proxy.address();
};
```

### OkHttp (Android) {#okhttp-android}

عليك إعداد الخادم الوكيل باستخدام
[`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/).

```kotlin
val proxyConfig = Proxy(Proxy.Type.HTTP, InetSocketAddress(proxy.host(), proxy.port()))
val client = OkHttpClient.Builder().proxy(proxyConfig).build()
```

### ‫JVM (Java وKotlin) {#jvm-java,-kotlin}

يجب إعداد الخادم الوكيل لاستخدام [سمات
النظام](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html):

```kotlin
System.setProperty("http.proxyHost", proxy.host())
System.setProperty("http.proxyPort", String.valueOf(proxy.port()))
System.setProperty("https.proxyHost", proxy.host())
System.setProperty("https.proxyPort", String.valueOf(proxy.port()))
```

### Android WebView {#android-web-view}

يمكنك تطبيق إعدادات الخادم الوكيل على كل طُرق عرض الويب في تطبيقك
باستخدام
مكتبة [`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController):

```java
ProxyController.getInstance()
    .setProxyOverride(
        ProxyConfig.Builder()
            .addProxyRule(this.proxy!!.address())
            .build(),
        {}, // execution context for the following callback - do anything needed here once the proxy is applied, like refreshing web views
        {} // callback to be called once the ProxyConfig is applied
    )
```

### iOS WebView {#ios-web-view}

في أجهزة iOS 17 والإصدارات الأحدث، يمكنك إضافة إعدادات الخادم الوكيل إلى `WKWebView` باستخدام
[سمة `WKWebsiteDataStore`](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration):

```swift
let configuration = WKWebViewConfiguration()
let endpoint = NWEndpoint.hostPort(host: NWEndpoint.Host(proxyHost), port: NWEndpoint.Port(proxyPort)!)
let proxyConfig = ProxyConfiguration.init(httpCONNECTProxy: endpoint)
let websiteDataStore = WKWebsiteDataStore.default()
websiteDataStore.proxyConfigurations = [proxyConfig]
let webview = WKWebView(configuration: configuration)
```

## إعداد متقدّم: إنشاء مكتبة مخصّصة للأجهزة الجوّالة {#advanced_generate_a_custom_mobile_library}

في حالات الاستخدام المتقدّم، يمكنك إنشاء المكتبات على الأجهزة الجوّالة بنفسك على النحو الآتي:

1. **إنشاء مكتبة Go**: عليك أولاً تطوير حزمة Go عن طريق تغليف وظائف حزمة تطوير البرامج (SDK)
المطلوبة.

2. **إنشاء مكتبات على الأجهزة الجوّالة**: يجب استخدام `gomobile bind` لإنشاء "أرشيف
Android" ‏(AAR) و"أُطُر عمل Apple" ‏(Apple Frameworks)، على سبيل المثال:

    - [أرشيف Android من Outline](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [إطار عمل Apple من Outline](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **التكامل مع التطبيق**: أضِف المكتبة التي تم إنشاؤها إلى التطبيق
على الأجهزة الجوّالة.
