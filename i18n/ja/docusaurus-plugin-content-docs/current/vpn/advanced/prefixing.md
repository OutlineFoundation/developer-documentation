---
title: "Disguise Connections with Prefixes"
sidebar_label: "Connection Prefixes"
---

Outline クライアント バージョン 1.9.0 以降では、アクセスキーで「プレフィックス」オプションがサポートされています。「プレフィックス」とは、Shadowsocks TCP 接続の[ソルト](https://shadowsocks.org/guide/aead.html)の最初のバイトとして使用されるバイトのリストです。これにより、接続を、ネットワークで許可されているプロトコルのように見せることができるため、認識されないプロトコルを拒否するファイアウォールを回避できます。

## 使用すべき状況

Outline デプロイメントのユーザーがまだブロックされていると思われる場合は、いくつかの異なるプレフィックスの試用を検討することをおすすめします。

## 手順

プレフィックスは 16 バイト以下にする必要があります。長いプレフィックスを使用すると、ソルトの競合が発生する可能性があります。その結果、暗号化の安全性が損なわれ、接続が検出される場合があります。ブロックを回避するには、できる限り短いプレフィックスを使用してください。

使用するポートは、プレフィックスが装うプロトコルと一致する必要があります。IANA には、プロトコルとポート番号をマップする[転送プロトコルのポート番号のレジストリ](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)があります。

以下に、一般的なプロトコルのように見える効果的なプレフィックスの例をいくつか示します。

推奨されるポート
JSON エンコード
URL エンコード

HTTP リクエスト
80（http）
`"POST "`
`POST%20`

HTTP レスポンス
80（http）
`"HTTP/1.1 "`
`HTTP%2F1.1%20`

DNS-over-TCP リクエスト
53（dns）
`"\u0005\u00DC\u005F\u00E0\u0001\u0020"`
`%05%C3%9C_%C3%A0%01%20`

TLS ClientHello
443（https）、463（smtps）、563（nntps）、636（ldaps）、989（ftps-data）、990（ftps）、993（imaps）、995（pop3s）、5223（Apple APN）、5228（Play ストア）、5349（turns）
`"\u0016\u0003\u0001\u0000\u00a8\u0001\u0001"`
`%16%03%01%00%C2%A8%01%01`

TLS Application Data
443（https）、463（smtps）、563（nntps）、636（ldaps）、989（ftps-data）、990（ftps）、993（imaps）、995（pop3s）、5223（Apple APN）、5228（Play ストア）、5349（turns）
`"\u0013\u0003\u0003\u003F"`
`%13%03%03%3F`

TLS ServerHello
443（https）、463（smtps）、563（nntps）、636（ldaps）、989（ftps-data）、990（ftps）、993（imaps）、995（pop3s）、5223（Apple APN）、5228（Play ストア）、5349（turns）
`"\u0016\u0003\u0003\u0040\u0000\u0002"`
`%16%03%03%40%00%02`

SSH
22（ssh）、830（netconf-ssh）、4334（netconf-ch-ssh）、5162（snmpssh-trap）
`"SSH-2.0\r\n"`
`SSH-2.0%0D%0A`

### 動的アクセスキー

[動的アクセスキー](../management/dynamic-access-keys)（`ssconf://`）でプレフィックス機能を使用するには、必要なプレフィックスを表す **JSON エンコード**値（上の表の例を参照）を使用して、「プレフィックス」キーを JSON オブジェクトに追加します。エスケープ コード（\u00FF など）を使用して、`U+0` から `U+FF` までの範囲で印刷できない Unicode コードポイントを表すことができます。次に例を示します。

### 静的アクセスキー

**静的アクセスキー**（ss://）でプレフィックスを使用するには、既存のキーを配布する前に変更する必要があります。Outline マネージャーによって生成された静的アクセスキーがある場合は、プレフィックスの **URL エンコード** バージョン（上の表の例を参照）を取得し、次のように、アクセスキーの末尾に追加します。

`ss://Z34nthataITHiTNIHTohithITHbVBqQ1o3bkk@127.0.0.1:33142/?outline=1&prefix=<your url-encoded prefix goes here>`

上級ユーザーの場合は、ブラウザの `encodeURIComponent()` 関数を使用して、**JSON エンコード**のプレフィックスを **URL エンコード**のプレフィックスに変換できます。これを行うには、ウェブ インスペクタ コンソール（Chrome の [デベロッパー ツール] > [コンソール]）を開き、以下を入力します。

Enter キーを押します。生成された値が、URL エンコード バージョンとなります。次に例を示します。
