---
title: "Disguise Connections as Web Traffic with Shadowsocks-over-WebSockets"
sidebar_label: "WebSockets"
---

Outline 用戶端 1.15.0 以上版本。**

本教學課程將詳述 Shadowsocks-over-WebSockets 的實作步驟，使您能在一般 Shadowsocks 連線受阻的環境中有效規避審查。其原理是將 Shadowsocks 流量封裝在 WebSocket 中，偽裝成標準網路流量，進而提升抗封鎖能力與存取性。

## 步驟 1：設定並執行 Outline 伺服器

建立新的 `config.yaml` 檔案並加入以下設定：

下載最新的 [`outline-ss-server`](https://github.com/Jigsaw-Code/outline-ss-server/releases)，並使用已建立的設定執行，如下所示：

## 步驟 2：公開網路伺服器

為了讓大眾能存取您的 WebSocket 網路伺服器，您需要將伺服器公開至網際網路並設定 [TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security)。您可以選擇使用 [Caddy](https://caddyserver.com/)、[nginx](https://nginx.org/) 或 [Apache](https://httpd.apache.org/) 等本機網路伺服器，並確保該伺服器具備有效的 TLS 憑證；或是運用 [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)、[ngrok](https://ngrok.com/) 等通道服務。

### 使用 TryCloudflare 的示例

我們將以 [TryCloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/) 為例，示範如何建立快速通道。這個方法既便利又安全，讓您無需開放傳入通訊埠，即可公開本機網路伺服器。

1. 

下載並安裝 [`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)。

2. 

建立指向本機網路伺服器通訊埠的通道，如下所示：

Cloudflare 會提供一個子網域 (例如 `acids-iceland-davidson-lb.trycloudflare.com`)，用於存取您的 WebSocket 端點並自動處理 TLS。請記下這個子網域，後續設定將會用到。

## 步驟 3：建立動態存取金鑰

使用[存取金鑰設定](../management/config)格式為使用者產生用戶端存取金鑰 YAML 檔案，並納入先前在伺服器端設定的 WebSocket 端點，如下所示：

產生動態存取金鑰 YAML 檔案後，您需要將檔案提供給使用者，比如將檔案託管於靜態網站代管服務，或動態產生檔案。進一步瞭解如何使用[動態存取金鑰](../management/dynamic-access-keys)。

## 步驟 4：使用 Outline 用戶端連線

使用官方 [Outline 用戶端](../../download-links)應用程式 (1.15.0 以上版本)，將新建立的動態存取金鑰新增為伺服器項目。點選「連線」****，即可使用 Shadowsocks-over-Websocket 設定建立的通道連線至您的伺服器。

您可以使用類似 [IPInfo](https://ipinfo.io) 的工具，確認目前是否透過 Outline 伺服器瀏覽網際網路。
