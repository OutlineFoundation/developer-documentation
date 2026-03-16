---
title: "動的アクセスキー"
sidebar_label: "動的アクセスキー"
---

Outline には、静的と動的の 2 種類のアクセスキーが用意されています。静的キーでは、キー自体にすべての接続情報がエンコードされますが、動的キーでは、接続情報の場所がエンコードされるため、この情報をリモートに保存し、必要に応じて変更できます。つまり、サーバーの構成を更新するたびに新しいキーを生成してユーザーに配布しなくても済みます。このドキュメントでは、動的アクセスキーを使用して Outline サーバーの配置を柔軟に、かつ効率的に行う方法を示します。

動的アクセスキーで使用されるアクセス情報は、次の 3 つの形式で指定できます。

### `ss://` リンクを使用する {#use_an_ss_link}

**Outline クライアント v1.8.1 以降。

既存の `ss://` リンクを直接使用できます。この方法は、サーバー、ポート、または暗号化方式を頻繁に変更する必要はないが、サーバー アドレスを柔軟に更新する必要がある場合に最適です。

**例:**

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

### JSON オブジェクトを使用する {#use_a_json_object}

**Outline クライアント v1.8.0 以降。

この方法では、ユーザーの Outline 接続のすべての面を柔軟に管理できます。サーバー、ポート、パスワード、暗号化方式をこの方法で更新できます。

**例:**

```json
{
  "server": "outline-server.example.com",
  "server_port": 8388,
  "password": "example",
  "method": "chacha20-ietf-poly1305"
}
```

- **server:** VPN サーバーのドメインまたは IP アドレス。

- **server_port:** VPN サーバーが実行されているポート番号。

- **password:** VPN との接続に必要なパスワード。

- **method:** VPN で使用される暗号化方式。Shadowsocks でサポートされる [AEAD 暗号方式](https://shadowsocks.org/doc/aead.html)をご覧ください。

### YAML オブジェクトを使用する {#use_a_yaml_object}

**Outline クライアント v1.15.0 以降。

この方法は、前述の JSON 方式と似ていますが、Outline の高度な構成形式を利用してさらに柔軟性が強化されています。サーバー、ポート、パスワード、暗号化方式などを更新できます。

**例:**

```yaml
transport:
  $type: tcpudp
  tcp:
    $type: shadowsocks
    endpoint: outline-server.example.com:8388
    cipher: chacha20-ietf-poly1305
    secret: example
  udp:
    $type: shadowsocks
    endpoint: outline-server.example.com:8388
    cipher: chacha20-ietf-poly1305
    secret: example
```

- **transport:** 使用するトランスポート プロトコルを定義します（この場合は TCP と UDP）。

- **tcp/udp:** 各プロトコルの構成を指定します。

    - **$type:** 構成のタイプを指定します（ここでは shadowsocks）。

    - **endpoint:** VPN サーバーのドメインまたは IP アドレスとポート。

    - **secret:** VPN との接続に必要なパスワード。

    - **cipher:** VPN で使用される暗号化方式。Shadowsocks でサポートされる [AEAD 暗号方式](https://shadowsocks.org/doc/aead.html)をご覧ください。

トランスポート、エンドポイント、ダイヤラー、パケット リスナーなど、Outline サーバーへのアクセスを構成できるすべての方法の詳細については、[アクセスキーの構成](config)をご覧ください。

## 静的キーからアクセス情報を抽出する {#extract_access_information_from_a_static_key}

既存の静的アクセスキーがある場合は、JSON または YAML ベースの動的アクセスキーを作成するのに必要な情報を抽出できます。静的アクセスキーは、次のパターンに従います。

```none
SS-URI = "ss://" userinfo "@" hostname ":" port [ "/" ] [ "#" tag ]
userinfo = websafe-base64-encode-utf8(method  ":" password)
           method ":" password
```

例:

```none
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl@outline-server.example.com:8388/?outline=1
```

- **サーバー:** `outline-server.example.com`

- **サーバー ポート:** `8388`

- **ユーザー情報:** `Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpleGFtcGxl`（[Google 管理者ツールボックスの Encode/Decode](https://toolbox.googleapps.com/apps/encode_decode/) などのツールを使用して [base64](https://en.wikipedia.org/wiki/Base64) としてデコードします）

    - **方式:** `chacha20-ietf-poly1305`

    - **パスワード:** `example`

## ホスティング プラットフォームを選択する {#choose_a_hosting_platform}

動的アクセスキーの作成方法について理解できたら、アクセスキーの構成に適したホスティング プラットフォームを選択することが重要になります。この決定を行う場合は、プラットフォームの信頼性、セキュリティ、使いやすさ、検閲耐性などの要因を考慮してください。プラットフォームでは、ダウンタイムなしでアクセスキー情報を安定した方法で処理できますか？構成を保護するのに適したセキュリティ対策は用意されていますか？プラットフォームでアクセスキーの情報を管理するのはどれくらい簡単ですか？インターネットの検閲が行われている地域からプラットフォームにアクセスできますか？

情報へのアクセスが制限されている可能性がある場合は、[Google ドライブ](https://drive.google.com)、[pad.riseup.net](https://pad.riseup.net/)、[Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html)（パススタイルのアクセス）、[Netlify](https://dev.to/alexmercedcoder/delivering-json-data-with-netlify-1j96)、[GitHub Secret Gist](https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists/creating-gists) など、検閲耐性のあるプラットフォームにホストすることを検討してください。デプロイに対する具体的なニーズを評価し、アクセシビリティとセキュリティの要件に合ったプラットフォームを選択します。
