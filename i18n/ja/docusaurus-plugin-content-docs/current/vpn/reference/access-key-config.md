---
title: "Access Key Configuration Reference"
sidebar_label: "Access Key Config"
---

## トンネル

### TunnelConfig

トンネルは Outline 構成の最上位のオブジェクトです。VPN の構成方法を指定します。

**形式:** [ExplicitTunnelConfig](#explicittunnelconfig) |
[LegacyShadowsocksConfig](#legacyshadowsocksconfig) |
[LegacyShadowsocksURI](#legacyshadowsocksuri)

### ExplicitTunnelConfig

**形式:** *struct*

**フィールド:**

- `transport` ([TransportConfig](#transportconfig)): 宛先とパッケージを交換する際に使用するトランスポート

- `error` (*struct*): サービス エラー（キーの期限切れ、割り当ての枯渇など）が発生した場合にユーザーに伝える情報

    - `message` (*string*): ユーザーに表示するユーザー フレンドリーなメッセージ

    - `details` (*string*): ユーザーがエラーの詳細を開いたときに表示するメッセージ。トラブルシューティングに役立ちます。

`error` フィールドと `transport` フィールドは相互に排他的です。

成功の例:

```yaml
transport:
  $type: tcpudp
  tcp:
    ...  # Stream Dialer for TCP
  udp:
    ...  # Packet Listener for UDP
```

エラーの例:

```yaml
error:
  message: Quota exceeded
  details: Used 100GB out of 100GB
```

## トランスポート

### TransportConfig

宛先とパケットを交換する方法を指定します。

**形式:** [Interface](#interface)

サポートされているインターフェース タイプ:

- `tcpudp`: [TCPUDPConfig](#tcpudpconfig)

### TCPUDPConfig

TCPUDPConfig では、TCP と UDP の扱い方を個別に設定できます。

**形式:** *struct*

**フィールド:**

- `tcp` ([DialerConfig](#dialerconfig)): TCP 接続に使用するストリーム ダイヤラー。

- `udp` ([PacketListenerConfig](#packetlistenerconfig)): UDP パケットに使用するパケット リスナー。

TCP と UDP を異なるエンドポイントに送信する例:

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

## エンドポイント

エンドポイントは固定エンドポイントとの接続を確立します。エンドポイントごとの最適化が可能であるため、ダイヤラーよりも推奨されています。ストリーム エンドポイントとパケット エンドポイントがあります。

### EndpointConfig

**形式:** *string* | [Interface](#interface)

*string* エンドポイントは、選択したエンドポイントの host:port 形式のアドレスです。接続はデフォルトのダイヤラーを使用して確立されます。

ストリーム エンドポイントとパケット エンドポイントでサポートされているインターフェース タイプ:

- `dial`: [DialEndpointConfig](#dialendpointconfig)

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `websocket`: [WebsocketEndpointConfig](#websocketendpointconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

### DialEndpointConfig

固定アドレスにダイヤルして接続を確立します。ダイヤラーを指定して、接続設定を構成することができます。

**形式:** *struct*

**フィールド:**

- `address` (*string*): ダイヤルするエンドポイント アドレス

- `dialer` ([DialerConfig](#dialerconfig)): アドレスにダイヤルする際に使用するダイヤラー

### WebsocketEndpointConfig

ストリーム接続とパケット接続を Websockets 経由でエンドポイントにトンネリングします。

ストリーム接続の場合、個々の書き込みが Websocket メッセージに変換されます。パケット接続の場合、各パケットが Websocket メッセージに変換されます。

**形式:** *struct*

**フィールド:**

- `url` (*string*): Websocket エンドポイントの URL。このスキーマは、Websocket over TLS の場合は `https` または `wss`、平文の Websocket 通信の場合は `http` または `ws` にする必要があります。

- `endpoint` ([EndpointConfig](#endpointconfig)): 接続先のウェブサーバー エンドポイント。指定しなかった場合は、URL で指定したアドレスに接続されます。

## ダイヤラー

ダイヤラーは、エンドポイント アドレスが指定された場合に接続を確立します。ストリーム ダイヤラーとパケット ダイヤラーがあります。

### DialerConfig

**形式:** *null* | [Interface](#interface)

*null* を指定すると（指定を省略すると）デフォルトのダイヤラーになり、ストリーム ダイヤラーの場合は直接の TCP 接続、パケット ダイヤラーの場合は直接の UDP 接続を使用します。

ストリーム ダイヤラーとパケット ダイヤラーでサポートされているインターフェース タイプ:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksConfig](#shadowsocksconfig)

## パケット リスナー

パケット リスナーは、複数の宛先にパケットを送信する際に使用できる、制限なしのパケット接続を確立します。

### PacketListenerConfig

**形式:** *null* | [Interface](#interface)

*null* を指定すると（指定を省略すると）、デフォルトのパケット リスナー（UDP パケット リスナー）になります。

サポートされているインターフェース タイプ:

- `first-supported`: [FirstSupportedConfig](#firstsupportedconfig)

- `shadowsocks`: [ShadowsocksPacketListenerConfig](#shadowsocksconfig)

## 接続方法

### Shadowsocks

#### LegacyShadowsocksConfig

LegacyShadowsocksConfig は、トランスポートとして Shadowsocks を使用するトンネルを表します。下位互換性のために以前の形式を実装しています。

**形式:** *struct*

**フィールド:**

- `server` (*string*): 接続先のホスト

- `server_port` (*number*): 接続先のポート番号

- `method` (*string*): 使用する [AEAD 暗号](https://shadowsocks.org/doc/aead.html#aead-ciphers)

- `password` (*string*): 暗号鍵の生成に使用

- `prefix` (*string*): 使用する[プレフィックスの偽装](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/)。ストリーム接続とパケット接続でサポートされます。

例:

```yaml
server: example.com
server_port: 4321
method: chacha20-ietf-poly1305
password: SECRET
prefix: "POST "
```

#### LegacyShadowsocksURI

LegacyShadowsocksURI は、トランスポートとして Shadowsocks を使用するトンネルを表します。下位互換性のために以前の URL 形式を実装しています。

**形式:** *string*

[以前の Shadowsocks URI 形式](https://shadowsocks.org/doc/configs.html#uri-and-qr-code)および [SIP002 URI スキーム](https://shadowsocks.org/doc/sip002.html)をご覧ください。プラグインはサポートされていません。

例:

```yaml
ss://chacha20-ietf-poly1305:SECRET@example.com:443?prefix=POST%20
```

#### ShadowsocksConfig

ShadowsocksConfig は、ストリーム または パケット ダイヤラーのほかに、Shadowsocks を使用するパケット リスナーを表すこともできます。

**形式:** *struct*

**フィールド:**

- `endpoint` ([EndpointConfig](#endpointconfig)): 接続先の Shadowsocks エンドポイント

- `cipher` (*string*): 使用する [AEAD 暗号](https://shadowsocks.org/doc/aead.html#aead-ciphers)

- `secret` (*string*): 暗号鍵の生成に使用

- `prefix` (*string*、省略可): 使用する[プレフィックスの偽装](https://www.reddit.com/r/outlinevpn/wiki/index/prefixing/)。ストリーム接続とパケット接続でサポートされます。

例:

```yaml
endpoint: example.com:80
cipher: chacha20-ietf-poly1305
secret: SECRET
prefix: "POST "
```

## メタ定義

### FirstSupportedConfig

アプリケーションでサポートされている最初の構成を使用します。これは、古い構成との下位互換性を維持しながら新しい構成を組み込む方法です。

**形式:** *struct*

**フィールド:**

- `options` ([EndpointConfig[]](#endpointconfig) |
[DialerConfig[]](#dialerconfig) |
[PacketListenerConfig[]](#packetlistenerconfig)): 検討するオプションのリスト

例:

```yaml
options:
  - $type: websocket
    url: wss://example.com/SECRET_PATH
  - ss.example.com:4321
```

### Interface

インターフェースを使用すると、複数の実装の中から 1 つを選択できます。`$type` フィールドを使用して構成が表すタイプを指定します。

例:

```yaml
$type: shadowsocks
endpoint: example.com:4321
cipher: chacha20-ietf-poly1305
secret: SECRET
```
