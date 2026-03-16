---
title: "Deploy with Automatic HTTPS Using Caddy"
sidebar_label: "HTTPS with Caddy"
---

このガイドでは、強力でユーザー フレンドリーなウェブサーバーである [Caddy](https://caddyserver.com/) を使用して、Outline サーバーのセットアップを強化する方法を示します。Caddy には[自動 HTTPS](https://caddyserver.com/docs/automatic-https) 機能があり、柔軟性の高い構成を備えているため、Outline サーバーの機能を拡張し強化する手段として最適であり、特に WebSocket トランスポートを使用する場合におすすめです。

## Caddy とは何ですか？ {#what_is_caddy}

Caddy は、使いやすさ、自動 HTTPS、さまざまなプロトコルのサポートという特長を持つオープンソース ウェブサーバーです。ウェブサーバーの構成を簡素化し、次のような機能を提供します。

- **自動 HTTPS:** Caddy は TLS 証明書を自動的に取得し、更新して、安全な接続を維持します。

- **HTTP/3 のサポート:** Caddy は最新の HTTP/3 プロトコルをサポートしており、ウェブ トラフィックの処理の高速化と効率化を図ることができます。

- **プラグインで拡張可能:** Caddy をプラグインで拡張し、リバース プロキシやロード バランシングなどのさまざまな機能をサポートできます。

## ステップ 1: 前提条件 {#step_1_prerequisites}

- [`xcaddy`](https://github.com/caddyserver/xcaddy) をダウンロードして、インストールします。

## ステップ 2: ドメインを構成する {#step_2_configure_your_domain}

Caddy を開始する前に、サーバーの IP アドレスを指すようにドメイン名が正しく構成されていることを確認します。

- **A/AAAA レコードの設定:** DNS プロバイダにログインし、サーバーの IPv4 アドレスと IPv6 アドレスをそれぞれ指すようにドメインの A レコードと AAAA レコードを設定します。

- **DNS レコードの確認:** 正式な DNS レコードをルックアップし、レコードが正しく設定されていることを確認します。

```sh
curl "https://cloudflare-dns.com/dns-query?name=<DOMAIN_NAME>&type=A" \
  -H "accept: application/dns-json"
```

## ステップ 3: Caddy のカスタムビルドを構築して実行する {#build-and-run}

`xcaddy` を使用して、Outline コアサーバー モジュールと必要な他のサーバー拡張機能モジュールを含む `caddy` のカスタム バイナリを構築できます。

```sh
xcaddy build \
  # The example uses a YAML config, so include a YAML config adapter module.
  --with github.com/iamd3vil/caddy_yaml_adapter \
  # The Outline core server module.
  --with github.com/OutlineFoundation/outline-ss-server/outlinecaddy
```

## ステップ 4: Outline で Caddy サーバーを構成して実行する {#step_4_configure_and_run_the_caddy_server_with_outline}

新しい `config.yaml` ファイルを作成し、次の構成を含めます。

```yaml
apps:
  http:
    servers:
      server1:
        listen:
          - ":443"
        routes:
          - match:
            - host:
              - <DOMAIN_NAME>
            - path:
              - /<TCP_PATH>
            handle:
            - handler: websocket2layer4
              type: stream
              connection_handler: ss1
          - match:
            - host:
              - <DOMAIN_NAME>
            - path:
              - /<UDP_PATH>
            handle:
              - handler: websocket2layer4
                type: packet
                connection_handler: ss1
  outline:
    shadowsocks:
      replay_history: 10000
    connection_handlers:
      - name: ss1
        handle:
          handler: shadowsocks
          keys:
            - id: user-1
              cipher: chacha20-ietf-poly1305
              secret: <SHADOWSOCKS_SECRET>
```

この構成は Shadowsocks-over-WebSockets 方式で、ウェブサーバーが `443` ポートでリッスンし、Shadowsocks でラップした TCP および UDP トラフィックをそれぞれ `TCP_PATH` パスと `UDP_PATH` パスで受け入れることを意味します。

作成した構成を使用して Outline とその拡張を含む Caddy サーバーを実行します。

```sh
caddy run --config config.yaml --adapter yaml --watch
```

他の構成例については、[outline-ss-server/outlinecaddy GitHub
repo](https://github.com/OutlineFoundation/outline-ss-server/tree/master/outlinecaddy/examples) をご覧ください。

## ステップ 5: 動的アクセスキーを作成する {#step_5_create_a_dynamic_access_key}

[高度な構成](../management/config)の形式を使用してユーザーのクライアント アクセスキー ファイル（YAML）を生成し、サーバー側で以前に構成した WebSocket エンドポイントを含めます。

```yaml
transport:
  $type: tcpudp

  tcp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN_NAME>/<TCP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>

  udp:
    $type: shadowsocks

    endpoint:
      $type: websocket
      url: wss://<DOMAIN_NAME>/<UDP_PATH>
    cipher: chacha20-ietf-poly1305
    secret: <SHADOWSOCKS_SECRET>
```

動的アクセスキー ファイル（YAML）を生成したら、ユーザーに提供する必要があります。このファイルは静的なウェブ ホスティング サービスでホストすることも、動的に生成することもできます。[動的アクセスキー](../management/dynamic-access-keys)の使用方法を確認してください

## ステップ 6: Outline クライアントで接続する {#step_6_connect_with_the_outline_client}

公式の [Outline クライアント](../../download-links) アプリケーション（バージョン 1.15.0 以降）のいずれかを使用し、新しく作成した動的アクセスキーをサーバー エントリとして追加します。[**接続**] をクリックし、Shadowsocks-over-Websocket 構成を使用してサーバーへのトンネリングを開始します。

[IPInfo](https://ipinfo.io) などのツールを使用して、Outline サーバー経由でインターネットをブラウジングしていることを確認します。
