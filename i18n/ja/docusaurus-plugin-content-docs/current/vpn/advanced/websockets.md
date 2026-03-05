---
title: "Disguise Connections as Web Traffic with Shadowsocks-over-WebSockets"
sidebar_label: "WebSockets"
---

*Outline クライアント v1.15.0 以降。*

このチュートリアルでは、Shadowsocks-over-WebSockets の実装に役立つ詳細を示します。Shadowsocks-over-WebSockets とは、通常の Shadowsocks 接続がブロックされる環境で検閲を回避する強力な手法のことです。Shadowsocks トラフィックを WebSockets にカプセル化すると、このトラフィックを標準のウェブトラフィックのように偽装して、トラフィックのレジリエンスとアクセシビリティを強化できます。

## ステップ 1: Outline サーバーを構成して実行する

新しい `config.yaml` ファイルを作成し、次の構成を含めます。

最新の [`outline-ss-server`](https://github.com/Jigsaw-Code/outline-ss-server/releases) をダウンロードし、作成した構成を使用して実行します。

## ステップ 2: ウェブサーバーを公開する

WebSocket ウェブサーバーを一般公開するには、インターネットに公開して、[TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security) を構成する必要があります。
このための方法はいくつかあります。[Caddy](https://caddyserver.com/)、[nginx](https://nginx.org/)、[Apache](https://httpd.apache.org/) などのローカル ウェブサーバーを使用して有効な TLS 証明書を保存したり、[Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) や [ngrok](https://ngrok.com/) などのトンネリング サーバーを導入したりできます。

### TryCloudflare を使用する例

この例では、[TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/) を使用して簡易トンネルを作成する方法を示します。この方法を使用すると、インバウンド ポートを開かなくても、ローカル ウェブサーバーを簡単に、かつ安全に公開することができます。

1. [`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) をダウンロードして、インストールします。

2. ローカル ウェブサーバー ポートを指すトンネルを作成します。

Cloudflare からサブドメイン（`acids-iceland-davidson-lb.trycloudflare.com` など）が提供され、WebSocket エンドポイントへのアクセスや、TLS の自動処理を実行できるようになります。このサブドメインは後で必要になるため、書き留めてください。

## ステップ 3: 動的アクセスキーを作成する

[アクセスキーの構成](../management/config)で示された形式を使用してユーザーのクライアント アクセスキー ファイル（YAML）を生成し、サーバー側で以前に構成した WebSocket エンドポイントを含めます。

動的アクセスキー ファイル（YAML）を生成したら、ユーザーに提供する必要があります。このファイルは静的なウェブ ホスティング サービスでホストすることも、動的に生成することもできます。[動的アクセスキー](../management/dynamic-access-keys)の使用方法を確認してください。

## ステップ 4: Outline クライアントで接続する

公式の [Outline クライアント](../../download-links) アプリケーション（バージョン 1.15.0 以降）のいずれかを使用して、新しく作成した動的アクセスキーをサーバー エントリとして追加します。[**Connect**] をクリックし、Shadowsocks-over-Websocket 構成を使用してサーバーへのトンネリングを開始します。

[IPInfo](https://ipinfo.io) などのツールを使用して、Outline サーバー経由でインターネットをブラウジングしていることを確認します。
