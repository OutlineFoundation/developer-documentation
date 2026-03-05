---
title: "Smart Dialer Configuration"
sidebar_label: "Smart Dialer Config"
---

**Smart Dialer** 會針對指定測試網域，搜尋能解除 DNS 和 TLS 封鎖的策略。這個元件會讀取包含多種策略的設定，並從中選擇一種策略。

## Smart Dialer 的 YAML 設定

Smart Dialer 使用的設定為 YAML 格式，範例如下：

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

### DNS 設定

- `dns` 欄位用於指定要測試的一組 DNS 解析器。

- DNS 解析器可為下列任一類型：

    - `system`：使用系統解析器，需透過空物件指定。

    - `https`：使用加密的 DNS-over-HTTPS (DoH) 解析器。

    - `tls`：使用加密的 DNS-over-TLS (DoT) 解析器。

    - `udp`：使用 UDP 解析器。

    - `tcp`：使用 TCP 解析器。

#### DNS-over-HTTPS 解析器 (DoH)

```yaml
https:
  name: dns.google
  address: 8.8.8.8
```

- `name`：DoH 伺服器的網域名稱。

- `address`：DoH 伺服器的主機和通訊埠，格式為 <主機>:<通訊埠>。預設為 `name`:443。

#### DNS-over-TLS 解析器 (DoT)

```yaml
tls:
  name: dns.google
  address: 8.8.8.8
```

- `name`：DoT 伺服器的網域名稱。

- `address`：DoT 伺服器的主機和通訊埠，格式為 <主機>:<通訊埠>。預設為 `name`:853。

#### UDP 解析器

```yaml
udp:
  address: 8.8.8.8
```

- `address`：UDP 解析器的主機和通訊埠，格式為 <主機>:<通訊埠>。

#### TCP 解析器

```yaml
tcp:
  address: 8.8.8.8
```

- `address`：TCP 解析器的主機和通訊埠，格式為 <主機>:<通訊埠>。

### TLS 設定

- `tls` 欄位用於指定一組要測試的 TLS 傳輸方式。

- 每個 TLS 傳輸方式皆以一組字串表示，指定所用傳輸機制。

- 例如，`override:host=cloudflare.net|tlsfrag:1` 表示使用 Cloudflare 的網域前置技術和 TLS 分割進行傳輸，詳見[設定說明文件](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x/configurl#hdr-Config_Format)。

### 備援設定

當所有無 Proxy 策略都無法建立連線時，系統會使用備援設定。例如，備援設定可指定備用的 Proxy 伺服器，嘗試與使用者建立連線。只有在其他 DNS/TLS 策略失敗或逾時時，系統才會使用備援設定，因此連線啟動時間會較長。

備援設定字串應符合以下格式：

- 有效的 `StreamDialer` 設定字串，定義於 [`configurl`](https://pkg.go.dev/github.com/Jigsaw-Code/outline-sdk/x/configurl#hdr-Proxy_Protocols) 中。

- 有效的 Psiphon 設定物件，做為 `psiphon` 欄位的子項。

#### Shadowsocks 伺服器範例

```yaml
fallback:
  - ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTprSzdEdHQ0MkJLOE9hRjBKYjdpWGFK@1.2.3.4:9999/?outline=1
```

#### SOCKS5 伺服器範例

```yaml
fallback:
  - socks5://[USERINFO]@[HOST]:[PORT]
```

#### Psiphon 設定範例

如要使用 [Psiphon](https://psiphon.ca/) 網路，請採取以下行動：

1. 聯絡 Psiphon 團隊，取得可連上他們網路的設定。這可能需要簽訂合約。

2. 將取得的 Psiphon 設定加入 Smart Dialer 設定的 `fallback` 區塊。由於 JSON 與 YAML 相容，所以直接將 Psiphon 設定內容複製貼到 `fallback` 區塊即可，如下所示：

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

### 如何使用 Smart Dialer

如要使用 Smart Dialer，請建立 `StrategyFinder` 物件並呼叫 `NewDialer` 方法，傳入測試網域清單和 YAML 設定。
`NewDialer` 方法會傳回 `transport.StreamDialer`，可用來依據選出的策略建立連線。例如：

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

這是基本範例，實際使用時可能需要根據具體情況做調整。
