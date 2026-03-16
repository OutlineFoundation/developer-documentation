---
title: "Deploy with Automatic HTTPS Using Caddy"
sidebar_label: "HTTPS with Caddy"
---

本指南將說明如何運用 [Caddy](https://caddyserver.com/) 強化 Outline 伺服器設定。Caddy 是一款功能強大又容易使用的網路伺服器，具備[自動 HTTPS](https://caddyserver.com/docs/automatic-https) 功能和彈性設定，是架設 Outline 伺服器的理想選擇，尤其在使用 WebSocket 傳輸時，更能簡化設定。

## 什麼是 Caddy？ {#what_is_caddy}

Caddy 是一款開放原始碼網路伺服器，主打簡單易用、自動設定 HTTPS 及支援多種通訊協定。這項服務可以簡化網路伺服器設定，並提供以下功能：

- **自動 HTTPS：**Caddy 會自動取得並更新 TLS 憑證，確保連線安全。

- **HTTP/3 支援：**Caddy 支援最新的 HTTP/3 通訊協定，讓網路傳輸更快速有效率。

- **以外掛程式擴充：**Caddy 可透過外掛程式擴充，支援反向 Proxy、負載平衡等多種功能。

## 步驟 1：事前準備 {#step_1_prerequisites}

- 下載並安裝 [`xcaddy`](https://github.com/caddyserver/xcaddy)

## 步驟 2：設定網域 {#step_2_configure_your_domain}

啟動 Caddy 前，請確認您的網域名稱已正確設定，指向您的伺服器 IP 位址。

- **設定 A/AAAA 記錄：**登入 DNS 供應商網站，將網域的 A 記錄設為指向伺服器的 IPv4 位址，AAAA 記錄設為指向 IPv6 位址。

- **驗證 DNS 記錄：**使用權威查詢確認 DNS 記錄設定正確，如下所示：

```sh
curl "https://cloudflare-dns.com/dns-query?name=<DOMAIN_NAME>&type=A" \
  -H "accept: application/dns-json"
```

## 步驟 3：建構並執行自訂 Caddy 版本 {#build-and-run}

使用 `xcaddy` 建構自訂 `caddy` 二進位檔，納入 Outline 核心伺服器模組和其他需要的伺服器擴充模組。

```sh
xcaddy build \
  # The example uses a YAML config, so include a YAML config adapter module.
  --with github.com/iamd3vil/caddy_yaml_adapter \
  # The Outline core server module.
  --with github.com/OutlineFoundation/outline-ss-server/outlinecaddy
```

## 步驟 4：設定並執行搭配 Outline 的 Caddy 伺服器 {#step_4_configure_and_run_the_caddy_server_with_outline}

建立新的 `config.yaml` 檔案並加入以下設定：

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

這項設定採用 Shadowsocks-over-WebSockets 策略，網路伺服器會監聽 `443` 通訊埠，並分別在 `TCP_PATH` 和 `UDP_PATH` 路徑接收經 TCP 和 UDP 封裝的 Shadowsocks 流量。

使用已建立的設定，執行經由 Outline 模組擴充的 Caddy 伺服器，如下所示：

```sh
caddy run --config config.yaml --adapter yaml --watch
```

如需更多設定示例，請前往 [outline-ss-server/outlinecaddy GitHub 存放區](https://github.com/OutlineFoundation/outline-ss-server/tree/master/outlinecaddy/examples)。

## 步驟 5：建立動態存取金鑰 {#step_5_create_a_dynamic_access_key}

使用[進階設定](../management/config)格式為使用者產生用戶端存取金鑰 YAML 檔案，並納入先前在伺服器端設定的 WebSocket 端點，如下所示：

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

產生動態存取金鑰 YAML 檔案後，您需要將檔案提供給使用者，比如將檔案託管於靜態網站代管服務，或動態產生檔案。進一步瞭解如何使用[動態存取金鑰](../management/dynamic-access-keys)。

## 步驟 6：使用 Outline 用戶端連線 {#step_6_connect_with_the_outline_client}

使用官方 [Outline 用戶端](../../download-links)應用程式 (1.15.0 以上版本)，將新建立的動態存取金鑰新增為伺服器項目。點選「連線」****，即可使用 Shadowsocks-over-Websocket 設定建立的通道連線至您的伺服器。

您可以使用類似 [IPInfo](https://ipinfo.io) 的工具，確認目前是否透過 Outline 伺服器瀏覽網際網路。
