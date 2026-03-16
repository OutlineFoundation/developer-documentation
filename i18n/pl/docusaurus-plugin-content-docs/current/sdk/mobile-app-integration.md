---
title: "Add Outline SDK to Your Mobile App"
sidebar_label: "Mobile App Integration"
---

W tym dokumencie opisujemy sposób integracji pakietu Outline SDK z aplikacjami mobilnymi, skupiając się na bibliotece `MobileProxy` umożliwiającej uproszczone zarządzanie lokalnym serwerem proxy.

`MobileProxy` to biblioteka Go, która ułatwia integrację funkcji proxy z aplikacjami mobilnymi. Wykorzystuje [Go Mobile](https://go.dev/wiki/Mobile) do generowania bibliotek mobilnych, co umożliwia skonfigurowanie bibliotek sieciowych aplikacji w celu kierowania ruchu przez lokalny serwer proxy.

**Aplikacja bez MobileProxy**

![Aplikacja do treści bez MobileProxy](/images/mobileproxy-before.png)

**Aplikacja z MobileProxy**

![Aplikacja do treści z MobileProxy](/images/mobileproxy-after.png)

## Krok 1. Kompilacja bibliotek mobilnych MobileProxy {#step_1_building_mobileproxy_mobile_libraries}

Użyj polecenia [gomobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile), aby skompilować kod Go z bibliotekami na Androida oraz iOS.

1. Sklonuj repozytorium Outline SDK:

```sh
git clone https://github.com/Jigsaw-Code/outline-sdk.git
cd outline-sdk/x
```

2. Utwórz pliki binarne Go Mobile za pomocą polecenia [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies):

```sh
go build -o "$(pwd)/out/" golang.org/x/mobile/cmd/gomobile golang.org/x/mobile/cmd/gobind
```

#### Dodawanie obsługi aplikacji Psiphon {#adding_psiphon_support}

Aby dodać obsługę sieci [Psiphon](https://psiphon.ca/), wykonaj te dodatkowe czynności:

    - Skontaktuj się z zespołem Psiphon, aby otrzymać konfigurację umożliwiającą dostęp do tej sieci. Może to wymagać zawarcia umowy.

    - Dodaj otrzymaną konfigurację Psiphon do sekcji `fallback` konfiguracji `SmartDialer`.

    - Skompiluj bibliotekę MobileProxy przy użyciu flagi `-tags psiphon`:

```sh
go build -tags psiphon -o "$(pwd)/out/" golang.org/x/mobile/cmd/gomobile golang.org/x/mobile/cmd/gobind
```

Flaga `-tags psiphon` jest wymagana, ponieważ baza kodu Psiphon jest objęta licencją GPL, która może nakładać ograniczenia licencyjne na Twój własny kod. W związku z tym być może warto uzyskać specjalną licencję od firmy Psiphon.

3. Wygeneruj biblioteki mobilne i dodaj je do projektu:

### Android {#android}

```sh
PATH="$(pwd)/out:$PATH" gomobile bind -ldflags='-s -w' -target=android -androidapi=21 -o "$(pwd)/out/mobileproxy.aar" github.com/Jigsaw-Code/outline-sdk/x/mobileproxy
```

W Android Studio wybierz **Plik > Importuj projekt…**, aby zaimportować wygenerowany pakiet `out/mobileproxy.aar`. Więcej informacji znajdziesz w instrukcjach [kompilowania i wdrażania aplikacji na Androida](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1) dotyczących Go Mobile.

### iOS {#ios}

```sh
PATH="$(pwd)/out:$PATH" gomobile bind -ldflags='-s -w' -target=ios -iosversion=11.0 -o "$(pwd)/out/mobileproxy.xcframework" github.com/Jigsaw-Code/outline-sdk/x/mobileproxy
```

Przeciągnij pakiet `out/mobileproxy.xcframework` do projektu w Xcode. Więcej informacji znajdziesz w instrukcjach [kompilowania i wdrażania aplikacji na iOS](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1) dotyczących Go Mobile.

## Krok 2. Uruchamianie MobileProxy {#step_2_run_the_mobileproxy}

Zainicjuj i uruchom lokalny serwer proxy `MobileProxy` w środowisku wykonawczym aplikacji.
Możesz użyć statycznej konfiguracji transportu lub inteligentnego serwera proxy, który dynamicznie wybiera strategię.

- **Statyczna konfiguracja transportu:** użyj funkcji `RunProxy` z lokalnym adresem i konfiguracją transportu.

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

- **Inteligentny serwer proxy:** ten serwer dynamicznie wybiera strategie DNS i TLS na podstawie określonych domen testowych. Strategię dotyczącą konfiguracji należy określić w formacie YAML ([przykład](https://github.com/Jigsaw-Code/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml)).

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

## Krok 3. Konfiguracja klientów HTTP i bibliotek sieciowych {#step_3_configure_http_clients_and_networking_libraries}

Skonfiguruj biblioteki sieciowe, aby używały adresu i portu lokalnego serwera proxy.

### HttpClient Dart/Flutter {#dartflutter-httpclient}

Ustaw serwer proxy przy użyciu metody [`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html).

```dart
HttpClient client = HttpClient();
client.findProxy = (Uri uri) {
  return "PROXY " + proxy.address();
};
```

### OkHttp (Android) {#okhttp-android}

Ustaw serwer proxy przy użyciu metody [`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/).

```kotlin
val proxyConfig = Proxy(Proxy.Type.HTTP, InetSocketAddress(proxy.host(), proxy.port()))
val client = OkHttpClient.Builder().proxy(proxyConfig).build()
```

### JVM (Java, Kotlin) {#jvm-java,-kotlin}

Skonfiguruj serwer proxy za pomocą [właściwości systemowych](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html):

```kotlin
System.setProperty("http.proxyHost", proxy.host())
System.setProperty("http.proxyPort", String.valueOf(proxy.port()))
System.setProperty("https.proxyHost", proxy.host())
System.setProperty("https.proxyPort", String.valueOf(proxy.port()))
```

### Android WebView {#android-web-view}

Zastosuj konfigurację serwera proxy do wszystkich widoków WebView w bibliotece [`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController):

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

Od wersji iOS 17 możesz dodać konfigurację serwera proxy do obiektu `WKWebView` za pomocą jego [właściwości `WKWebsiteDataStore`](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration):

```swift
let configuration = WKWebViewConfiguration()
let endpoint = NWEndpoint.hostPort(host: NWEndpoint.Host(proxyHost), port: NWEndpoint.Port(proxyPort)!)
let proxyConfig = ProxyConfiguration.init(httpCONNECTProxy: endpoint)
let websiteDataStore = WKWebsiteDataStore.default()
websiteDataStore.proxyConfigurations = [proxyConfig]
let webview = WKWebView(configuration: configuration)
```

## Zaawansowane: generowanie niestandardowej biblioteki mobilnej {#advanced_generate_a_custom_mobile_library}

W zaawansowanych przypadkach użycia możesz wygenerować własne biblioteki mobilne:

1. **Tworzenie biblioteki Go:** utwórz pakiet Go zawierający wymagane funkcje SDK.

2. **Generowanie bibliotek mobilnych:** użyj polecenia `gomobile bind`, aby utworzyć pliki Android Archive (AAR) i frameworki Apple. Przykłady:

    - [Plik Android Archive biblioteki Outline](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [Framework Apple biblioteki Outline](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **Integracja aplikacji:** dodaj wygenerowaną bibliotekę do aplikacji mobilnej.
