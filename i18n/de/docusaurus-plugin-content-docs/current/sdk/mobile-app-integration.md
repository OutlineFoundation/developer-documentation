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

## Schritt 1: MobileProxy-Bibliotheken erstellen {#step_1_building_mobileproxy_mobile_libraries}

Sie können [gomobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile) verwenden, um den Go-Code in Programmbibliotheken für Android und iOS zu kompilieren.

1. Klonen Sie das Outline SDK Repository:

```sh
git clone https://github.com/Jigsaw-Code/outline-sdk.git
cd outline-sdk/x
```

2. Erstellen Sie die Go Mobile-Binärprogramme mit [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies):

```sh
go build -o "$(pwd)/out/" golang.org/x/mobile/cmd/gomobile golang.org/x/mobile/cmd/gobind
```

#### Psiphon-Support hinzufügen {#adding_psiphon_support}

Sie können Support zur Nutzung des [Psiphon](https://psiphon.ca/)-Netzwerks hinzufügen, wenn Sie diese zusätzlichen Schritte ausführen:

    - Wenden Sie sich an das Psiphon-Team, um eine Konfiguration zu erhalten, die Ihnen Zugriff auf deren Netzwerk ermöglicht. Dazu kann ein Vertrag erforderlich sein.

    - Fügen Sie die erhaltene Psiphon-Konfiguration in den `fallback`-Abschnitt Ihrer `SmartDialer`-Konfiguration ein.

    - Erstellen Sie den MobileProxy und verwenden Sie dazu das `-tags psiphon`-Flag:

```sh
go build -tags psiphon -o "$(pwd)/out/" golang.org/x/mobile/cmd/gomobile golang.org/x/mobile/cmd/gobind
```

Das `-tags psiphon`-Flag ist erforderlich, weil die Psiphon-Codebasis unter der GPL lizenziert ist, was zu Einschränkungen der Lizenz für Ihren eigenen Code führen kann. Sie sollten erwägen, eine spezielle Lizenz zu kaufen.

3. Erstellen Sie Bibliotheken für mobile Apps und fügen Sie diese zu Ihrem Projekt hinzu:

### Android {#android}

```sh
PATH="$(pwd)/out:$PATH" gomobile bind -ldflags='-s -w' -target=android -androidapi=21 -o "$(pwd)/out/mobileproxy.aar" github.com/Jigsaw-Code/outline-sdk/x/mobileproxy
```

Wählen Sie in Android Studio **Datei > Projekt importieren…**, um das erstellte `out/mobileproxy.aar`-Bundle zu importieren. Weitere Hilfe finden Sie im Bereich zu [Entwicklung und Bereitstellung für Android](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1) von Go Mobile.

### iOS {#ios}

```sh
PATH="$(pwd)/out:$PATH" gomobile bind -ldflags='-s -w' -target=ios -iosversion=11.0 -o "$(pwd)/out/mobileproxy.xcframework" github.com/Jigsaw-Code/outline-sdk/x/mobileproxy
```

Ziehen Sie das `out/mobileproxy.xcframework`-Bundle in das Xcode-Projekt. Weitere Hilfe finden Sie im Bereich zu [Entwicklung und Bereitstellung für iOS](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1).

## Schritt 2: MobileProxy ausführen {#step_2_run_the_mobileproxy}

Initialisieren und starten Sie den lokalen Proxy `MobileProxy` während der Laufzeit Ihrer App.
Sie können entweder eine statische Transportkonfiguration oder den Smart Proxy für eine dynamische Strategieauswahl verwenden.

- **Statische Transportkonfiguration**: Verwenden Sie die `RunProxy`-Funktion mit einer lokalen Adresse und Transportkonfiguration.

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

- **Smart Proxy**: Der Smart Proxy wählt dynamisch DNS- und TLS-Strategien anhand der angegebenen Testdomains aus. Sie müssen die Konfigurationsstrategie im YAMLFormat festlegen ([Beispiel](https://github.com/Jigsaw-Code/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml)).

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

## Schritt 3: HTTP-Clients und Netzwerk-Bibliotheken konfigurieren {#step_3_configure_http_clients_and_networking_libraries}

Konfigurieren Sie Ihre Netzwerk-Bibliotheken so, dass sie die lokale Proxy-Adresse und den Proxy-Port verwenden.

### Dart/Flutter HttpClient {#dartflutter-httpclient}

Konfigurieren Sie den Proxy mit
[`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html).

```dart
HttpClient client = HttpClient();
client.findProxy = (Uri uri) {
  return "PROXY " + proxy.address();
};
```

### OkHttp (Android) {#okhttp-android}

Konfigurieren Sie den Proxy mit
[`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/).

```kotlin
val proxyConfig = Proxy(Proxy.Type.HTTP, InetSocketAddress(proxy.host(), proxy.port()))
val client = OkHttpClient.Builder().proxy(proxyConfig).build()
```

### JVM (Java, Kotlin) {#jvm-java,-kotlin}

Konfigurieren Sie den verwendeten Proxy mit den [Systemeigenschaften](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html):

```kotlin
System.setProperty("http.proxyHost", proxy.host())
System.setProperty("http.proxyPort", String.valueOf(proxy.port()))
System.setProperty("https.proxyHost", proxy.host())
System.setProperty("https.proxyPort", String.valueOf(proxy.port()))
```

### Android Web-Ansicht {#android-web-view}

Wenden Sie eine Proxy-Konfiguration auf alle Webansichten in Ihrer App mit der [`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController)-Bibliothek an:

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

### iOS Web-Ansicht {#ios-web-view}

Ab iOS 17 können Sie eine Proxy-Konfiguration zu einem `WKWebView` hinzufügen, indem sie die [`WKWebsiteDataStore`-Eigenschaft](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration) nutzen:

```swift
let configuration = WKWebViewConfiguration()
let endpoint = NWEndpoint.hostPort(host: NWEndpoint.Host(proxyHost), port: NWEndpoint.Port(proxyPort)!)
let proxyConfig = ProxyConfiguration.init(httpCONNECTProxy: endpoint)
let websiteDataStore = WKWebsiteDataStore.default()
websiteDataStore.proxyConfigurations = [proxyConfig]
let webview = WKWebView(configuration: configuration)
```

## Erweitert: Benutzerdefinierte Bibliothek für mobile Apps erstellen {#advanced_generate_a_custom_mobile_library}

Für erweiterte Anwendungsfälle können Sie eigene Bibliotheken für mobile Apps erstellen:

1. **Go-Programmbibliothek erstellen**: Entwickeln Sie ein Go-Paket, dass die erforderlichen SDK-Funktionen zusammenfasst.

2. **Bibliotheken für mobile Apps erstellen**: Verwenden Sie `gomobile bind`, um Android-Archive (AAR) und Apple Frameworks zu erstellen. Beispiele:

    - [Outline Android-Archiv](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [Outline Apple-Framework](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **In Ihre App einbinden**: Fügen Sie die erstellte Bibliothek zu Ihrer App hinzu.
