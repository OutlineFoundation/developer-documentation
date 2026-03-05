---
title: "Add Outline SDK to Your Mobile App"
sidebar_label: "Mobile App Integration"
---

このドキュメントでは、Outline SDK をモバイル アプリケーションに統合する方法を概説します。特に、ローカル プロキシの管理を簡素化するための `MobileProxy` ライブラリに重点を置きます。

`MobileProxy` は、プロキシの機能を効率的にモバイルアプリに統合するための、Go をベースにしたライブラリです。[Go Mobile](https://go.dev/wiki/Mobile) を使用してモバイル ライブラリを生成し、アプリのネットワーキング ライブラリを構成してトラフィックをローカル プロキシにルーティングできるようにします。

**MobileProxy を使用しないアプリ**

![MobileProxy を使用しないコンテンツ アプリ](/images/mobileproxy-before.png)

**MobileProxy を使用するアプリ**

![MobileProxy を使用するコンテンツ アプリ](/images/mobileproxy-after.png)

## ステップ 1: MobileProxy モバイル ライブラリをビルドする

[gomobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile) を使用して Go 言語のコードをコンパイルし、Android 用と iOS 用のライブラリをビルドします。

1. Outline SDK のリポジトリのクローンを作成します:

```sh
git clone https://github.com/Jigsaw-Code/outline-sdk.git
cd outline-sdk/x
```

2. [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies) を使用して Go Mobile のバイナリをビルドします:

```sh
go build -o "$(pwd)/out/" golang.org/x/mobile/cmd/gomobile golang.org/x/mobile/cmd/gobind
```

#### Psiphon サポートを追加する

以下の追加ステップを行うことにより、[Psiphon](https://psiphon.ca/) ネットワークを使用するためのサポートを追加できます:

    - Psiphon のネットワークにアクセスするための構成を入手するには、Psiphon チームに問い合わせてください。これには、契約が必要になる場合があります。

    - 入手した Psiphon の構成を `SmartDialer` の構成の `fallback` セクションに追加します。

    - `-tags psiphon` フラグを使用して Mobile Proxy をビルドします:

```sh
go build -tags psiphon -o "$(pwd)/out/" golang.org/x/mobile/cmd/gomobile golang.org/x/mobile/cmd/gobind
```

`-tags psiphon` フラグが必要なのは、Psiphon のコードベースのライセンスが GPL の元で付与されているからであり、そのため、あなたのコードにもライセンス制限が課される可能性があります。Psiphon から特別なライセンスを取得することも検討してください。

3. モバイル ライブラリを生成し、プロジェクトに追加します:

### Android

```sh
PATH="$(pwd)/out:$PATH" gomobile bind -ldflags='-s -w' -target=android -androidapi=21 -o "$(pwd)/out/mobileproxy.aar" github.com/Jigsaw-Code/outline-sdk/x/mobileproxy
```

Android Studio で **[File] > [Import Project…]** を選択し、生成した `out/mobileproxy.aar` バンドルをインポートします。詳しくは、Go Mobile の[ビルドと Android へのデプロイ](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1)をご覧ください。

### iOS

```sh
PATH="$(pwd)/out:$PATH" gomobile bind -ldflags='-s -w' -target=ios -iosversion=11.0 -o "$(pwd)/out/mobileproxy.xcframework" github.com/Jigsaw-Code/outline-sdk/x/mobileproxy
```

`out/mobileproxy.xcframework` バンドルを Xcode プロジェクトにドラッグします。詳しくは、Go Mobile の[ビルドと iOS へのデプロイ](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1)をご覧ください。

## ステップ 2: MobileProxy を実行する

アプリのランタイム内で `MobileProxy` ローカル プロキシを初期化し、開始します。静的なトランスポート構成を使用することも、動的な戦略選択のために Smart Proxy を使用することも可能です。

- **静的トランスポート構成**: `RunProxy` 関数を使用して、ローカル アドレスとトランスポートを構成します。

### Android

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

### iOS

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

- **Smart Proxy**: Smart Proxy は、指定したテストドメインに応じて DSN と TLS の戦略を動的に選択します。構成の戦略は YAML 形式で指定します（[例](https://github.com/Jigsaw-Code/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml)）。

### Android

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

### iOS

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

## ステップ 3: HTTP クライアントとネットワーキング ライブラリを構成する

ローカル プロキシ アドレスとポートを使用するようにネットワーキング ライブラリを構成します。

### Dart/Flutter HttpClient

[`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html) を使用してプロキシを設定します。

```dart
HttpClient client = HttpClient();
client.findProxy = (Uri uri) {
  return "PROXY " + proxy.address();
};
```

### OkHttp（Android）

[`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/) を使用してプロキシを設定します。

```kotlin
val proxyConfig = Proxy(Proxy.Type.HTTP, InetSocketAddress(proxy.host(), proxy.port()))
val client = OkHttpClient.Builder().proxy(proxyConfig).build()
```

### JVM（Java、Kotlin）

[システム プロパティ](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html)を使用してプロキシを構成します。

```kotlin
System.setProperty("http.proxyHost", proxy.host())
System.setProperty("http.proxyPort", String.valueOf(proxy.port()))
System.setProperty("https.proxyHost", proxy.host())
System.setProperty("https.proxyPort", String.valueOf(proxy.port()))
```

### Android WebView

[`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController) ライブラリを使用して、アプリケーション内のすべての WebView にプロキシの構成を適用します。

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

### iOS WebView

iOS 17 以降では、[`WKWebsiteDataStore` プロパティ](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration)を使用して `WKWebView` にプロキシの構成を追加できます。

```swift
let configuration = WKWebViewConfiguration()
let endpoint = NWEndpoint.hostPort(host: NWEndpoint.Host(proxyHost), port: NWEndpoint.Port(proxyPort)!)
let proxyConfig = ProxyConfiguration.init(httpCONNECTProxy: endpoint)
let websiteDataStore = WKWebsiteDataStore.default()
websiteDataStore.proxyConfigurations = [proxyConfig]
let webview = WKWebView(configuration: configuration)
```

## 高度な用例: カスタム モバイル ライブラリを生成する

高度な用例として、独自のモバイル ライブラリを生成することも可能です。

1. **Go ライブラリを作成する**: 必要な SDK 機能をラップした Go パッケージを作成します。

2. **モバイル ライブラリを生成する**: `gomobile bind` を使用して Android ARchive（AAR）と Apple フレームワークを作成します。例:

    - [Outline Android ARchive](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [Outline Apple フレームワーク](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **アプリに統合する**: 生成したライブラリをモバイル アプリケーションに追加します。
