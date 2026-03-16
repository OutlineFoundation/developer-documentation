---
title: "Command Line Debugging"
sidebar_label: "Command Line Debugging"
---

このガイドでは、Outline SDK のコマンドライン ツールを使用して、リモートの視点からネットワーク干渉を把握し、回避する方法について説明します。このコースでは、SDK のツールを使用してネットワーク干渉を測定し、回避策をテストして、結果を分析する方法を学びます。このガイドでは、`resolve`、`fetch`、`http2transport` ツールに焦点を当てます。

## Outline SDK ツールの使用を開始する

Outline SDK ツールは、コマンドラインから直接使用できます。

### DNS を解決する

`resolve` ツールを使用すると、指定したリゾルバで DNS ルックアップを実行できます。

ドメインの A レコードを解決するには:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type A 1.2.3.4.nip.io
```

CNAME レコードを解決するには:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type CNAME www.google.com
```

### ウェブページを取得する

`fetch` ツールを使用して、ウェブページの内容を取得できます。

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest https://example.com
```

接続で QUIC を強制的に使用することもできます。

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -proto=h3 https://www.youtube.com
```

### ローカル プロキシを使用する

`http2transport` ツールは、トラフィックをルーティングするためのローカル プロキシを作成します。Shadowsocks トランスポートを使用してローカル プロキシを起動するには:

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/http2transport@latest -localAddr 127.0.0.1:8080 -transport "ss://{your_shadowsocks_credentials}"
```

このプロキシは、curl などの他のツールで使用できます。

```sh
curl -p -x http://127.0.0.1:8080 https://ipinfo.io
```

## 回避戦略を指定する

Outline SDK では、さまざまな回避戦略を指定できます。これらの戦略を組み合わせて、さまざまな形式のネットワーク干渉を回避できます。これらの戦略の仕様については、[Go のドキュメント](https://pkg.go.dev/github.com/OutlineFoundation/outline-sdk/x@v0.0.3/configurl)をご覧ください。

### コンポーザブル戦略

これらの戦略を組み合わせることで、より堅牢な回避手法を作成できます。

* **TLS フラグメンテーションを使用した DNS-over-HTTPS**: `doh:name=cloudflare-dns.com&address=cloudflare.net:443 | tlsfrag:1`

* **ドメイン フロント サービスを使用した TLS 経由の SOCKS5**: `tls:sni=decoy.example.com&certname=[HOST] | socks5:[HOST]:[PORT]`

* **Shadowsocks を使用したマルチホップ ルーティング**: `ss://[USERINFO1]@[HOST1]:[PORT1] | ss://[USERINFO2]@[HOST2]:[PORT2] | ss://[USERINFO3]@[HOST3]:[PORT3]`

## リモート アクセスと測定

さまざまな地域で発生するネットワーク干渉を測定するには、リモート プロキシを使用します。接続するリモート プロキシを見つけるか、作成できます。

### リモート アクセス オプション

`fetch` ツールを使用すると、さまざまな方法で接続をリモートでテストできます。

#### Outline サーバー

Shadowsocks トランスポートを使用して、標準の Outline サーバーにリモートで接続します。

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "ss://{remote_shadowsocks_credentials}" https://ipinfo.io | jq
```

#### SSH 経由の SOCKS5

SSH トンネルを使用して SOCKS5 プロキシを作成します。

```sh
ssh -D 127.0.0.1:1080 -C -N $USER@$HOST:$PORT
```

fetch を使用してそのトンネルに接続する

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "socks5://localhost:1080" https://ipinfo.io | jq
```

## 事例紹介: イランでの YouTube のブロックを回避する

ネットワーク干渉を検出してバイパスする実用的な例を次に示します。

### ブロックを検出する

イランのプロキシ経由で YouTube のホームページを取得しようとすると、リクエストがタイムアウトし、ブロックされていることがわかります。

```sh
export TRANSPORT="ss://{remote_shadowsocks_credentials}"
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)" https://www.youtube.com
```

このコマンドはタイムアウトで失敗します。

### TLS フラグメンテーションによるバイパス

TLS フラグメンテーションをトランスポートに追加することで、このブロックを回避できます。

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)|tlsfrag:1" https://www.youtube.com | grep -oe '<title>.*</title>'
```

このコマンドは、YouTube のホームページのタイトル（`<title>YouTube</title>`）を正常に取得します。

### TLS フラグメンテーションと DNS-over-HTTPS によるバイパス

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|tlsfrag:1|doh:name=cloudflare-dns.com&address=www.cloudflare.net" https://www.youtube.com | grep -oe '<title>.*</title>'
```

この場合も `<title>YouTube</title>` が正常に返されます。

### Outline サーバーでバイパスする

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|ss://<your_shadowsocks_credentials>" https://www.youtube.com | grep -oe '<title>.*</title>'
```

これも `<title>YouTube</title>` を返します。

## 詳細な分析とリソース

ディスカッションや質問については、[Outline SDK ディスカッション グループ](https://github.com/OutlineFoundation/outline-sdk/discussions)をご覧ください。
