---
title: "Access Key Configuration Reference"
sidebar_label: "Access Key Config"
---

## 隧道

### TunnelConfig

隧道是 Outline 配置中的顶级对象。它指定了 VPN 的配置方式。

**格式：**[ExplicitTunnelConfig](#explicittunnelconfig) | [LegacyShadowsocksConfig](#legacyshadowsocksconfig) | [LegacyShadowsocksURI](#legacyshadowsocksuri)

### ExplicitTunnelConfig

**格式：**结构体**

**字段：**

- `transport` ([TransportConfig](#transportconfig))：用于与目标目的地交换软件包的传输

- `error`（结构体**）：在发生服务错误（例如密钥已过期、配额已用尽）时向用户传达的信息

    - `message`（字符串**）：向用户显示的简单易懂的消息

    - `details`（字符串**）：用户打开错误详情时显示的消息，有助于排查问题。

`error` 和 `transport` 字段是互斥的。

成功示例：

错误示例：

## 传输

### TransportConfig

指定应如何与目标目的地交换数据包。

**格式：**[接口](#interface)

受支持的接口类型：

- `tcpudp`：[TCPUDPConfig](#tcpudpconfig)

### TCPUDPConfig

TCPUDPConfig 允许设置单独的 TCP 和 UDP 策略。

**格式：**结构体**

**字段：**

- `tcp` ([DialerConfig](#dialerconfig))：用于 TCP 连接的数据流拨号器。

- `udp` ([PacketListenerConfig](#packetlistenerconfig))：用于 UDP 数据包的数据包监听器。

向不同端点发送 TCP 和 UDP 的示例：

## 端点

端点会与固定端点建立连接。它比拨号器更合适，因为它支持对特定端点进行优化。端点分为数据流端点和数据包端点。

### EndpointConfig

**格式：**字符串** | [接口](#interface)

字符串**端点是所选端点的 host:port 地址。连接是使用默认拨号器建立的。

适用于数据流端点和数据包端点的受支持接口类型：

- `dial`：[DialEndpointConfig](#dialendpointconfig)

- `first-supported`：[FirstSupportedConfig](#firstsupportedconfig)

- `websocket`：[WebsocketEndpointConfig](#websocketendpointconfig)

- `shadowsocks`：[ShadowsocksConfig](#shadowsocksconfig)

### DialEndpointConfig

通过向固定地址拨号来建立连接。它可以采用拨号器，拨号器支持策略组合。

**格式：**结构体**

**字段：**

- `address`（字符串**）：要向其拨号的端点地址

- `dialer` ([DialerConfig](#dialerconfig))：用于向地址拨号的拨号器

### WebsocketEndpointConfig

通过 WebSocket 将隧道数据流连接和数据包连接传输到端点。

对于数据流连接，每次写入都会转换为 WebSocket 消息。对于数据包连接，每个数据包都会转换为 WebSocket 消息。

**格式：**结构体**

**字段：**

- `url`（字符串**）：WebSocket 端点的网址。对于基于 TLS 的 WebSocket，架构必须为 `https` 或 `wss`，对于明文 WebSocket，架构必须为 `http` 或 `ws`。

- `endpoint` ([EndpointConfig](#endpointconfig))：要连接到的 Web 服务器端点。如果不存在，则连接到网址中指定的地址。

## 拨号器

拨号器会根据端点地址建立连接，分为数据流拨号器和数据包拨号器。

### DialerConfig

**格式：**null** | [接口](#interface)

null**（不存在）拨号器是指默认拨号器，它会为数据流使用直接 TCP 连接，为数据包使用直接 UDP 连接。

适用于数据流拨号器和数据包拨号器的受支持接口类型：

- `first-supported`：[FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`：[ShadowsocksConfig](#shadowsocksconfig)

## 数据包监听器

数据包监听器会建立无界限的数据包连接，该连接可用于向多个目的地发送数据包。

### PacketListenerConfig

**格式：**null** | [接口](#interface)

null**（不存在）数据包监听器是指默认数据包监听器，即 UDP 数据包监听器。

受支持的接口类型：

- `first-supported`：[FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`：[ShadowsocksPacketListenerConfig](#shadowsocksconfig)

## 策略

### Shadowsocks

#### LegacyShadowsocksConfig

LegacyShadowsocksConfig 表示使用 Shadowsocks 传输数据的隧道。为了实现向后兼容性，它实现了旧版格式。

**格式：**结构体**

**字段：**

- `server`（字符串**）：要连接到的主机

- `server_port`（数字**）：要连接到的端口号

- `method`（字符串**）：要使用的 [AEAD 加密](https://shadowsocks.org/doc/aead.html#aead-ciphers)

- `password`（字符串**）：用于生成加密密钥

- `prefix`（字符串**）：要使用的[前缀伪装](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/)。支持数据流和数据包连接。

示例：

#### LegacyShadowsocksURI

LegacyShadowsocksURI 表示使用 Shadowsocks 传输数据的隧道。为了实现向后兼容性，它实现了旧版网址格式。

**格式：**字符串**

请参阅[旧版 Shadowsocks URI 格式](https://shadowsocks.org/doc/configs.html#uri-and-qr-code)和 [SIP002 URI scheme](https://shadowsocks.org/doc/sip002.html)。我们不支持插件。

示例：

#### ShadowsocksConfig

ShadowsocksConfig 可以表示数据流或数据包拨号器，以及使用 Shadowsocks 的数据包监听器。

**格式：**结构体**

**字段：**

- `endpoint` ([EndpointConfig](#endpointconfig))：要连接到的 Shadowsocks 端点

- `cipher`（字符串**）：要使用的 [AEAD 加密](https://shadowsocks.org/doc/aead.html#aead-ciphers)

- `secret`（字符串**）：用于生成加密密钥

- `prefix`（字符串**，可选）：要使用的[前缀伪装](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/)。支持数据流和数据包连接。

示例：

## 元定义

### FirstSupportedConfig

使用应用支持的第一个配置。这种方式可在纳入新配置的同时与旧配置向后兼容。

**格式：**结构体**

**字段：**

- `options` ([EndpointConfig[]](#endpointconfig) | [DialerConfig[]](#dialerconfig) | [PacketListenerConfig[]](#packetlistenerconfig))：要考虑的选项列表

示例：

### 接口

接口允许从多个实现中进行选择。它使用 `$type` 字段指定配置表示的类型。

示例：
