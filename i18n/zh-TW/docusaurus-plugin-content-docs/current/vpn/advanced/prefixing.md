---
title: "prefix 偽裝的連線"
sidebar_label: "prefix 偽裝的連線"
---

自 Outline 用戶端 1.9.0 版起，存取金鑰支援「prefix」選項。「prefix」是 Shadowsocks TCP 連線中做為[鹽](https://shadowsocks.org/doc/aead.html)開頭的一串位元組。這可以使連線偽裝成網路中允許的協定，從而繞過防火牆對未知通訊協定的封鎖。

## 何時應嘗試使用 prefix？ {#when_should_i_try_this}

如果您懷疑 Outline 部署的使用者仍然受到封鎖，可以考慮嘗試幾組 prefix。

## 操作說明 {#instructions}

prefix 的長度不應超過 16 個位元組。較長的 prefix 可能會導致鹽值重複，因而影響加密安全性，使得連線被偵測到。建議盡可能使用最短的 prefix 來繞過封鎖。

您使用的通訊埠應與 prefix 偽裝的通訊協定一致。在 IANA 維護的[傳輸通訊協定埠號註冊表](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)中，您可以查看各種通訊協定對應的埠號。

以下是一些模擬常見通訊協定的有效 prefix：

建議通訊埠
JSON 編碼
網址編碼

HTTP 要求
80 (http)
`"POST "`
`POST%20`

HTTP 回應
80 (http)
`"HTTP/1.1 "`
`HTTP%2F1.1%20`

DNS-over-TCP 要求
53 (dns)
`"\u0005\u00DC\u005F\u00E0\u0001\u0020"`
`%05%C3%9C_%C3%A0%01%20`

TLS ClientHello
443 (https)、463 (smtps)、563 (nntps)、636 (ldaps)、989 (ftps-data)、990 (ftps)、993 (imaps)、995 (pop3s)、5223 (Apple APN)、5228 (Play 商店)、5349 (turns)
`"\u0016\u0003\u0001\u0000\u00a8\u0001\u0001"`
`%16%03%01%00%C2%A8%01%01`

TLS 應用程式資料
443 (https)、463 (smtps)、563 (nntps)、636 (ldaps)、989 (ftps-data)、990 (ftps)、993 (imaps)、995 (pop3s)、5223 (Apple APN)、5228 (Play 商店)、5349 (turns)
`"\u0013\u0003\u0003\u003F"`
`%13%03%03%3F`

TLS ServerHello
443 (https)、463 (smtps)、563 (nntps)、636 (ldaps)、989 (ftps-data)、990 (ftps)、993 (imaps)、995 (pop3s)、5223 (Apple APN)、5228 (Play 商店)、5349 (turns)
`"\u0016\u0003\u0003\u0040\u0000\u0002"`
`%16%03%03%40%00%02`

SSH
22 (ssh)、830 (netconf-ssh)、4334 (netconf-ch-ssh)、5162 (snmpssh-trap)
`"SSH-2.0\r\n"`
`SSH-2.0%0D%0A`

### 動態存取金鑰 {#dynamic_access_keys}

如要在[動態存取金鑰](../management/dynamic-access-keys) (`ssconf://`) 中使用 prefix 功能，請在 JSON 物件中新增「prefix」鍵，並將所需的 prefix 以 **JSON 編碼**表示 (參見上表示例)。您可以使用 \u00FF 之類的逸出代碼，表示 `U+0` 至 `U+FF` 範圍內的不可列印 Unicode 代碼點，例如：

```json
{
    "server": "example.com",
    "server_port": 8388,
    "password": "example",
    "method": "chacha20-ietf-poly1305",
    "prefix": "\u0005\u00DC\u005F\u00E0\u0001\u0020"
}
```

### 靜態存取金鑰 {#static_access_keys}

如要在**靜態存取金鑰** (ss://) 中使用 prefix，您需要先修改現有金鑰再發布。如果您使用 Outline Manager 生成的靜態存取金鑰，請將您的 prefix 轉換為**網址編碼**版本 (參見上表示例)，然後加入存取金鑰末端，如下所示：

`ss://Z34nthataITHiTNIHTohithITHbVBqQ1o3bkk@127.0.0.1:33142/?outline=1&prefix=<your url-encoded prefix goes here>`

對於進階使用者，您可以運用瀏覽器的 `encodeURIComponent()` 函式將 **JSON 編碼**的 prefix 轉換為**網址編碼**版本。如要這麼做，請開啟網頁檢查器控制台 (在 Chrome 中依序點選「Developer」>「JavaScript Web Console」) 並輸入以下內容：

```js
encodeURIComponent("<your json-encoded prefix goes here>")
```

按下 Enter 鍵，生成的值即為「網址編碼」版本，例如：

```js
encodeURIComponent("\u0016\u0003\u0001\u0000\u00a8\u0001\u0001")
'%16%03%01%00%C2%A8%01%01'
```
