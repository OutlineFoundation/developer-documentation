---
title: "Smart Dialer Configuration"
sidebar_label: "Smart Dialer Config"
---

**Smart Dialer** は、指定されたテストドメインのリストに対して、DSN と TLS のブロックを回避する戦略を探索します。選択対象となる複数の戦略を記述した構成が必要です。

## Smart Dialer 用の YAML 構成 {#yaml_config_for_the_smart_dialer}

Smart Dialer が使用する構成は YAML 形式です。次に例を示します。

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

### DNS の構成 {#dns_configuration}

- `dns` フィールドでは、テストする DNS リゾルバのリストを指定します。

- 各 DNS リゾルバは、以下のいずれかのタイプです。

    - `system`: システム リゾルバを使用します。空のオブジェクトを指定します。

    - `https`: 暗号化された DNS over HTTPS（DoH）リゾルバを使用します。

    - `tls`: 暗号化された DNS over TLS（DoT）リゾルバを使用します。

    - `udp`: UDP リゾルバを使用します。

    - `tcp`: TCP リゾルバを使用します。

#### DNS-over-HTTPS リゾルバ（DoH） {#dns-over-https_resolver_doh}

```yaml
https:
  name: dns.google
  address: 8.8.8.8
```

- `name`: DoH サーバーのドメイン名。

- `address`: DoH サーバーの host:port。デフォルトは `name`:443 です。

#### DNS-over-TLS リゾルバ（DoT） {#dns-over-tls_resolver_dot}

```yaml
tls:
  name: dns.google
  address: 8.8.8.8
```

- `name`: DoT サーバーのドメイン名。

- `address`: DoT サーバーの host:port。デフォルトは `name`:853 です。

#### UDP リゾルバ {#udp_resolver}

```yaml
udp:
  address: 8.8.8.8
```

- `address`: UDP リゾルバの host:port。

#### TCP リゾルバ {#tcp_resolver}

```yaml
tcp:
  address: 8.8.8.8
```

- `address`: TCP リゾルバの host:port。

### TLS の構成 {#tls_configuration}

- `tls` フィールドでは、テストする TLS トランスポートのリストを指定します。

- 各 TLS トランスポートは、使用するトランスポートを指定する文字列です。

- たとえば、`override:host=cloudflare.net|tlsfrag:1` は、Cloudflare のドメイン フロンティングと TLS フラグメンテーションを使用するトランスポートを指定します。詳しくは、[構成に関するドキュメント](https://pkg.go.dev/github.com/OutlineFoundation/outline-sdk/x/configurl#hdr-Config_Format)をご覧ください。

### フォールバックの構成 {#fallback_configuration}

フォールバックの構成は、どのプロキシレス戦略でも接続できない場合に使用されます。たとえば、バックアップ プロキシ サーバーを指定してユーザーの接続を試みます。フォールバックは他の DNS/TLS 戦略が失敗またはタイムアウトした場合のみ使用されるため、その開始は後回しになります。

フォールバック文字列は次のように指定します。

- [`configurl`](https://pkg.go.dev/github.com/OutlineFoundation/outline-sdk/x/configurl#hdr-Proxy_Protocols) で定義されている有効な `StreamDialer` 構成文字列。

- `psiphon` フィールドの子としての有効な Psiphon 構成オブジェクト。

#### Shadowsocks サーバーの例 {#shadowsocks_server_example}

```yaml
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

#### SOCKS5 サーバーの例 {#socks5_server_example}

```yaml
fallback:
  - socks5://[USERINFO]@[HOST]:[PORT]
```

#### Psiphon の構成の例 {#psiphon_config_example}

[Psiphon](https://psiphon.ca/) ネットワークを使用するには、以下を行う必要があります。

1. Psiphon チームに問い合わせて、Psiphon のネットワークにアクセスするための構成を入手します。これには、契約が必要になる場合があります。

2. 入手した Psiphon の構成を Smart Dialer の構成の `fallback` セクションに追加します。JSON は YAML と互換性を持つため、以下のように `fallback` セクションに Psiphon の構成をそのままコピーして貼り付けることができます。

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

### Smart Dialer の使用方法 {#how_to_use_the_smart_dialer}

Smart Dialer を使用するには、`StrategyFinder` オブジェクトを作成し、`NewDialer` メソッドを呼び出してテストドメインのリストと YAML の構成を引数として渡します。`NewDialer` メソッドは、見つけた戦略を使用して接続を作成するための `transport.StreamDialer` を返します。次に例を示します。

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

これは基本的な例であり、具体的なユースケースに応じて変更が必要になる場合があります。
