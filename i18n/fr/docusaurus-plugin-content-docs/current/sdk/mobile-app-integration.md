---
title: "Ajouter le SDK Outline à votre application mobile"
sidebar_label: "Ajouter le SDK Outline à votre application mobile"
---

Ce document explique comment intégrer le SDK Outline à des applications mobiles et se concentre sur la bibliothèque `MobileProxy` afin de simplifier la gestion des proxys locaux.

`MobileProxy` est une bibliothèque basée sur Go conçue pour simplifier l'intégration de fonctionnalités de proxy dans les applications mobiles. Elle utilise [Go Mobile](https://go.dev/wiki/Mobile) pour générer des bibliothèques mobiles. Vous pouvez ainsi configurer les bibliothèques réseau de vos applications pour acheminer le trafic via un proxy local.

**Application sans MobileProxy**

![Application de contenu sans MobileProxy](/images/mobileproxy-before.png)

**Application avec MobileProxy**

![Application de contenu avec MobileProxy](/images/mobileproxy-after.png)

## Étape 1 : Créer des bibliothèques mobiles MobileProxy {#step_1_building_mobileproxy_mobile_libraries}

Utilisez [gomobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile) pour compiler le code Go en bibliothèques pour Android et iOS.

1. Clonez le dépôt du SDK Outline :

```sh
git clone https://github.com/OutlineFoundation/outline-sdk.git
cd outline-sdk/x
```

2. Créez les binaires Go Mobile avec [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies) :

```sh
go build -o "$(pwd)/out/" golang.org/x/mobile/cmd/gomobile golang.org/x/mobile/cmd/gobind
```

#### Ajouter la compatibilité Psiphon {#adding_psiphon_support}

Vous pouvez rendre possible l'utilisation du réseau [Psiphon](https://psiphon.ca/) en suivant ces étapes :

    - Contactez l'équipe Psiphon pour obtenir une configuration qui vous donne accès à son réseau. Un contrat peut être nécessaire.

    - Ajoutez la configuration Psiphon reçue à la section `fallback` de votre configuration `SmartDialer`.

    - Créez le MobileProxy à l'aide de l'option `-tags psiphon` :

```sh
go build -tags psiphon -o "$(pwd)/out/" golang.org/x/mobile/cmd/gomobile golang.org/x/mobile/cmd/gobind
```

L'option `-tags psiphon` est nécessaire, car le codebase Psiphon est sous licence GPL, ce qui peut imposer des restrictions de licence à votre propre code. Vous pouvez envisager d'obtenir une licence spéciale auprès de Psiphon.

3. Générez les bibliothèques mobiles et ajoutez-les à votre projet :

### Android {#android}

```sh
PATH="$(pwd)/out:$PATH" gomobile bind -ldflags='-s -w' -target=android -androidapi=21 -o "$(pwd)/out/mobileproxy.aar" github.com/OutlineFoundation/outline-sdk/x/mobileproxy
```

Dans Android Studio, sélectionnez **File > Import Project** (Fichier > Importer un projet) pour importer le bundle `out/mobileproxy.aar` généré. Pour en savoir plus, consultez la section sur [la création et le déploiement sur Android](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1) de la documentation Go Mobile.

### iOS {#ios}

```sh
PATH="$(pwd)/out:$PATH" gomobile bind -ldflags='-s -w' -target=ios -iosversion=11.0 -o "$(pwd)/out/mobileproxy.xcframework" github.com/OutlineFoundation/outline-sdk/x/mobileproxy
```

Faites glisser le bundle `out/mobileproxy.xcframework` dans le projet Xcode. Pour en savoir plus, consultez la section sur [la création et le déploiement sur iOS](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1) de la documentation Go Mobile.

## Étape 2 : Exécuter le MobileProxy {#step_2_run_the_mobileproxy}

Initialisez et lancez le proxy local `MobileProxy` dans l'environnement d'exécution de votre application.
Vous pouvez utiliser une configuration de transport statique ou le Smart Proxy pour sélectionner une stratégie de façon dynamique.

- **Configuration de transport statique** : utilisez la fonction `RunProxy` en incluant une adresse locale et une configuration de transport.

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

- **Smart Proxy** : le Smart Proxy sélectionne des stratégies DNS et TLS de façon dynamique en fonction des domaines de test spécifiés. Vous devez spécifier la stratégie de configuration au format YAML ([exemple](https://github.com/OutlineFoundation/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml)).

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

## Étape 3 : Configurer les clients HTTP et les bibliothèques réseau {#step_3_configure_http_clients_and_networking_libraries}

Configurez vos bibliothèques réseau pour qu'elles utilisent l'adresse et le port du proxy local.

### HttpClient Dart/Flutter {#dartflutter-httpclient}

Configurez le proxy avec [`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html).

```dart
HttpClient client = HttpClient();
client.findProxy = (Uri uri) {
  return "PROXY " + proxy.address();
};
```

### OkHttp (Android) {#okhttp-android}

Configurez le proxy avec [`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/).

```kotlin
val proxyConfig = Proxy(Proxy.Type.HTTP, InetSocketAddress(proxy.host(), proxy.port()))
val client = OkHttpClient.Builder().proxy(proxyConfig).build()
```

### JVM (Java, Kotlin) {#jvm-java,-kotlin}

Configurez le proxy avec les [propriétés système](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html) :

```kotlin
System.setProperty("http.proxyHost", proxy.host())
System.setProperty("http.proxyPort", String.valueOf(proxy.port()))
System.setProperty("https.proxyHost", proxy.host())
System.setProperty("https.proxyPort", String.valueOf(proxy.port()))
```

### WebView Android {#android-web-view}

Appliquez une configuration de proxy à toutes les vues Web de votre application avec la bibliothèque [`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController) :

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

### WebView iOS {#ios-web-view}

À partir d'iOS 17, vous pouvez ajouter une configuration de proxy à une `WKWebView` en utilisant sa [propriété `WKWebsiteDataStore`](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration) :

```swift
let configuration = WKWebViewConfiguration()
let endpoint = NWEndpoint.hostPort(host: NWEndpoint.Host(proxyHost), port: NWEndpoint.Port(proxyPort)!)
let proxyConfig = ProxyConfiguration.init(httpCONNECTProxy: endpoint)
let websiteDataStore = WKWebsiteDataStore.default()
websiteDataStore.proxyConfigurations = [proxyConfig]
let webview = WKWebView(configuration: configuration)
```

## Options avancées : générer une bibliothèque mobile personnalisée {#advanced_generate_a_custom_mobile_library}

Pour les cas d'utilisation avancés, vous pouvez générer vos propres bibliothèques mobiles :

1. **Créez une bibliothèque Go** : créez un package Go réunissant les fonctionnalités de SDK nécessaires.

2. **Générez des bibliothèques mobiles** : utilisez `gomobile bind` pour créer des archives Android (AAR) et des frameworks Apple. Exemples :

    - [Archive Android Outline](https://github.com/OutlineFoundation/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [Framework Apple Outline](https://github.com/OutlineFoundation/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **Intégrez-les à votre application** : ajoutez les bibliothèques générées à votre application mobile.
