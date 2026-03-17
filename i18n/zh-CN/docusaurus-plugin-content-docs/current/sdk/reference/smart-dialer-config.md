---
title: "Smart Dialer 配置"
sidebar_label: "Smart Dialer 配置"
---

**Smart Dialer** 可针对特定的测试网域列表，搜索可绕过 DNS 和 TLS 封锁的策略。它需要用到包含多种策略的配置，以便从中选择一种策略。

## 适用于 Smart Dialer 的 YAML 配置 {#yaml_config_for_the_smart_dialer}

Smart Dialer 采用的是 YAML 格式的配置，示例如下：

```yaml
dns:
  - system: {}
  - https:
      name: 8.8.8.8
  - https:
      name: 9.9.9.9
tls:
  - ""
  - split:2
  - tlsfrag:1

fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

### DNS 配置 {#dns_configuration}

- `dns` 字段用于指定要测试的 DNS 解析器列表。

- DNS 解析器可以是以下类型之一：

    - `system`：使用系统解析器，通过空对象指定。

    - `https`：使用加密的 DNS-over-HTTPS (DoH) 解析器。

    - `tls`：使用加密的 DNS-over-TLS (DoT) 解析器。

    - `udp`：使用 UDP 解析器。

    - `tcp`：使用 TCP 解析器。

#### DNS-over-HTTPS 解析器 (DoH) {#dns-over-https_resolver_doh}

```yaml
https:
  name: dns.google
  address: 8.8.8.8
```

- `name`：DoH 服务器的域名。

- `address`：DoH 服务器的 host:port。默认为 `name`:443。

#### DNS-over-TLS 解析器 (DoT) {#dns-over-tls_resolver_dot}

```yaml
tls:
  name: dns.google
  address: 8.8.8.8
```

- `name`：DoT 服务器的域名。

- `address`：DoT 服务器的 host:port。默认为 `name`:853。

#### UDP 解析器 {#udp_resolver}

```yaml
udp:
  address: 8.8.8.8
```

- `address`：UDP 解析器的 host:port。

#### TCP 解析器 {#tcp_resolver}

```yaml
tcp:
  address: 8.8.8.8
```

- `address`：TCP 解析器的 host:port。

### TLS 配置 {#tls_configuration}

- `tls` 字段用于指定要测试的 TLS 传输列表。

- 每个 TLS 传输都以一个字符串表示，用于指定要使用的传输方式。

- 例如，`override:host=cloudflare.net|tlsfrag:1` 指定了使用 Cloudflare 域名前置和 TLS 分片进行传输。如需了解详情，请参阅[配置文档](https://pkg.go.dev/github.com/OutlineFoundation/outline-sdk/x/configurl#hdr-Config_Format)。

### 后备配置 {#fallback_configuration}

所有无代理策略均无法连接时，将使用后备配置。例如，该配置可指定备份代理服务器，用于尝试建立用户请求的连接。由于需要先等待其他 DNS/TLS 策略尝试失败/超时，才会使用后备配置，所以后备配置会增加启动延迟。

后备字符串应为：

- [`configurl`](https://pkg.go.dev/github.com/OutlineFoundation/outline-sdk/x/configurl#hdr-Proxy_Protocols) 中定义的有效 `StreamDialer` 配置字符串。

- 作为 `psiphon` 字段的子字段的有效 Psiphon 配置对象。

#### Shadowsocks 服务器示例 {#shadowsocks_server_example}

```yaml
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

#### SOCKS5 服务器示例 {#socks5_server_example}

```yaml
fallback:
  - socks5://[USERINFO]@[HOST]:[PORT]
```

#### Psiphon 配置示例 {#psiphon_config_example}

如需使用 [Psiphon](https://psiphon.ca/) 网络，您需要：

1. 与 Psiphon 团队联系，获取用于访问其网络的配置，可能需要签订合同。

2. 将获得的 Psiphon 配置添加到 Smart Dialer 配置的 `fallback` 部分。由于 JSON 与 YAML 兼容，您可以直接将 Psiphon 配置复制并粘贴到 `fallback` 部分，如下所示：

```yaml
fallback:
  - psiphon: {
      "PropagationChannelId": "FFFFFFFFFFFFFFFF",
      "SponsorId": "FFFFFFFFFFFFFFFF",
      "DisableLocalSocksProxy" : true,
      "DisableLocalHTTPProxy" : true,
      ...
    }
```


:::note
Psiphon 代码库基于 GPL 协议授予许可，可能会对您的代码施加许可限制。您可能需要考虑申请特殊许可。
:::

### 如何使用 Smart Dialer {#how_to_use_the_smart_dialer}

要使用 Smart Dialer，请创建一个 `StrategyFinder` 对象，然后调用 `NewDialer` 方法，以传入测试网域列表和 YAML 配置。`NewDialer` 方法将返回一个 `transport.StreamDialer`，可将其用于使用找到的策略创建连接。例如：

```go
finder := &smart.StrategyFinder{
    TestTimeout:  5 * time.Second,
    LogWriter:   os.Stdout,
    StreamDialer: &transport.TCPDialer{},
    PacketDialer: &transport.UDPDialer{},
}

configBytes := []byte(`
dns:
  - system: {}
  - https:
      name: 8.8.8.8
  - https:
      name: 9.9.9.9
tls:
  - ""
  - split:2
  - tlsfrag:1
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
`)

dialer, err := finder.NewDialer(
  context.Background(),
  []string{"www.google.com"},
  configBytes
)
if err != nil {
    // Handle error.
}

// Use dialer to create connections.
```

这是一个基本示例，可能需要根据具体应用场景进行调整。
