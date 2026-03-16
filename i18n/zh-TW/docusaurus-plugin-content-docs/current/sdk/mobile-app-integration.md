---
title: "在行動應用程式中加入 Outline SDK"
sidebar_label: "在行動應用程式中加入 Outline SDK"
---

本文件說明如何在行動應用程式中整合 Outline SDK，重點介紹如何運用 `MobileProxy` 程式庫簡化本機 Proxy 管理。

`MobileProxy` 是用 Go 編寫的程式庫，可協助您輕鬆將 Proxy 功能整合至行動應用程式。這個程式庫會運用 [Go Mobile](https://go.dev/wiki/Mobile) 生成行動程式庫，讓您能設定應用程式的網路程式庫，將流量導向本機 Proxy。

**不使用 MobileProxy 的應用程式**

![不使用 MobileProxy 的內容應用程式](/images/mobileproxy-before.png)

**使用 MobileProxy 的應用程式**

![使用 MobileProxy 的內容應用程式](/images/mobileproxy-after.png)

## 步驟 1：建立 MobileProxy 行動程式庫 {#step_1_building_mobileproxy_mobile_libraries}

使用 [gomobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile) 將 Go 程式碼編譯成 Android 和 iOS 程式庫。

1. 複製 Outline SDK 存放區：

```sh
git clone https://github.com/OutlineFoundation/outline-sdk.git
cd outline-sdk/x
```

2. 使用 [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies) 建構 Go Mobile 二進位檔：

```sh
go build -o "$(pwd)/out/" golang.org/x/mobile/cmd/gomobile golang.org/x/mobile/cmd/gobind
```

#### 新增 Psiphon 支援 {#adding_psiphon_support}

如果想讓應用程式也能使用 [Psiphon](https://psiphon.ca/) 網路，的支援，請額外執行下列步驟：

    - 聯絡 Psiphon 團隊，取得可連上他們網路的設定。這可能需要簽訂合約。

    - 將取得的 Psiphon 設定加入 `SmartDialer` 設定的 `fallback` 區塊。

    - 使用 `-tags psiphon` 標記建構 MobileProxy：

```sh
go build -tags psiphon -o "$(pwd)/out/" golang.org/x/mobile/cmd/gomobile golang.org/x/mobile/cmd/gobind
```

建構時需要加上 `-tags psiphon`，因為 Psiphon 採用 GPL 授權，可能對您的程式碼授權造成限制。建議您考慮向 Psiphon 團隊洽談特殊授權。

3. 生成行動程式庫並加入專案：

### Android {#android}

```sh
PATH="$(pwd)/out:$PATH" gomobile bind -ldflags='-s -w' -target=android -androidapi=21 -o "$(pwd)/out/mobileproxy.aar" github.com/OutlineFoundation/outline-sdk/x/mobileproxy
```

在 Android Studio 中依序選取「檔案」>「匯入專案…」****，即可匯入生成的 `out/mobileproxy.aar` 套件。如需其他協助，請參閱 Go Mobile 的「[建構並部署至 Android](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1)」。

### iOS {#ios}

```sh
PATH="$(pwd)/out:$PATH" gomobile bind -ldflags='-s -w' -target=ios -iosversion=11.0 -o "$(pwd)/out/mobileproxy.xcframework" github.com/OutlineFoundation/outline-sdk/x/mobileproxy
```

將 `out/mobileproxy.xcframework` 套件拖曳至 Xcode 專案中。如需其他協助，請參閱 Go Mobile 的「[建構並部署至 iOS](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1)」。

## 步驟 2：執行 MobileProxy {#step_2_run_the_mobileproxy}

在應用程式執行期間，初始化並啟動 `MobileProxy` 本機 Proxy。您可以使用靜態傳輸設定，或由 Smart Proxy 動態選擇策略。

- **靜態傳輸設定**：使用 `RunProxy` 函式，搭配本機位址和傳輸設定。

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

- **Smart Proxy**：Smart Proxy 會根據指定的測試網域，動態選擇 DNS 和 TLS 策略。您需要以 YAML 格式指定設定策略 ([範例](https://github.com/OutlineFoundation/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml))。

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

## 步驟 3：設定 HTTP 用戶端和網路程式庫 {#step_3_configure_http_clients_and_networking_libraries}

請將您的網路程式庫設為使用本機 Proxy 位址和通訊埠。

### Dart/Flutter HttpClient {#dartflutter-httpclient}

使用 [`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html) 設定 Proxy。

```dart
HttpClient client = HttpClient();
client.findProxy = (Uri uri) {
  return "PROXY " + proxy.address();
};
```

### OkHttp (Android) {#okhttp-android}

使用 [`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/) 設定 Proxy。

```kotlin
val proxyConfig = Proxy(Proxy.Type.HTTP, InetSocketAddress(proxy.host(), proxy.port()))
val client = OkHttpClient.Builder().proxy(proxyConfig).build()
```

### JVM (Java、Kotlin) {#jvm-java,-kotlin}

透過[系統屬性](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html)設定要使用的 Proxy：

```kotlin
System.setProperty("http.proxyHost", proxy.host())
System.setProperty("http.proxyPort", String.valueOf(proxy.port()))
System.setProperty("https.proxyHost", proxy.host())
System.setProperty("https.proxyPort", String.valueOf(proxy.port()))
```

### Android WebView {#android-web-view}

使用 [`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController) 程式庫，將 Proxy 設定套用至應用程式的所有網頁檢視畫面：

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

自 iOS 17 起，您可以使用 [`WKWebsiteDataStore`](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration) 屬性將 Proxy 設定套用至 `WKWebView`：

```swift
let configuration = WKWebViewConfiguration()
let endpoint = NWEndpoint.hostPort(host: NWEndpoint.Host(proxyHost), port: NWEndpoint.Port(proxyPort)!)
let proxyConfig = ProxyConfiguration.init(httpCONNECTProxy: endpoint)
let websiteDataStore = WKWebsiteDataStore.default()
websiteDataStore.proxyConfigurations = [proxyConfig]
let webview = WKWebView(configuration: configuration)
```

## 進階：產生自訂行動程式庫 {#advanced_generate_a_custom_mobile_library}

如有進階需求，您可以自行製作行動程式庫：

1. **建立 Go 程式庫**：開發包含所需 SDK 功能的 Go 套件。

2. **產生行動程式庫**：使用 `gomobile bind` 產生 Android ARchive (AAR) 和 Apple 框架。範例：

    - [Outline Android ARchive](https://github.com/OutlineFoundation/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [Outline Apple 框架](https://github.com/OutlineFoundation/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **整合進應用程式**：將產生的程式庫加入行動應用程式。
