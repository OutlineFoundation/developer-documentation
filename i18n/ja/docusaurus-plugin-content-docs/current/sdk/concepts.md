---
title: "コンセプト"
sidebar_label: "コンセプト"
---

Outline SDK は基本的なコンセプトに基づいて構築されています。それらのコンセプトは、コンポジションや簡単な再利用を可能にするための相互運用可能なインターフェースとして定義されます。

## 接続 {#connections}

接続は、抽象的なトランスポート上の 2 つのエンドポイント間の通信を可能にします。接続には次の 2 種類があります。

- `transport.StreamConn`: TCP や `SOCK_STREAM` タイプの Posix ソケットなど、ストリーム ベースの接続。

- `transport.PacketConn`: UDP や `SOCK_DGRAM` タイプの Posix ソケットなど、データグラム ベースの接続。Go 標準ライブラリの慣習に従い、「データグラム」ではなく「パケット」という言葉を使用します。

接続をラップし、新しいトランスポート上でネストした接続を作成することもできます。たとえば、`StreamConn` には、TCP 上、TCP 上の TLS 上、TCP 上の TLS 上の HTTP 上、QUIC 上など、さまざまなオプションがあります。

## ダイヤラー {#dialers}

ダイヤラーは、基盤となるトランスポート プロトコルまたはプロキシ プロトコルをカプセル化しながら、host:port アドレスを指定した接続の作成を可能にします。指定したアドレスに対し、`StreamDialer` タイプは `StreamConn` 接続、`PacketDialer` タイプは `PacketConn` 接続を作成します。ダイヤラーもネスト化が可能です。たとえば TLS ストリーム ダイヤラーは、TCP ダイヤラーを使用して TCP 接続に基づく `StreamConn` を作成した後、TCP `StreamConn` に基づく TLS `StreamConn` を作成できます。SOCKS5-over-TLS ダイヤラーは、TLS ダイヤラーを使用してプロキシへの TLS `StreamConn` を作成した後、ターゲット アドレスへの SOCKS5 接続を実行できます。

## リゾルバ {#resolvers}

リゾルバ（`dns.Resolver`）は、基盤となるアルゴリズムまたはプロトコルをカプセル化しながら、DNS クエリへの回答を可能にします。リゾルバは主に、ドメイン名から IP アドレスへのマッピングに使用されます。
