---
title: "Add Outline SDK to Your Mobile App"
sidebar_label: "Mobile App Integration"
---

In dit document leggen we uit hoe je de Outline SDK integreert in je mobiele apps. We richten ons hierbij op de `MobileProxy`-bibliotheek voor eenvoudig beheer van lokale proxy's.

`MobileProxy` is een Go-gebaseerde bibliotheek, gemaakt om de integratie van proxyfuncties in mobiele apps te stroomlijnen. De bibliotheek gebruikt [Go Mobile](https://go.dev/wiki/Mobile) om mobiele bibliotheken te genereren. Zo kun je de netwerkbibliotheken van je app instellen om verkeer door een lokale proxy te routeren.

**App zonder MobileProxy**

![Content van app zonder MobileProxy](/images/mobileproxy-before.png)

**App met MobileProxy**

![Content van app met MobileProxy](/images/mobileproxy-after.png)

## Stap 1: Mobiele MobileProxy-bibliotheken ontwerpen

Gebruik [gomobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile) om de Go-code te compileren in bibliotheken voor Android en iOS.

1. Kloon de Outline SDK-repository:

2. Ontwerp de binaire bestanden voor Go Mobile met [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies):

#### Psiphon-ondersteuning toevoegen

Je kunt ondersteuning voor het [Psiphon](https://psiphon.ca/)-netwerk toevoegen door deze extra stappen te volgen:

    - Vraag het Psiphon-team om een configuratie waarmee je toegang krijgt tot hun netwerk. Je moet hiervoor misschien een contract aangaan.

    - Voeg de Psiphon-configuratie die je hebt gekregen toe aan het gedeelte `fallback` van je `SmartDialer`-configuratie.

    - Ontwerp de MobileProxy met de markering `-tags psiphon`:

De markering `-tags psiphon` is vereist omdat de Psiphon-codebase is gelicentieerd onder de GPL, waardoor er licentiebeperkingen kunnen gelden voor je eigen code. Je kunt overwegen een speciale licentie bij ze aan te vragen.

3. Genereer mobiele bibliotheken en voeg ze toe aan je project:

### Android

Selecteer in Android Studio de optie **Bestand > Project importeren…** om het gegenereerde `out/mobileproxy.aar`-pakket te importeren. Ga voor meer hulp naar [Building and deploying to Android](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1) van Go Mobile.

### iOS

Sleep het `out/mobileproxy.xcframework`-pakket naar het Xcode-project. Ga voor meer hulp naar [Building and deploying to iOS](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1) van Go Mobile.

## Stap 2: Voer de MobileProxy uit

Initialiseer en start de lokale `MobileProxy`-proxy binnen de runtime van je app.
Je kunt een statische transportconfiguratie gebruiken of de Smart Proxy gebruiken voor dynamische strategieselectie.

- **Statische transportconfiguratie**: Gebruik de functie `RunProxy` met een lokaal adres en lokale transportconfiguratie.

### Android

### iOS

- **Smart Proxy**: De Smart Proxy selecteert dynamisch DNS- en TLS-strategieën gebaseerd op specifieke testdomeinen. Je moet de configuratiestrategie opgeven in YAML-indeling ([voorbeeld](https://github.com/Jigsaw-Code/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml)).

### Android

### iOS

## Stap 3: Stel HTTP-clients en netwerkbibliotheken in

Stel in dat je netwerkbibliotheken het lokale proxyadres en -poort gebruiken.

### Dart/Flutter HttpClient

Stel de proxy in met [`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html).

### OkHttp (Android)

Stel de proxy in met [`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/).

### JVM (Java, Kotlin)

Stel via de [systeemeigenschappen](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html) in welke proxy moet worden gebruikt:

### Android WebView

Pas een proxyconfiguratie toe op alle webweergaven in je app met de [`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController)-bibliotheek:

### iOS WebView

Vanaf iOS 17 kun je een proxyconfiguratie toevoegen aan een `WKWebView` met het [kenmerk `WKWebsiteDataStore`](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration):

## Geavanceerd: Een aangepaste mobiele bibliotheek maken

Voor geavanceerde use cases kun je je eigen mobiele bibliotheken maken:

1. **Een Go-bibliotheek maken**: Ontwikkel een Go-pakket waarin de vereiste SDK-functies zijn verpakt.

2. **Mobiele bibliotheken maken**: Gebruik `gomobile bind` om Android ARchives (AAR) en Apple Frameworks te produceren. Voorbeelden:

    - [Android ARchive voor Outline](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [Apple Framework voor Outline](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **Integreren in je app**: Voeg de gemaakte bibliotheek toe aan je mobiele app.
