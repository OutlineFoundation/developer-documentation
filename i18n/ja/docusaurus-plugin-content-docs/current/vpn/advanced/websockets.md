---
title: "Shadowsocks-over-WebSockets"
sidebar_label: "Shadowsocks-over-WebSockets"
---

*Outline クライアント v1.15.0 以降。*

このチュートリアルでは、Shadowsocks-over-WebSockets の実装に役立つ詳細を示します。Shadowsocks-over-WebSockets とは、通常の Shadowsocks 接続がブロックされる環境で検閲を回避する強力な手法のことです。Shadowsocks トラフィックを WebSockets にカプセル化すると、このトラフィックを標準のウェブトラフィックのように偽装して、トラフィックのレジリエンスとアクセシビリティを強化できます。


:::note
Shadowsocks-over-WebSockets がサポートされているのは、Outline クライアント v1.15.0 以降のみです。古いクライアント バージョンをサポートするには、既存の構成を維持する必要があります。
:::

## ステップ 1: Outline サーバーを構成して実行する {#step_1_configure_and_run_an_outline_server}

新しい `config.yaml` ファイルを作成し、次の構成を含めます。

```yaml
web:
  servers:
    - id: server1
        listen: 127.0.0.1:<WEB_SERVER_PORT>

services:
  - listeners:
      - type: websocket-stream
        web_server: server1
        path: /<TCP_PATH>
      - type: websocket-packet
        web_server: server1
        path: /<UDP_PATH>
    keys:
      - id: 1
        cipher: chacha20-ietf-poly1305
        secret: <SHADOWSOCKS_SECRET>
```

:::tip
プローブを回避するため、`path` をシークレットにしてください。これはシークレット エンドポイントとして機能します。長い、ランダムに生成されたパスの使用をおすすめします。
:::


最新の [`outline-ss-server`](https://github.com/OutlineFoundation/outline-ss-server/releases) をダウンロードし、作成した構成を使用して実行します。

```sh
outline-ss-server -config=config.yaml
```

## ステップ 2: ウェブサーバーを公開する {#step_2_expose_the_web_server}

WebSocket ウェブサーバーを一般公開するには、インターネットに公開して、[TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security) を構成する必要があります。
このための方法はいくつかあります。[Caddy](https://caddyserver.com/)、[nginx](https://nginx.org/)、[Apache](https://httpd.apache.org/) などのローカル ウェブサーバーを使用して有効な TLS 証明書を保存したり、[Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) や [ngrok](https://ngrok.com/) などのトンネリング サーバーを導入したりできます。

### TryCloudflare を使用する例 {#example_using_trycloudflare}


:::caution
TryCloudflare は、デモやテスト専用です。
:::

この例では、[TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/) を使用して簡易トンネルを作成する方法を示します。この方法を使用すると、インバウンド ポートを開かなくても、ローカル ウェブサーバーを簡単に、かつ安全に公開することができます。

1. [`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) をダウンロードして、インストールします。

2. ローカル ウェブサーバー ポートを指すトンネルを作成します。

```sh
cloudflared tunnel --url http://127.0.0.1:<WEB_SERVER_PORT>
```

Cloudflare からサブドメイン（`acids-iceland-davidson-lb.trycloudflare.com` など）が提供され、WebSocket エンドポイントへのアクセスや、TLS の自動処理を実行できるようになります。このサブドメインは後で必要になるため、書き留めてください。

## ステップ 3: 動的アクセスキーを作成する {#step_3_create_a_dynamic_access_key}

[アクセスキーの構成](../management/config)で示された形式を使用してユーザーのクライアント アクセスキー ファイル（YAML）を生成し、サーバー側で以前に構成した WebSocket エンドポイントを含めます。

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN>/<TCP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>

  udp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN>/<UDP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>
```

動的アクセスキー ファイル（YAML）を生成したら、ユーザーに提供する必要があります。このファイルは静的なウェブ ホスティング サービスでホストすることも、動的に生成することもできます。[動的アクセスキー](../management/dynamic-access-keys)の使用方法を確認してください。

## ステップ 4: Outline クライアントで接続する {#step_4_connect_with_the_outline_client}

公式の [Outline クライアント](../../download-links) アプリケーション（バージョン 1.15.0 以降）のいずれかを使用して、新しく作成した動的アクセスキーをサーバー エントリとして追加します。[**Connect**] をクリックし、Shadowsocks-over-Websocket 構成を使用してサーバーへのトンネリングを開始します。

[IPInfo](https://ipinfo.io) などのツールを使用して、Outline サーバー経由でインターネットをブラウジングしていることを確認します。
