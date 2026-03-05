---
title: "Access Key Configuration Reference"
sidebar_label: "Access Key Config"
---

## 通道

### TunnelConfig

通道是 Outline 設定中的頂層物件，指定了 VPN 的設定方式。

**格式：**[ExplicitTunnelConfig](#explicittunnelconfig) |
[LegacyShadowsocksConfig](#legacyshadowsocksconfig) |
[LegacyShadowsocksURI](#legacyshadowsocksuri)

### ExplicitTunnelConfig

**格式：**struct**

**欄位：**

- `transport` ([TransportConfig](#transportconfig))：與目標目的地交換封包的傳輸方式

- `error` (struct**)：服務發生錯誤 (例如金鑰過期、配額用盡) 時，傳達給使用者的資訊

    - `message` (字串**)：對使用者顯示的簡單訊息

    - `details` (字串**)：使用者查看錯誤詳細資料時顯示的訊息，有助於排解問題

`error` 和 `transport` 欄位互斥。

成功示例：

```yaml
transport:
  $type: tcpudp
  tcp:
    ...  # Stream Dialer for TCP
  udp:
    ...  # Packet Listener for UDP
```

錯誤示例：

```yaml
error:
  message: Quota exceeded
  details: Used 100GB out of 100GB
```

## 傳輸

### TransportConfig

指定應如何與目標目的地交換封包。

**格式：**[Interface](#interface)

支援的 Interface 類型：

- `tcpudp`：[TCPUDPConfig](#tcpudpconfig)

### TCPUDPConfig

TCPUDPConfig 可分別設定 TCP 和 UDP 策略。

**格式：**struct**

**欄位：**

- `tcp` ([DialerConfig](#dialerconfig))：用於 TCP 連線的串流撥號器。

- `udp` ([PacketListenerConfig](#packetlistenerconfig))：用於 UDP 封包的封包監聽器。

將 TCP 和 UDP 傳送至不同端點的示例：

```yaml
tcp:
  $type: shadowsocks
  endpoint: ss.example.com:80
  <<: &cipher
    cipher: chacha20-ietf-poly1305
    secret: SECRET
  prefix: "POST "

udp:
  $type: shadowsocks
  endpoint: ss.example.com:53
  <<: *cipher
```

## 端點

「端點」會建立連往固定端點的連線，且可針對特定端點進行最佳化，所以比撥號器更為理想。分為串流端點和封包端點。

### EndpointConfig

**格式：**字串** | [Interface](#interface)

「字串」**端點是所選端點的 host:port 位址。連線是由預設撥號器建立。

串流端點和封包端點支援的 Interface 類型：

- `dial`：[DialEndpointConfig](#dialendpointconfig)

- `first-supported`：[FirstSupportedConfig](#firstsupportedconfig)

- `websocket`：[WebsocketEndpointConfig](#websocketendpointconfig)

- `shadowsocks`：[ShadowsocksConfig](#shadowsocksconfig)

### DialEndpointConfig

透過撥號至固定位址來建立連線。這個過程可以使用撥號器，將不同策略結合使用。

**格式：**struct**

**欄位：**

- `address` (字串**)：撥號目標端點位址

- `dialer` ([DialerConfig](#dialerconfig))：所用撥號器

### WebsocketEndpointConfig

運用 Websocket 建立將串流和封包傳送至端點的連線通道。

串流連線的每次寫入，以及封包連線的每個封包，都會轉換為一則 WebSocket 訊息。

**格式：**struct**

**欄位：**

- `url` (字串**)：WebSocket 端點網址。WebSocket 使用 TLS 時，網址格式須為 `https` 或 `wss`；若為明文 WebSocket，則須為 `http` 或 `ws`。

- `endpoint` ([EndpointConfig](#endpointconfig))：連線目標網路伺服器端點。若未指定，則會連線至網址中指定的位址。

## 撥號器

撥號器可依指定端點位址建立連線，分為串流撥號器和封包撥號器。

### DialerConfig

**格式：**空值** | [Interface](#interface)

撥號器為「空值」**(省略) 代表使用預設撥號器，即透過直接的 TCP 連線處理串流，透過直接的 UDP 連線處理封包。

串流撥號器和封包撥號器支援的 Interface 類型：

- `first-supported`：[FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`：[ShadowsocksConfig](#shadowsocksconfig)

## 封包監聽器

封包監聽器會建立不受限制的封包連線，能將封包傳送至多個目的地。

### PacketListenerConfig

**格式：**空值** | [Interface](#interface)

封包監聽器為「空值」**(省略) 代表使用預設封包監聽器，即 UDP 封包監聽器。

支援的 Interface 類型：

- `first-supported`：[FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`：[ShadowsocksPacketListenerConfig](#shadowsocksconfig)

## 策略

### Shadowsocks

#### LegacyShadowsocksConfig

LegacyShadowsocksConfig 代表使用 Shadowsocks 做為傳輸方式的通道，並採用舊版格式以確保回溯相容性。

**格式：**struct**

**欄位：**

- `server` (字串**)：連線目標主機

- `server_port` (數字**)：連線目標埠號

- `method` (字串**)：要使用的 [AEAD 加密演算法](https://shadowsocks.org/doc/aead.html#aead-ciphers)

- `password` (字串**)：用於產生加密金鑰

- `prefix` (字串**)：要使用的 [prefix 偽裝](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/)；適用於串流連線和封包連線。

示例：

```yaml
server: example.com
server_port: 4321
method: chacha20-ietf-poly1305
password: SECRET
prefix: "POST "
```

#### LegacyShadowsocksURI

LegacyShadowsocksURI 代表使用 Shadowsocks 做為傳輸方式的通道，並採用舊版網址格式以確保回溯相容性。

**格式：**字串**

請參閱「[舊版 Shadowsocks URI 格式](https://shadowsocks.org/doc/configs.html#uri-and-qr-code)」和「[SIP002 URI 配置](https://shadowsocks.org/doc/sip002.html)」。系統不支援外掛程式。

示例：

```yaml
ss://chacha20-ietf-poly1305:SECRET@example.com:443?prefix=POST%20
```

#### ShadowsocksConfig

ShadowsocksConfig 可代表串流撥號器或封包撥號器，以及使用 Shadowsocks 的封包監聽器。

**格式：**struct**

**欄位：**

- `endpoint` ([EndpointConfig](#endpointconfig))：連線目標 Shadowsocks 端點

- `cipher` (字串**)：要使用的 [AEAD 加密演算法](https://shadowsocks.org/doc/aead.html#aead-ciphers)

- `secret` (字串**)：用於產生加密金鑰

- `prefix` (字串**，選用)：要使用的 [prefix 偽裝](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/)；適用於串流連線和封包連線。

示例：

```yaml
endpoint: example.com:80
cipher: chacha20-ietf-poly1305
secret: SECRET
prefix: "POST "
```

## 中繼定義

### FirstSupportedConfig

使用應用程式支援的第一項設定。這可以在納入新設定時，確保與舊設定回溯相容。

**格式：**struct**

**欄位：**

- `options` ([EndpointConfig[]](#endpointconfig) |
[DialerConfig[]](#dialerconfig) |
[PacketListenerConfig[]](#packetlistenerconfig))：要考慮的選項清單

示例：

```yaml
options:
  - $type: websocket
    url: wss://example.com/SECRET_PATH
  - ss.example.com:4321
```

### Interface

Interface 支援從多種實作方式中擇一，並以 `$type` 欄位指定設定代表的類型。

示例：

```yaml
$type: shadowsocks
endpoint: example.com:4321
cipher: chacha20-ietf-poly1305
secret: SECRET
```
