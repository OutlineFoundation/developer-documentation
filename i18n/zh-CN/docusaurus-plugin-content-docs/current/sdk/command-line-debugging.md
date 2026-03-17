---
title: "使用 Outline SDK 远程表征和绕过网络干扰"
sidebar_label: "使用 Outline SDK 远程表征和绕过网络干扰"
---

本指南演示了如何使用 Outline SDK 的命令行工具从远程角度了解并规避网络干扰。您将学习如何使用 SDK 的工具来衡量网络干扰、测试规避策略并分析结果。本指南将重点介绍 `resolve`、`fetch` 和 `http2transport` 工具。

## Outline SDK 工具使用入门

您可以直接从命令行开始使用 Outline SDK 工具。

### 解析 DNS

借助 `resolve` 工具，您可以执行使用指定解析器的 DNS 查找。

如需解析网域的 A 记录，请执行以下操作：

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type A 1.2.3.4.nip.io
```

如需解析 CNAME 记录，请执行以下操作：

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type CNAME www.google.com
```

### 提取网页

`fetch` 工具可用于检索网页的内容。

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest https://example.com
```

它还可以强制连接使用 QUIC。

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -proto=h3 https://www.youtube.com
```

### 使用本地代理

`http2transport` 工具会创建一个本地代理来路由您的流量。如需启动使用 Shadowsocks 传输的本地代理，请执行以下操作：

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/http2transport@latest -localAddr 127.0.0.1:8080 -transport "ss://{your_shadowsocks_credentials}"
```

然后，您可以将此代理与其他工具（例如 curl）搭配使用：

```sh
curl -p -x http://127.0.0.1:8080 https://ipinfo.io
```

## 指定规避策略

Outline SDK 允许指定各种规避策略，这些策略可以组合使用，以绕过不同形式的网络干扰。这些策略的规范位于 [Go 文档](https://pkg.go.dev/golang.getoutline.org/sdk/x/configurl)中。

### 可组合策略

您可以将这些策略结合起来，以创建更强大的规避技术。

* **DNS-over-HTTPS with TLS Fragmentation**：`doh:name=cloudflare-dns.com&address=cloudflare.net:443 | tlsfrag:1`

* **通过 TLS 进行 SOCKS5 传输并进行域名伪装**：`tls:sni=decoy.example.com&certname=[HOST] | socks5:[HOST]:[PORT]`

* **使用 Shadowsocks 进行多跳路由**：`ss://[USERINFO1]@[HOST1]:[PORT1] | ss://[USERINFO2]@[HOST2]:[PORT2] | ss://[USERINFO3]@[HOST3]:[PORT3]`

## 远程访问和衡量

如需衡量不同区域的网络干扰情况，您可以使用远程代理。您可以查找或创建要连接的远程代理。

### 远程访问选项

借助 `fetch` 工具，您可以通过多种方式远程测试连接。

#### Outline 服务器

通过 Shadowsocks 传输远程连接到标准 Outline 服务器。

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "ss://{remote_shadowsocks_credentials}" https://ipinfo.io | jq
```

#### 通过 SSH 使用 SOCKS5

使用 SSH 隧道创建 SOCKS5 代理。

```sh
ssh -D 127.0.0.1:1080 -C -N $USER@$HOST:$PORT
```

使用 fetch 连接到该隧道

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "socks5://localhost:1080" https://ipinfo.io | jq
```

## 案例研究：绕过伊朗的 YouTube 封锁

下面是一个检测和绕过网络干扰的实际示例。

### 检测屏蔽

当尝试通过伊朗代理获取 YouTube 首页时，请求超时，表明存在屏蔽。

```sh
export TRANSPORT="ss://{remote_shadowsocks_credentials}"
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)" https://www.youtube.com
```

此命令因超时而失败。

### 通过 TLS 分段绕过

通过向传输层添加 TLS 分段，我们可以绕过此限制。

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)|tlsfrag:1" https://www.youtube.com | grep -oe '<title>.*</title>'
```

此命令成功检索到 YouTube 首页的标题，即 `<title>YouTube</title>`。

### 通过 TLS 分段和 DNS-over-HTTPS 进行绕过

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|tlsfrag:1|doh:name=cloudflare-dns.com&address=www.cloudflare.net" https://www.youtube.com | grep -oe '<title>.*</title>'
```

此调用也会成功返回 `<title>YouTube</title>`。

### 通过 Outline 服务器绕过

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|ss://<your_shadowsocks_credentials>" https://www.youtube.com | grep -oe '<title>.*</title>'
```

此操作也会返回 `<title>YouTube</title>`。

## 进一步分析和资源

如需参与讨论和提问，请访问 [Outline SDK 讨论组](https://github.com/OutlineFoundation/outline-sdk/discussions)。
