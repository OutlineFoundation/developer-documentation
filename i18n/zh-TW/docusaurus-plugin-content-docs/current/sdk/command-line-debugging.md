---
title: "使用 Outline SDK 遠端分析及規避網路干擾"
sidebar_label: "使用 Outline SDK 遠端分析及規避網路干擾"
---

本指南說明如何使用 Outline SDK 的指令列工具，從遠端瞭解並規避網路干擾。您將瞭解如何使用 SDK 的工具評估網路干擾、測試規避策略，以及分析結果。本指南將著重於 `resolve`、`fetch` 和 `http2transport` 工具。

## 開始使用 Outline SDK 工具

您可以直接從指令列開始使用 Outline SDK 工具。

### 解析 DNS

`resolve` 工具可讓您使用指定的解析器執行 DNS 查詢。

如要解析網域的 A 記錄：

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type A 1.2.3.4.nip.io
```

如要解析 CNAME 記錄，請按照下列步驟操作：

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/resolve@latest -resolver 8.8.8.8 -type CNAME www.google.com
```

### 擷取網頁

`fetch` 工具可用來擷取網頁內容。

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest https://example.com
```

也可以強制連線使用 QUIC。

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -proto=h3 https://www.youtube.com
```

### 使用本機 Proxy

`http2transport` 工具會建立本機 Proxy，以便透過該 Proxy 傳送流量。如要使用 Shadowsocks 傳輸方式啟動本機 Proxy，請執行下列操作：

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/http2transport@latest -localAddr 127.0.0.1:8080 -transport "ss://{your_shadowsocks_credentials}"
```

接著，您就能搭配 curl 等其他工具使用這個 Proxy：

```sh
curl -p -x http://127.0.0.1:8080 https://ipinfo.io
```

## 指定規避策略

Outline SDK 可指定各種規避策略，並加以組合，藉此規避不同形式的網路干擾。這些策略的規格位於 [Go 說明文件](https://pkg.go.dev/github.com/OutlineFoundation/outline-sdk/x@v0.0.3/configurl)中。

### 可組合策略

這些策略可以合併使用，打造更強大的規避技術。

* **DNS-over-HTTPS with TLS Fragmentation**：`doh:name=cloudflare-dns.com&address=cloudflare.net:443 | tlsfrag:1`

* **透過網域前端技術的 SOCKS5-over-TLS**：`tls:sni=decoy.example.com&certname=[HOST] | socks5:[HOST]:[PORT]`

* **透過 Shadowsocks 進行多躍點路由**：`ss://[USERINFO1]@[HOST1]:[PORT1] | ss://[USERINFO2]@[HOST2]:[PORT2] | ss://[USERINFO3]@[HOST3]:[PORT3]`

## 遠端存取和測量

如要測量不同地區的網路干擾情況，可以使用遠端 Proxy。您可以尋找或建立遠端 Proxy 來連線。

### 遠端存取選項

使用 `fetch` 工具，即可透過多種方式從遠端測試連線。

#### Outline 伺服器

透過 Shadowsocks 傳輸方式，遠端連線至標準 Outline 伺服器。

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "ss://{remote_shadowsocks_credentials}" https://ipinfo.io | jq
```

#### 透過 SSH 使用 SOCKS5

使用 SSH 通道建立 SOCKS5 Proxy。

```sh
ssh -D 127.0.0.1:1080 -C -N $USER@$HOST:$PORT
```

使用 fetch 連線至該通道

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "socks5://localhost:1080" https://ipinfo.io | jq
```

## 個案研究：在伊朗規避 YouTube 封鎖

以下是偵測及略過網路干擾的實用範例。

### 偵測封鎖

透過伊朗的 Proxy 擷取 YouTube 首頁時，要求會逾時，表示遭到封鎖。

```sh
export TRANSPORT="ss://{remote_shadowsocks_credentials}"
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)" https://www.youtube.com
```

這個指令會因逾時而失敗。

### 透過 TLS 分段繞過

在傳輸作業中加入 TLS 片段化，即可繞過這項封鎖。

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|override:host=$(dig +short www.youtube.com | tail -1)|tlsfrag:1" https://www.youtube.com | grep -oe '<title>.*</title>'
```

這項指令成功擷取 YouTube 首頁的標題，也就是「`<title>YouTube</title>`」。

### 使用 TLS 分段和 DNS-over-HTTPS 繞過

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|tlsfrag:1|doh:name=cloudflare-dns.com&address=www.cloudflare.net" https://www.youtube.com | grep -oe '<title>.*</title>'
```

這也會成功傳回 `<title>YouTube</title>`。

### 使用 Outline 伺服器繞過限制

```sh
go run github.com/OutlineFoundation/outline-sdk/x/tools/fetch@latest -timeout 15 -transport "${TRANSPORT}|ss://<your_shadowsocks_credentials>" https://www.youtube.com | grep -oe '<title>.*</title>'
```

這也會傳回 `<title>YouTube</title>`。

## 進一步分析和資源

如要參與討論或提問，請前往 [Outline SDK 討論群組](https://github.com/OutlineFoundation/outline-sdk/discussions)。
