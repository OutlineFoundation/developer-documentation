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

## Krok 1. Kompilacja bibliotek mobilnych MobileProxy

Użyj polecenia [gomobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile), aby skompilować kod Go z bibliotekami na Androida oraz iOS.

1. 

Sklonuj repozytorium Outline SDK:

2. 

Utwórz pliki binarne Go Mobile za pomocą polecenia [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies):

#### Dodawanie obsługi aplikacji Psiphon

Aby dodać obsługę sieci [Psiphon](https://psiphon.ca/), wykonaj te dodatkowe czynności:

    - Skontaktuj się z zespołem Psiphon, aby otrzymać konfigurację umożliwiającą dostęp do tej sieci. Może to wymagać zawarcia umowy.

    - Dodaj otrzymaną konfigurację Psiphon do sekcji `fallback` konfiguracji `SmartDialer`.

    - 

Skompiluj bibliotekę MobileProxy przy użyciu flagi `-tags psiphon`:

Flaga `-tags psiphon` jest wymagana, ponieważ baza kodu Psiphon jest objęta licencją GPL, która może nakładać ograniczenia licencyjne na Twój własny kod. W związku z tym być może warto uzyskać specjalną licencję od firmy Psiphon.

3. 

Wygeneruj biblioteki mobilne i dodaj je do projektu:

### Android

W Android Studio wybierz **Plik > Importuj projekt…**, aby zaimportować wygenerowany pakiet `out/mobileproxy.aar`. Więcej informacji znajdziesz w instrukcjach [kompilowania i wdrażania aplikacji na Androida](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1) dotyczących Go Mobile.

### iOS

Przeciągnij pakiet `out/mobileproxy.xcframework` do projektu w Xcode. Więcej informacji znajdziesz w instrukcjach [kompilowania i wdrażania aplikacji na iOS](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1) dotyczących Go Mobile.

## Krok 2. Uruchamianie MobileProxy

Zainicjuj i uruchom lokalny serwer proxy `MobileProxy` w środowisku wykonawczym aplikacji.
Możesz użyć statycznej konfiguracji transportu lub inteligentnego serwera proxy, który dynamicznie wybiera strategię.

- 

**Statyczna konfiguracja transportu:** użyj funkcji `RunProxy` z lokalnym adresem i konfiguracją transportu.

### Android

### iOS

- 

**Inteligentny serwer proxy:** ten serwer dynamicznie wybiera strategie DNS i TLS na podstawie określonych domen testowych. Strategię dotyczącą konfiguracji należy określić w formacie YAML ([przykład](https://github.com/Jigsaw-Code/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml)).

### Android

### iOS

## Krok 3. Konfiguracja klientów HTTP i bibliotek sieciowych

Skonfiguruj biblioteki sieciowe, aby używały adresu i portu lokalnego serwera proxy.

### HttpClient Dart/Flutter

Ustaw serwer proxy przy użyciu metody [`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html).

### OkHttp (Android)

Ustaw serwer proxy przy użyciu metody [`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/).

### JVM (Java, Kotlin)

Skonfiguruj serwer proxy za pomocą [właściwości systemowych](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html):

### Android WebView

Zastosuj konfigurację serwera proxy do wszystkich widoków WebView w bibliotece [`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController):

### iOS WebView

Od wersji iOS 17 możesz dodać konfigurację serwera proxy do obiektu `WKWebView` za pomocą jego [właściwości `WKWebsiteDataStore`](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration):

## Zaawansowane: generowanie niestandardowej biblioteki mobilnej

W zaawansowanych przypadkach użycia możesz wygenerować własne biblioteki mobilne:

1. **Tworzenie biblioteki Go:** utwórz pakiet Go zawierający wymagane funkcje SDK.

2. **Generowanie bibliotek mobilnych:** użyj polecenia `gomobile bind`, aby utworzyć pliki Android Archive (AAR) i frameworki Apple. Przykłady:

    - [Plik Android Archive biblioteki Outline](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [Framework Apple biblioteki Outline](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **Integracja aplikacji:** dodaj wygenerowaną bibliotekę do aplikacji mobilnej.
