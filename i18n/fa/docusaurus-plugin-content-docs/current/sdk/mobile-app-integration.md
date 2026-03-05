---
title: "Add Outline SDK to Your Mobile App"
sidebar_label: "Mobile App Integration"
---

این سند طرح کلی نحوه ادغام کردن Outline SDK را در برنامه‌های تلفن همراهتان ارائه می‌کند
و بر کتابخانه `MobileProxy` تمرکز می‌کند تا مدیریت پراکسی محلی را
ساده کند.

‫`MobileProxy` کتابخانه‌ای مبتنی بر Go است که برای ساده کردن یکپارچه‌سازی
عملکرد پراکسی در برنامه‌های تلفن همراه طراحی شده است. از [Go
Mobile](https://go.dev/wiki/Mobile) استفاده می‌کند تا کتابخانه‌های تلفن همراه را تولید کند و شما را قادر کند
کتابخانه‌های شبکه‌سازی برنامه‌تان را پیکربندی کنید تا ترافیک را ازطریق
پراکسی محلی هدایت کنید.

**برنامه بدون MobileProxy**

![MobileProxy برنامه محتوای بدون](/images/mobileproxy-before.png)

**برنامه با MobileProxy**

![MobileProxy برنامه محتوا با](/images/mobileproxy-after.png)

## مرحله ۱: ساختن کتابخانه‌های تلفن همراه MobileProxy

از [gomobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile) استفاده کنید تا کد Go را در کتابخانه‌های Android و iOS ترجمه کنید.

1. همسانه‌سازی کردن مخزن Outline SDK:

2. ساختن دودویی‌های Go Mobile با [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies):

#### افزودن پشتیبانی Psiphon

می‌توانید پشتیبان اضافه کنید تا از شبکه [Psiphon](https://psiphon.ca/) استفاده کنید،
مراحل اضافه زیر را دنبال کنید:

    - با تیم Psiphon تماس بگیرید تا پیکربندی‌ای را دریافت کنید که به شما اجازه دسترسی به
شبکه می‌دهد. برای دریافت کردن این اجازه، ممکن است به قرارداد نیاز داشته باشید.

    - پیکربندی Psiphon را که دریافت کرده‌اید به بخش `fallback` در
پیکربندی `SmartDialer` اضافه کنید.

    - ساختن «پراکسی تلفن همراه» بااستفاده از پرچم `-tags psiphon`:

پرچم `-tags psiphon` لازم است زیرا پایگاه کد Psiphon
تحت پروانه GPL است که می‌تواند محدودیت‌های پروانه‌دار را بر
کد شما اعمال کند. می‌توانید برای دریافت کردن پروانه ویژه آن اقدام کنید.

3. تولید کردن کتابخانه‌های تلفن همراه و افزودن آن‌ها به پروژه:

### Android

در «استودیو Android»، **فایل > وارد کردن پروژه…** را انتخاب کنید تا بسته `out/mobileproxy.aar` تولیدشده را وارد کنید. برای راهنمایی بیشتر، [ساختن و پیاده‌سازی در Android](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1) مربوط به Go Mobile را ببینید.

### iOS

بسته `out/mobileproxy.xcframework` را به پروژه Xcode بکشید. برای
راهنمایی بیشتر، [Building and deploying to
iOS (ساختن و پیاده‌سازی در
iOS)](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1) مربوط به Go Mobile را ببینید.

## مرحله ۲: اجرا کردن MobileProxy

درون زمان اجرای برنامه‌تان، به پراکسی محلی `MobileProxy` مقدار اولیه دهید و آن را شروع کنید.
می‌توانید از پیکربندی حمل‌ونقل ثابت یا از Smart Proxy (پراکسی هوشمند) برای
انتخاب راهبرد پویا استفاده کنید.

- **پیکربندی حمل‌ونقل ثابت**: از تابع `RunProxy` با
نشانی محلی و پیکربندی حمل‌ونقل استفاده کنید.

### Android

### iOS

- **پراکسی هوشمند**: «پراکسی هوشمند» رهنمودهای ساناد و «امنیت لایه انتقال» را
براساس دامنه‌های آزمایشی معین‌شده‌ای به‌طور پویا انتخاب می‌کند. باید رهنمود پیکربندی را
در قالب YAML معین کنید
([نمونه](https://github.com/Jigsaw-Code/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml)).

### Android

### iOS

## مرحله ۳: پیکربندی کردن کارخواه HTTP و کتابخانه‌های شبکه‌سازی

کتابخانه‌های شبکه‌سازی‌تان را پیکربندی کنید تا از درگاه و نشانی پراکسی محلی‌تان استفاده کنید.

### Dart/Flutter HttpClient

تنظیم کردن پراکسی با
[`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html).

### OkHttp (Android)

تنظیم کردن پراکسی با
[`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/).

### JVM (Java, Kotlin)

پراکسی را پیکربندی کنید تا با [خصوصیات
سیستم](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html) استفاده کنید:

### نمای وب Android

پیکربندی پراکسی را روی همه نماهای وب در برنامه‌تان
با
کتابخانه [`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController)
اعمال کنید:

### نمای وب iOS

از iOS نسخه ۱۷، می‌توانید پیکربندی پراکسی را بااستفاده از [property (خصوصیت) `WKWebsiteDataStore`](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration) آن، به `WKWebView` اضافه کنید:

## پیشرفته: تولید کردن کتابخانه سفارشی تلفن همراه

در موارد استفاده پیشرفته، می‌توانید کتابخانه‌های تلفن همراه خودتان را تولید کنید:

1. **ساختن کتابخانه Go**: بسته Go را توسعه دهید تا عملکردهای «کیت توسعه نرم‌افزار» (SDK) لازم را بسته‌بندی کند.

2. **تولید کردن کتابخانه‌های تلفن همراه**: از `gomobile bind` استفاده کنید تا Android
Archives (AAR) و چارچوب‌های Apple تولید کنید. مثال‌ها:

    - [بایگانی Outline Android](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [چارچوب Outline Apple](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **ادغام کردن در برنامه‌تان**: کتابخانه تولیدشده را به برنامه
تلفن همراهتان اضافه کنید.
