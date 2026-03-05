---
title: "Add Outline SDK to Your Mobile App"
sidebar_label: "Mobile App Integration"
---

In diesem Dokument wird beschrieben, wie Sie das Outline SDK in Ihre mobilen Apps einbinden können. Der Fokus liegt dabei auf der `MobileProxy`-Programmbibliothek für die vereinfachte Verwaltung des lokalen Proxys.

`MobileProxy` ist eine Go-basierte Programmbibliothek, die entwickelt wurde, um die Einbindung von Proxy-Funktionen in mobile Apps zu vereinfachen. Sie nutzt [Go Mobile](https://go.dev/wiki/Mobile), um Bibliotheken für mobile Apps zu erstellen. Sie können dadurch die Netzwerk-Bibliotheken Ihrer App so konfigurieren, dass der Datenverkehr über einen lokalen Proxy geleitet wird.

**App ohne MobileProxy**

![Content-App ohne MobileProxy](/images/mobileproxy-before.png)

**App mit MobileProxy**

![Content-App mit MobileProxy](/images/mobileproxy-after.png)

## Schritt 1: MobileProxy-Bibliotheken erstellen

Sie können [gomobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile) verwenden, um den Go-Code in Programmbibliotheken für Android und iOS zu kompilieren.

1. Klonen Sie das Outline SDK Repository:

2. Erstellen Sie die Go Mobile-Binärprogramme mit [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies):

#### Psiphon-Support hinzufügen

Sie können Support zur Nutzung des [Psiphon](https://psiphon.ca/)-Netzwerks hinzufügen, wenn Sie diese zusätzlichen Schritte ausführen:

    - Wenden Sie sich an das Psiphon-Team, um eine Konfiguration zu erhalten, die Ihnen Zugriff auf deren Netzwerk ermöglicht. Dazu kann ein Vertrag erforderlich sein.

    - Fügen Sie die erhaltene Psiphon-Konfiguration in den `fallback`-Abschnitt Ihrer `SmartDialer`-Konfiguration ein.

    - Erstellen Sie den MobileProxy und verwenden Sie dazu das `-tags psiphon`-Flag:

Das `-tags psiphon`-Flag ist erforderlich, weil die Psiphon-Codebasis unter der GPL lizenziert ist, was zu Einschränkungen der Lizenz für Ihren eigenen Code führen kann. Sie sollten erwägen, eine spezielle Lizenz zu kaufen.

3. Erstellen Sie Bibliotheken für mobile Apps und fügen Sie diese zu Ihrem Projekt hinzu:

### Android

Wählen Sie in Android Studio **Datei > Projekt importieren…**, um das erstellte `out/mobileproxy.aar`-Bundle zu importieren. Weitere Hilfe finden Sie im Bereich zu [Entwicklung und Bereitstellung für Android](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1) von Go Mobile.

### iOS

Ziehen Sie das `out/mobileproxy.xcframework`-Bundle in das Xcode-Projekt. Weitere Hilfe finden Sie im Bereich zu [Entwicklung und Bereitstellung für iOS](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1).

## Schritt 2: MobileProxy ausführen

Initialisieren und starten Sie den lokalen Proxy `MobileProxy` während der Laufzeit Ihrer App.
Sie können entweder eine statische Transportkonfiguration oder den Smart Proxy für eine dynamische Strategieauswahl verwenden.

- **Statische Transportkonfiguration**: Verwenden Sie die `RunProxy`-Funktion mit einer lokalen Adresse und Transportkonfiguration.

### Android

### iOS

- **Smart Proxy**: Der Smart Proxy wählt dynamisch DNS- und TLS-Strategien anhand der angegebenen Testdomains aus. Sie müssen die Konfigurationsstrategie im YAMLFormat festlegen ([Beispiel](https://github.com/Jigsaw-Code/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml)).

### Android

### iOS

## Schritt 3: HTTP-Clients und Netzwerk-Bibliotheken konfigurieren

Konfigurieren Sie Ihre Netzwerk-Bibliotheken so, dass sie die lokale Proxy-Adresse und den Proxy-Port verwenden.

### Dart/Flutter HttpClient

Konfigurieren Sie den Proxy mit
[`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html).

### OkHttp (Android)

Konfigurieren Sie den Proxy mit
[`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/).

### JVM (Java, Kotlin)

Konfigurieren Sie den verwendeten Proxy mit den [Systemeigenschaften](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html):

### Android Web-Ansicht

Wenden Sie eine Proxy-Konfiguration auf alle Webansichten in Ihrer App mit der [`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController)-Bibliothek an:

### iOS Web-Ansicht

Ab iOS 17 können Sie eine Proxy-Konfiguration zu einem `WKWebView` hinzufügen, indem sie die [`WKWebsiteDataStore`-Eigenschaft](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration) nutzen:

## Erweitert: Benutzerdefinierte Bibliothek für mobile Apps erstellen

Für erweiterte Anwendungsfälle können Sie eigene Bibliotheken für mobile Apps erstellen:

1. **Go-Programmbibliothek erstellen**: Entwickeln Sie ein Go-Paket, dass die erforderlichen SDK-Funktionen zusammenfasst.

2. **Bibliotheken für mobile Apps erstellen**: Verwenden Sie `gomobile bind`, um Android-Archive (AAR) und Apple Frameworks zu erstellen. Beispiele:

    - [Outline Android-Archiv](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [Outline Apple-Framework](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **In Ihre App einbinden**: Fügen Sie die erstellte Bibliothek zu Ihrer App hinzu.
