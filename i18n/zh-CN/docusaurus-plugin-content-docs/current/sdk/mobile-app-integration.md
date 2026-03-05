---
title: "Add Outline SDK to Your Mobile App"
sidebar_label: "Mobile App Integration"
---

本文档概述了如何将 Outline SDK 集成到移动应用中，并重点讲解如何使用 `MobileProxy` 库简化本地代理管理。

`MobileProxy` 是一个基于 Go 的库，旨在简化将代理服务器功能集成到移动应用中的流程。该库利用 [Go Mobile](https://go.dev/wiki/Mobile) 生成移动端库，让您能够配置应用的网络库，将流量通过本地代理进行传输。

**不使用 MobileProxy 的应用**

![不使用 MobileProxy 的内容应用](/images/mobileproxy-before.png)

**使用 MobileProxy 的应用**

![使用 MobileProxy 的内容应用](/images/mobileproxy-after.png)

## 第 1 步：构建 MobileProxy 移动端库

使用 [gomobile](https://pkg.go.dev/golang.org/x/mobile/cmd/gomobile) 将 Go 代码编译为 Android 和 iOS 库。

1. 克隆 Outline SDK 仓库：

2. 使用 [`go
build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies) 构建 Go Mobile 二进制文件：

#### 添加 Psiphon 支持

要想让应用支持使用 [Psiphon](https://psiphon.ca/) 网络，请按以下额外步骤操作：

    - 与 Psiphon 团队联系，获取用于访问其网络的配置，可能需要签订合同。

    - 将获得的 Psiphon 配置添加到 `SmartDialer` 配置的 `fallback` 部分。

    - 使用 `-tags psiphon` 标记构建 MobileProxy：

由于 Psiphon 代码库基于 GPL 协议授予许可，可能会对您的代码施加许可限制，因此需要使用 `-tags psiphon` 标记。您可能需要考虑申请特殊许可。

3. 生成移动端库并将其添加到项目中：

### Android

在 Android Studio 中，依次选择**文件 > 导入项目…**，导入生成的 `out/mobileproxy.aar` 软件包。如需获取更多帮助，请参阅 Go Mobile 的[构建并部署到 Android](https://go.dev/wiki/Mobile#building-and-deploying-to-android-1)。

### iOS

将 `out/mobileproxy.xcframework` 软件包拖放到 Xcode 项目中。如需获取更多帮助，请参阅 Go Mobile 的[构建并部署到 iOS](https://go.dev/wiki/Mobile#building-and-deploying-to-ios-1)。

## 第 2 步：运行 MobileProxy

在应用的运行时内初始化并启动 `MobileProxy` 本地代理服务器。您可以使用静态传输配置，或通过 Smart Proxy 实现动态策略选择。

- **静态传输配置**：将 `RunProxy` 函数与本地地址和传输配置结合使用。

### Android

### iOS

- **Smart Proxy**：Smart Proxy 可根据指定的测试网域动态选择 DNS 和 TLS 策略。您需要以 YAML 格式指定配置策略（[示例](https://github.com/Jigsaw-Code/outline-sdk/blob/master/x/examples/smart-proxy/config.yaml)）。

### Android

### iOS

## 第 3 步：配置 HTTP 客户端和网络库

配置网络库以使用本地代理服务器地址和端口。

### Dart/Flutter HttpClient

通过 [`HttpClient.findProxy`](https://api.flutter.dev/flutter/dart-io/HttpClient/findProxy.html) 设置代理服务器。

### OkHttp (Android)

通过 [`OkHttpClient.Builder.proxy`](https://square.github.io/okhttp/4.x/okhttp/okhttp3/-ok-http-client/-builder/proxy/) 设置代理服务器。

### JVM（Java、Kotlin）

使用[系统属性](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html)配置要使用的代理服务器：

### Android WebView

通过 [`androidx.webview`](https://developer.android.com/reference/androidx/webkit/ProxyController) 库将代理服务器配置应用于应用中的所有 WebView：

### iOS WebView

从 iOS 17 开始，您可以使用 [`WKWebsiteDataStore` 属性](https://developer.apple.com/documentation/webkit/wkwebviewconfiguration)将代理服务器配置添加到 `WKWebView`：

## 高级：生成自定义移动端库

对于高级应用场景，您可以生成自己的移动端库：

1. **创建 Go 库**：开发一个封装了所需 SDK 功能的 Go 库。

2. **生成移动端库**：使用 `gomobile bind` 生成 Android Archive (AAR) 和 Apple 框架。示例：

    - [Outline Android Archive](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L67-L81)

    - [Outline Apple 框架](https://github.com/Jigsaw-Code/outline-apps/blob/7058a89530a25a3de376a6ea2d4433a926787f50/client/go/Taskfile.yml#L83-L95)

3. **集成到应用中**：将生成的库添加到移动应用中。
