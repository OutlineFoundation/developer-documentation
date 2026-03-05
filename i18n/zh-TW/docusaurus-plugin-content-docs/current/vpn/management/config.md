---
title: "Configure Access Keys"
sidebar_label: "Configure Access Keys"
---

Outline 運用基於 YAML 的設定來定義 VPN 參數及處理 TCP/UDP 流量。這種設定支援多層次組合，讓配置更靈活且易於擴充。

頂層設定會指定 [TunnelConfig](../reference/access-key-config#tunnelconfig)。

## 示例

典型的 Shadowsocks 設定如下：

請注意，我們現在可以讓 TCP 和 UDP 在不同端點或通訊埠上運作，並使用不同 prefix。

您可以使用 YAML 錨點和 `<<` 合併鍵來避免重複，如下所示：

現在可以組合不同策略並實現多重跳躍，如下所示：

如果 Shadowsocks 等「看似普通」的通訊協定遭到封鎖，您可以使用 Shadowsocks-over-Websockets。關於部署方式，請參考[伺服器範例設定](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/config_example.yml)。用戶端設定如下：

請注意，WebSocket 端點本身也可以指定另一個端點，從而繞過 DNS 封鎖，如下所示：

為確保不同版本的 Outline 用戶端相容性，請在設定中使用 `first-supported` 選項。由於 Outline 會持續新增策略和功能，但並非所有使用者都會立即更新至最新用戶端軟體，因此這一點尤其重要。使用 `first-supported` 時，只需提供單一設定，即可在各種平台和用戶端版本上順暢運作，確保回溯相容性並維持一致的使用體驗。
