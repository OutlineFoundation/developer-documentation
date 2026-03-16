---
title: "Add Outline SDK to Your Mobile App"
sidebar_label: "Mobile App Integration"
---

이 문서에서는 모바일 애플리케이션에 Outline SDK를 통합하는 방법을 간략하게 설명하며, 특히 로컬 프록시 관리를 간소화하는 `MobileProxy` 라이브러리를 중점적으로 살펴봅니다.

`MobileProxy`는 모바일 앱에 프록시 기능을 간편하게 통합하도록 설계된 Go 기반 라이브러리입니다. [Go Mobile](https://go.dev/wiki/Mobile)을 활용하여 모바일 라이브러리를 생성하고, 앱의 네트워킹 라이브러리를 구성하여 로컬 프록시를 통해 트래픽을 라우팅할 수 있습니다.

**MobileProxy를 사용하지 않는 앱**

![MobileProxy를 사용하지 않는 콘텐츠 앱](/images/mobileproxy-before.png)

**MobileProxy를 사용하는 앱**

![MobileProxy를 사용하는 콘텐츠 앱](/images/mobileproxy-after.png)

## 1단계: MobileProxy 모바일 라이브러리 빌드하기 {#step_1_building_mobileproxy_mobile_libraries}

[gomobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile)을 사용하여 Go 코드를 Android 및 IOS용 라이브러리로 컴파일합니다.

1. Outline SDK 저장소를 클론합니다.

```sh
git clone https://github.com/Jigsaw-Code/outline-sdk.git
cd outline-sdk/x
```

2. [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies) 명령어를 사용하여 Go Mobile 바이너리를 빌드합니다.

```sh
go build -o "$(pwd)/out/" golang.org/x/mobile/cmd/gomobile golang.org/x/mobile/cmd/gobind
```

#### Psiphon 지원 추가하기 {#adding_psiphon_support}

다음의 추가 단계에 따라 [Psiphon](https://psiphon.ca/) 네트워크 사용에 대한 지원을 추가할 수 있습니다.

    - Psiphon팀에 문의하여 해당 네트워크에 액세스할 수 있는 구성 정보를 받습니다. 계약이 필요할 수도 있습니다.

    - 수신한 Psiphon 구성 정보를 `SmartDialer` 구성의 `fallback` 섹션에 추가합니다.

    - `-tags psiphon` 플래그를 사용하여 모바일 프록시 빌드하기

```sh
go build -tags psiphon -o "$(pwd)/out/" golang.org/x/mobile/cmd/gomobile golang.org/x/mobile/cmd/gobind
```

Psiphon 코드베이스는 GPL 라이선스를 따르므로, 사용자의 코드에 라이선스 제한이 적용될 수 있습니다. 따라서 `-tags psiphon` 플래그가 필요합니다. Psiphon의 별도 라이선스 취득을 고려할 수도 있습니다.

3. 모바일 라이브러리를 생성하여 다음과 같이 프로젝트에 추가합니다.

### Android {#android}

```sh
PATH="$(pwd)/out:$PATH" gomobile bind -ldflags='-s -w' -target=android -androidapi=21 -o "$(pwd)/out/mobileproxy.aar" github.com/Jigsaw-Code/outline-sdk/x/mobileproxy
```

Android 스튜디오에서 **파일 > 프로젝트 가져오기…**를 선택하여 생성된 `out/mobileproxy.aar` 번들을 가져옵니다. 도움이 더 필요하면 Go Mobile의 [Android 빌드 및 배포](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1)를 참고하세요.

### iOS {#ios}

```sh
PATH="$(pwd)/out:$PATH" gomobile bind -ldflags='-s -w' -target=ios -iosversion=11.0 -o "$(pwd)/out/mobileproxy.xcframework" github.com/Jigsaw-Code/outline-sdk/x/mobileproxy
```

`out/mobileproxy.xcframework` 번들을 Xcode 프로젝트로 드래그합니다. 도움이 더 필요하면 Go Mobile의 [iOS 빌드 및 배포](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1)를 참고하세요.

## 2단계: MobileProxy 실행하기 {#step_2_run_the_mobileproxy}

앱 런타임 내에서 `MobileProxy` 로컬 프록시를 초기화하고 시작합니다.
정적 전송 구성이나 동적 전략 선택을 위한 스마트 프록시 중 하나를 사용할 수 있습니다.

- **정적 전송 구성**: 로컬 주소 및 전송 구성과 함께 `RunProxy` 기능을 사용합니다.

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

- **스마트 프록시**: 스마트 프록시는 지정된 테스트 도메인을 기반으로 DNS 및 TLS 전략을 동적으로 선택합니다. YAML 형식의 구성 전략을 지정해야 합니다([예](https://github.com/Jigsaw-Code/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml)).

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

## 3단계: HTTP 클라이언트 및 네트워킹 라이브러리 구성하기 {#step_3_configure_http_clients_and_networking_libraries}

로컬 프록시 주소 및 포트를 사용하기 위한 네트워킹 라이브러리를 구성합니다.

### Dart/Flutter HttpClient {#dartflutter-httpclient}

[`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html)를 사용하여 프록시를 설정합니다.

```dart
HttpClient client = HttpClient();
client.findProxy = (Uri uri) {
  return "PROXY " + proxy.address();
};
```

### OkHttp(Android) {#okhttp-android}

[`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/)를 사용하여 프록시를 설정합니다.

```kotlin
val proxyConfig = Proxy(Proxy.Type.HTTP, InetSocketAddress(proxy.host(), proxy.port()))
val client = OkHttpClient.Builder().proxy(proxyConfig).build()
```

### JVM(Java, Kotlin) {#jvm-java,-kotlin}

[시스템 속성](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html)과 함께 사용할 프록시를 구성합니다:

```kotlin
System.setProperty("http.proxyHost", proxy.host())
System.setProperty("http.proxyPort", String.valueOf(proxy.port()))
System.setProperty("https.proxyHost", proxy.host())
System.setProperty("https.proxyPort", String.valueOf(proxy.port()))
```

### Android 웹 뷰 {#android-web-view}

[`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController) 라이브러리를 사용하여 애플리케이션의 모든 웹 뷰에 프록시 구성을 적용합니다.

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

### iOS 웹 뷰 {#ios-web-view}

iOS 17부터 [`WKWebsiteDataStore` 속성](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration)을 사용하여 `WKWebView`에 프록시 구성을 추가할 수 있습니다.

```swift
let configuration = WKWebViewConfiguration()
let endpoint = NWEndpoint.hostPort(host: NWEndpoint.Host(proxyHost), port: NWEndpoint.Port(proxyPort)!)
let proxyConfig = ProxyConfiguration.init(httpCONNECTProxy: endpoint)
let websiteDataStore = WKWebsiteDataStore.default()
websiteDataStore.proxyConfigurations = [proxyConfig]
let webview = WKWebView(configuration: configuration)
```

## 고급: 맞춤 모바일 라이브러리 생성하기 {#advanced_generate_a_custom_mobile_library}

고급 사용 사례의 경우 다음과 같이 직접 모바일 라이브러리를 생성할 수 있습니다.

1. **Go 라이브러리 만들기**: 필수 SDK 기능을 포함하는 Go 패키지를 개발합니다.

2. **모바일 라이브러리 생성하기**: `gomobile bind` 코드를 사용하여 Android 보관 파일(AAR) 및 Apple 프레임워크를 생성합니다. 예를 들면 다음과 같습니다.

    - [Outline Android 보관 파일](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [Outline Apple 프레임워크](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **앱에 통합하기**: 생성된 라이브러리를 모바일 애플리케이션에 추가합니다.
