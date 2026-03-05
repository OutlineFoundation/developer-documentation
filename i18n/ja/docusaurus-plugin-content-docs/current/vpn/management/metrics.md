---
title: "Access Performance Metrics"
sidebar_label: "Performance Metrics"
---

Outline は [Prometheus](https://prometheus.io/) を通じて詳細なパフォーマンス指標を提供するため、ユーザーはサーバーの使用状況や健全性に関する詳しい分析情報を得ることができます。このガイドでは、これらの指標の取得および表示のプロセスについて説明します。

**重要な注意事項:** このガイドは、Prometheus と PromQL の基礎を理解していることを前提としています。Prometheus についてよくご存じでない場合は、Outline の指標を詳しく確認する前に、Prometheus のドキュメントやチュートリアルを参照することをご検討ください。

## 前提条件

- **Prometheus が有効な Outline サーバー**: Outline サーバーで Prometheus 指標が有効になっていることを確認します（通常、これはデフォルトの設定です）。

- **サーバーへの SSH アクセス**: Prometheus ポートを転送するには SSH アクセスが必要です。

## 手順

1. **Prometheus ポートを転送する**

SSH を使用してサーバーに接続し、ポート 9090 を転送します。

```sh
ssh root@your_server_ip -L 9090:localhost:9090
```

2. **Prometheus ウェブ インターフェースにアクセスする**

ウェブブラウザを開き、<http://localhost:9090/graph> に移動します。
Prometheus 指標に対するクエリを実行する

3. **PromQL クエリを使用して、関心のある指標を取得します。**

### PromQL クエリの例

#### 使用状況

- **データのバイト数（アクセスキー、プロトコル、方向ごと）:**

`increase(shadowsocks_data_bytes[1d])`

- **データのバイト数（アクセスキーで集計）:**

`sum(increase(shadowsocks_data_bytes[1d])) by (access_key)`

- **データのバイト数（データ上限の計算用）:**

`sum(increase(shadowsocks_data_bytes{dir=~"c<p|p>t"}[30d])) by (access_key)`

- **データのバイト数（場所、プロトコル、方向ごと）:**

`increase(shadowsocks_data_bytes_per_location[1d])`

#### アクティブなアクセスキー

`sum(max(max_over_time(shadowsocks_data_bytes{access_key!=""} [1h])) by (access_key) > bool 0)`

#### TCP 接続

- **TCP 接続（アクセスキー、場所、ステータスごと）:**

`increase(shadowsocks_tcp_connections_closed[1d])`

- **TCP 接続（場所ごと）:**

`increase(shadowsocks_tcp_connections_opened[1d])`

#### UDP

- **UDP パケット（場所、ステータスごと）:**

`increase(shadowsocks_udp_packets_from_client_per_location[1d])`

- **UDP の関連付け（内訳なし）:**

`increase(shadowsocks_udp_nat_entries_added[1d])`

#### パフォーマンス

- **CPU 使用率（プロセスごと）:**

`rate(process_cpu_seconds_total[10m])`

- **メモリ（プロセスごと）:**

`process_virtual_memory_bytes`

#### ビルド情報

- **Prometheus:**

`prometheus_build_info`

- **outline-ss-server:**

`shadowsocks_build_info`

- **Node.js:**

`nodejs_version_info`

使用可能な指標の完全なリストは、`outline-ss-server`
[ソースコード](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/metrics.go)で確認できます。
