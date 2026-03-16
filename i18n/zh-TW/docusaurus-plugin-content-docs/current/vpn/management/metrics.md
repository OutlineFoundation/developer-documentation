---
title: "Access Performance Metrics"
sidebar_label: "Performance Metrics"
---

Outline 會透過 [Prometheus](https://prometheus.io/) 提供詳細效能指標，讓您可以深入瞭解伺服器的使用情形和健康狀態。本指南將逐步引導您檢索與查看這些指標。

**重要注意事項：**本指南假設您已瞭解 Prometheus 和 PromQL 的基本概念。如果您不熟悉 Prometheus，建議先瀏覽相關文件和教學課程，再深入研究 Outline 指標。

## 事前準備 {#prerequisites}

- **已啟用 Prometheus 的 Outline 伺服器**：確認您的 Outline 伺服器已啟用 Prometheus 指標 (這通常是預設設定)。

- **該伺服器的 SSH 存取權**：您需要有 SSH 存取權才能轉發 Prometheus 通訊埠。

## 操作說明 {#instructions}

1. **轉發 Prometheus 通訊埠**

利用 SSH 連線至伺服器，然後轉發通訊埠 9090：

```sh
ssh root@your_server_ip -L 9090:localhost:9090
```

2. **存取 Prometheus 網頁介面**

開啟網路瀏覽器並前往：<http://localhost:9090/graph>
查詢 Prometheus 指標

3. **運用 PromQL 查詢檢索感興趣的特定指標。**

### PromQL 查詢示例 {#example_promql_queries}

#### 使用量 {#usage}

- **資料位元組 (依存取金鑰、通訊協定和方向分類)：**

`increase(shadowsocks_data_bytes[1d])`

- **資料位元組 (依存取金鑰匯總)：**

`sum(increase(shadowsocks_data_bytes[1d])) by (access_key)`

- **資料位元組 (用於計算是否達到數據用量上限)：**

`sum(increase(shadowsocks_data_bytes{dir=~"c<p|p>t"}[30d])) by (access_key)`

- **資料位元組 (依位置、通訊協定和方向分類)：**

`increase(shadowsocks_data_bytes_per_location[1d])`

#### 使用中的存取金鑰 {#active_access_keys}

`sum(max(max_over_time(shadowsocks_data_bytes{access_key!=""} [1h])) by (access_key) > bool 0)`

#### TCP 連線 {#tcp_connections}

- **TCP 連線 (依存取金鑰、通訊協定和狀態分類)：**

`increase(shadowsocks_tcp_connections_closed[1d])`

- **TCP 連線 (依位置分類)：**

`increase(shadowsocks_tcp_connections_opened[1d])`

#### UDP {#udp}

- **UDP 封包 (依位置和狀態分類)：**

`increase(shadowsocks_udp_packets_from_client_per_location[1d])`

- **UDP 關聯 (未細分)：**

`increase(shadowsocks_udp_nat_entries_added[1d])`

#### 效能 {#performance}

- **CPU 用量 (依程序分類)：**

`rate(process_cpu_seconds_total[10m])`

- **記憶體 (依程序分類)：**

`process_virtual_memory_bytes`

#### 建構資訊 {#build_information}

- **Prometheus：**

`prometheus_build_info`

- **outline-ss-server：**

`shadowsocks_build_info`

- **Node.js：**

`nodejs_version_info`

您可以在 `outline-ss-server` 的[原始碼](https://github.com/OutlineFoundation/outline-ss-server/blob/master/cmd/outline-ss-server/metrics.go)中查找完整的可用指標清單。
