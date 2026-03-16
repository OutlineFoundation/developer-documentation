---
title: "Add Outline SDK to Your Mobile App"
sidebar_label: "Mobile App Integration"
---

Bu belgede, Outline SDK'yı mobil uygulamalarınıza nasıl entegre edeceğiniz açıklanmaktadır. Basitleştirilmiş yerel proxy yönetimi için `MobileProxy` kitaplığına odaklanılmıştır.

Go temelli bir kitaplık olan `MobileProxy`, proxy işlevlerini mobil uygulamalara entegrasyonunu iyileştirmek için tasarlanmıştır. Mobil uygulama kitaplıklarını oluşturmak için [Go Mobile](https://go.dev/wiki/Mobile)'dan yararlanır. Böylece, uygulamanızın ağ kitaplıklarını trafiği yerel bir proxy üzerinden yönlendirecek şekilde yapılandırabilirsiniz.

**MobileProxy kullanılmayan uygulama**

![MobileProxy kullanılmayan içerik uygulaması](/images/mobileproxy-before.png)

**MobileProxy kullanılan uygulama**

![MobileProxy kullanılan içerik uygulaması](/images/mobileproxy-after.png)

## 1. adım: MobileProxy mobil uygulama kitaplıklarını oluşturun {#step_1_building_mobileproxy_mobile_libraries}

Go kodunu Android ve iOS'e yönelik kitaplıklar hâlinde derlemek için [gomobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile)'ı kullanın.

1. Outline SDK deposunu klonlayın:

```sh
git clone https://github.com/OutlineFoundation/outline-sdk.git
cd outline-sdk/x
```

2. [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies) ile Go Mobile ikili programlarını derleyin:

```sh
go build -o "$(pwd)/out/" golang.org/x/mobile/cmd/gomobile golang.org/x/mobile/cmd/gobind
```

#### Psiphon desteği ekleme {#adding_psiphon_support}

Şu ek adımları izleyerek [Psiphon](https://psiphon.ca/) ağını kullanma desteği ekleyebilirsiniz:

    - Psiphon ekibine ulaşarak ağlarına erişim sağlayan bir yapılandırma alın. Bunun için bir sözleşmenizin olması gerekebilir.

    - Aldığınız Psiphon yapılandırmasını, `SmartDialer` yapılandırmanızın `fallback` bölümüne ekleyin.

    - `-tags psiphon` işaretini kullanarak MobileProxy'yi derleyin:

```sh
go build -tags psiphon -o "$(pwd)/out/" golang.org/x/mobile/cmd/gomobile golang.org/x/mobile/cmd/gobind
```

Psiphon kod tabanı GPL kapsamında lisanslandığından kodunuza lisans kısıtlamaları uygulanabilir. Bu nedenle `-tags psiphon` işareti zorunludur. Psiphon ekibinden özel bir lisans almanız önerilir.

3. Mobil uygulama kitaplıklarını oluşturun ve projenize ekleyin:

### Android {#android}

```sh
PATH="$(pwd)/out:$PATH" gomobile bind -ldflags='-s -w' -target=android -androidapi=21 -o "$(pwd)/out/mobileproxy.aar" github.com/OutlineFoundation/outline-sdk/x/mobileproxy
```

Oluşturulan `out/mobileproxy.aar` paketini içe aktarmak için Android Studio'da **Dosya > Projeyi İçe Aktar…** seçeneğini belirleyin. Daha fazla yardım için Go Mobile'ın [Building and deploying to Android](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1) (Uygulama derleme ve Android'e dağıtma) başlıklı bölümünü inceleyin.

### iOS {#ios}

```sh
PATH="$(pwd)/out:$PATH" gomobile bind -ldflags='-s -w' -target=ios -iosversion=11.0 -o "$(pwd)/out/mobileproxy.xcframework" github.com/OutlineFoundation/outline-sdk/x/mobileproxy
```

`out/mobileproxy.xcframework` paketini Xcode projesine sürükleyin. Daha fazla yardım için Go Mobile'ın [Building and deploying to Android](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1) (Uygulama derleme ve iOS'e dağıtma) başlıklı bölümünü inceleyin.

## 2. adım: MobileProxy'yi çalıştırın {#step_2_run_the_mobileproxy}

`MobileProxy` yerel proxy'sini uygulamanızın çalışma zamanında başlatın.
Dinamik strateji seçimi için statik bir araç yapısı ya da akıllı proxy kullanabilirsiniz.

- **Statik araç yapılandırması**: Yerel bir adres ve araç yapılandırmasıyla `RunProxy` işlevini kullanın.

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

- **Akıllı proxy**: Akıllı proxy, DNS ve TLS stratejilerini belirtilen test alan adlarına göre dinamik olarak seçer. Yapılandırma stratejisini YAML biçiminde ([örnek](https://github.com/OutlineFoundation/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml)) belirtmeniz gerekir.

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

## 3. adım: HTTP istemcilerini ve ağ kitaplıklarını yapılandırın {#step_3_configure_http_clients_and_networking_libraries}

Ağ kitaplıklarınızı yerel proxy adresini ve bağlantı noktasını kullanacak şekilde yapılandırın.

### Dart/Flutter HttpClient {#dartflutter-httpclient}

Proxy'yi [`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html) ile ayarlayın.

```dart
HttpClient client = HttpClient();
client.findProxy = (Uri uri) {
  return "PROXY " + proxy.address();
};
```

### OkHttp (Android) {#okhttp-android}

Proxy'yi [`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/) ile ayarlayın.

```kotlin
val proxyConfig = Proxy(Proxy.Type.HTTP, InetSocketAddress(proxy.host(), proxy.port()))
val client = OkHttpClient.Builder().proxy(proxyConfig).build()
```

### JVM (Java, Kotlin) {#jvm-java,-kotlin}

Proxy'yi [sistem özellikleriyle](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html) kullanılacak şekilde yapılandırın:

```kotlin
System.setProperty("http.proxyHost", proxy.host())
System.setProperty("http.proxyPort", String.valueOf(proxy.port()))
System.setProperty("https.proxyHost", proxy.host())
System.setProperty("https.proxyPort", String.valueOf(proxy.port()))
```

### Android Web Görünümü {#android-web-view}

[`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController) kitaplığını kullanarak uygulamanızdaki tüm web görünümlerine bir proxy yapılandırması uygulayın:

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

### iOS Web Görünümü {#ios-web-view}

iOS 17 sürümünden itibaren, [`WKWebsiteDataStore` özelliğini](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration) kullanarak `WKWebView` görünümüne proxy yapılandırması uygulayabilirsiniz:

```swift
let configuration = WKWebViewConfiguration()
let endpoint = NWEndpoint.hostPort(host: NWEndpoint.Host(proxyHost), port: NWEndpoint.Port(proxyPort)!)
let proxyConfig = ProxyConfiguration.init(httpCONNECTProxy: endpoint)
let websiteDataStore = WKWebsiteDataStore.default()
websiteDataStore.proxyConfigurations = [proxyConfig]
let webview = WKWebView(configuration: configuration)
```

## İleri düzey: Özel mobil uygulama kitaplığı oluşturma {#advanced_generate_a_custom_mobile_library}

İleri düzey kullanım alanları için kendi mobil uygulama kitaplıklarınızı oluşturabilirsiniz:

1. **Go kitaplığı oluşturma**: Zorunlu SDK işlevlerini sarmalayan bir Go paketi oluşturun.

2. **Mobil uygulama kitaplıkları oluşturma**: Android Archive (AAR) ve Apple çerçeveleri oluşturmak için `gomobile bind` komutunu kullanın. Örnekler:

    - [Outline Android Archive](https://github.com/OutlineFoundation/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [Outline Apple Çerçevesi](https://github.com/OutlineFoundation/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **Uygulamanıza entegre etme**: Oluşturulan kitaplığı mobil uygulamanıza ekleyin.
