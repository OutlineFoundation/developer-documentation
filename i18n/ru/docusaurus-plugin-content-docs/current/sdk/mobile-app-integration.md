---
title: "Add Outline SDK to Your Mobile App"
sidebar_label: "Mobile App Integration"
---

В этом руководстве описывается, как интегрировать Outline SDK в мобильные приложения с использованием библиотеки `MobileProxy`, которая упрощает работу с локальным прокси-сервером.

`MobileProxy` – это библиотека на основе языка Go. Она упрощает интеграцию функций прокси-сервера в мобильные приложения. Библиотека использует инструмент [Go Mobile](https://go.dev/wiki/Mobile) для генерирования мобильных библиотек. Это позволяет настраивать сетевые библиотеки приложения так, чтобы трафик проходил через локальный прокси-сервер.

**Приложение без MobileProxy**

![Приложение для работы с контентом без MobileProxy](/images/mobileproxy-before.png)

**Приложение с MobileProxy**

![Приложение для работы с контентом с MobileProxy3](/images/mobileproxy-after.png)

## Шаг 1. Создайте мобильные библиотеки MobileProxy

Используйте [gomobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile), чтобы скомпилировать код Go в библиотеки для Android и iOS.

1. Клонируйте хранилище Outline SDK:

2. Соберите исполняемые файлы Go Mobile с помощью команды [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies):

#### Как добавить поддержку Psiphon

Вы можете добавить поддержку сети [Psiphon](https://psiphon.ca/), выполнив следующие дополнительные шаги:

    - Свяжитесь с командой Psiphon, чтобы получить конфигурацию для доступа к их сети. Возможно, для этого потребуется заключить договор.

    - Добавьте полученную конфигурацию Psiphon в раздел `fallback` конфигурации `SmartDialer`.

    - Соберите Mobile Proxy с пометкой `-tags psiphon`:

Пометка `-tags psiphon` обязательна, поскольку код Psiphon доступен по лицензии GPL, которая может накладывать лицензионные ограничения на ваш код. Рассмотрите возможность получения специальной лицензии у команды Psiphon.

3. Как создать мобильные библиотеки и добавить их в проект

### Android

В Android Studio выберите **File > Import Project… (Файл > Импортировать проект…)**, чтобы импортировать сгенерированный пакет `out/mobileproxy.aar`. Дополнительная информация приведена в разделе Go Mobile на странице [Сборка и развертывание для Android](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1).

### iOS

Перетащите пакет `out/mobileproxy.xcframework` в проект Xcode. Дополнительная информация приведена в разделе Go Mobile на странице [Сборка и развертывание для iOS](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1).

## Шаг 2. Запустите MobileProxy

Инициализируйте и запустите локальный прокси-сервер `MobileProxy` в среде выполнения вашего приложения.
Вы можете использовать статическую конфигурацию протокола или SmartProxy для динамического выбора стратегии.

- **Статическая конфигурация протокола:** используйте функцию `RunProxy`, указав локальный адрес и параметры конфигурации протокола.

### Android

### iOS

- **SmartProxy:** эта технология динамически выбирает стратегии DNS и TLS на основе заданных тестовых доменов. Стратегию конфигурации необходимо указать в формате YAML ([пример](https://github.com/Jigsaw-Code/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml)).

### Android

### iOS

## Шаг 3. Настройте HTTP-клиенты и сетевые библиотеки

Настройте сетевые библиотеки на использование локального адреса и порта прокси-сервера.

### Dart/Flutter HttpClient

Установите прокси-сервер с помощью [`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html).

### OkHttp (Android)

Установите прокси-сервер с помощью [`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/).

### JVM (Java, Kotlin)

Настройте прокси-сервер с использованием [системных свойств](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html):

### Android WebView

Примените конфигурацию прокси-сервера ко всем WebView в приложении с помощью библиотеки [`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController):

### iOS WebView

Начиная с iOS 17 и более поздних версий вы можете добавить прокси-конфигурацию для `WKWebView`, используя [свойство `WKWebsiteDataStore`](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration):

## Как создать собственную мобильную библиотеку (расширенная настройка)

Если требуется расширенная настройка, вы можете сгенерировать собственные мобильные библиотеки.

1. **Создайте библиотеку на основе языка Go:** разработайте Go-пакет, включающий нужные функции SDK.

2. **Сгенерируйте мобильные библиотеки:** используйте `gomobile bind` для создания Android ARchive (AAR) и Apple Framework. Примеры:

    - [Outline Android Archive](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [Outline Apple Framework](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **Интегрируйте сгенерированную библиотеку в мобильное приложение.**
