---
title: "Configure Access Keys"
sidebar_label: "Configure Access Keys"
---

Outline は YAML ベースの構成を使用して VPN パラメータを定義し、TCP/UDP トラフィックを処理します。この構成では、複数のレベルのコンポーザビリティがサポートされるため、設定の柔軟性と拡張性が高まります。

最上位の構成は、[TunnelConfig](../reference/access-key-config#tunnelconfig) を指定します。

## 例

通常の Shadowsocks 構成は次のようになります。

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks
    endpoint: ss.example.com:80
    cipher: chacha20-ietf-poly1305
    secret: SECRET
    prefix: "POST "  # HTTP request

  udp:
    $type: shadowsocks
    endpoint: ss.example.com:53
    cipher: chacha20-ietf-poly1305
    secret: SECRET
    prefix: "\u0097\u00a7\u0001\u0000\u0000\u0001\u0000\u0000\u0000\u0000\u0000\u0000"  # DNS query
```

TCP と UDP にそれぞれ異なるプレフィックスを指定し、それぞれ異なるポートまたはエンドポインで実行できるようになりました。

YAML アンカーと `<<` マージキーを使用して、重複を回避できます。

```yaml
transport:
  $type: tcpudp

  tcp:
    <<: &shared
      $type: shadowsocks
      endpoint: ss.example.com:4321
      cipher: chacha20-ietf-poly1305
      secret: SECRET
    prefix: "POST "

  udp: *shared
```

戦略を構成し、マルチホップを実行できるようになりました。

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: dial
      address: exit.example.com:4321
      dialer:
        $type: shadowsocks
        address: entry.example.com:4321
        cipher: chacha20-ietf-poly1305
        secret: ENTRY_SECRET

    cipher: chacha20-ietf-poly1305
    secret: EXIT_SECRET

  udp: *shared
```

Shadowsocks などの「独自性の高い」プロトコルをブロックしている場合は、Shadowsocks-over-Websockets を使用できます。これのデプロイ方法については、[サーバーの構成例](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml)をご覧ください。クライアントの構成は次のようになります。

```yaml
transport:
  $type: tcpudp
  tcp:
    $type: shadowsocks
    endpoint:
        $type: websocket
        url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/tcp
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET

  udp:
    $type: shadowsocks
    endpoint:
        $type: websocket
        url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/udp
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET
```

Websocket エンドポイントは次にエンドポイントを取得し、これを利用して DNS ベースのブロックを回避できます。

```yaml
transport:
  $type: tcpudp
  tcp:
    $type: shadowsocks
    endpoint:
        $type: websocket
        url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/tcp
        endpoint: cloudflare.net:443
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET

  udp:
    $type: shadowsocks
    endpoint:
        $type: websocket
        url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/udp
        endpoint: cloudflare.net:443
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET
```

複数の Outline クライアント バージョンで互換性を確保するには、構成内で `first-supported` オプションを使用します。これは特に、新しい戦略と機能が Outline に追加されている場合に重要です。すべてのユーザーが最新のクライアント ソフトウェアに更新しているわけではないためです。`first-supported` を使用すると、さまざまなプラットフォームおよびクライアント バージョンでシームレスに動作する単一構成が可能になるため、下位互換性とユーザー エクスペリエンスの一貫性を確保できます。

```yaml
transport:
  $type: tcpudp
  tcp:
    $type: shadowsocks
    endpoint:
      $type: first-supported
      options:
        - $type: websocket
          url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/tcp
        - ss.example.com:4321
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET

  udp:
    $type: shadowsocks
    endpoint:
      $type: first-supported
      options:
        - $type: websocket
          url: wss://legendary-faster-packs-und.trycloudflare.com/SECRET_PATH/udp
        - ss.example.com:4321
    cipher: chacha20-ietf-poly1305
    secret: SS_SECRET
```
