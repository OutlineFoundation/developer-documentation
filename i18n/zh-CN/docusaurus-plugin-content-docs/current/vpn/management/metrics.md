---
title: "Access Performance Metrics"
sidebar_label: "Performance Metrics"
---

Outline 通过 [Prometheus](https://prometheus.io/) 提供详细的性能指标，可助您深入了解有关服务器的使用情况和健康状况。本指南为您详细介绍了检索和查看这些指标的相关流程。

**重要注意事项**：本指南在编写时假定您对 Prometheus 和 PromQL 有基本的了解。如果您刚刚接触 Prometheus，不妨先查阅相关的文档和教程，然后再探索 Outline 的各项指标。

## 前提条件

- 

**Outline 服务器（已启用 Prometheus）**：确保您的 Outline 服务器已启用 Prometheus 指标。（这通常是默认配置）。

- 

**对服务器的 SSH 访问权限**：您需要使用 SSH 访问权限来转发 Prometheus 端口。

## 操作说明

1. 

**转发 Prometheus 端口**

使用 SSH 连接到服务器，并转发 9090 端口：

2. 

**访问 Prometheus 网页界面**

打开网络浏览器，并访问 <http://localhost:9090/graph>
查询 Prometheus 指标

3. 

**使用 PromQL 查询检索您感兴趣的指标。**

### PromQL 查询示例

#### 使用情况

- 

**数据字节数（按访问密钥、协议和方向统计）：**

`increase(shadowsocks_data_bytes[1d])`

- 

**数据字节数（按访问密钥汇总）：**

`sum(increase(shadowsocks_data_bytes[1d])) by (access_key)`

- 

**数据字节数（用于数据限值计算）：**

`sum(increase(shadowsocks_data_bytes{dir=~"c<p|p>t"}[30d])) by (access_key)`

- 

**数据字节数（按位置、协议和方向统计）：**

`increase(shadowsocks_data_bytes_per_location[1d])`

#### 有效的访问密钥

`sum(max(max_over_time(shadowsocks_data_bytes{access_key!=""} [1h])) by (access_key) > bool 0)`

#### TCP 连接

- 

**TCP 连接数（按访问密钥、位置和状态统计）：**

`increase(shadowsocks_tcp_connections_closed[1d])`

- 

**TCP 连接数（按位置统计）：**

`increase(shadowsocks_tcp_connections_opened[1d])`

#### UDP

- 

**UDP 数据包量（按位置和状态统计）：**

`increase(shadowsocks_udp_packets_from_client_per_location[1d])`

- 

**UDP 关联量（无细分）：**

`increase(shadowsocks_udp_nat_entries_added[1d])`

#### 性能

- 

**CPU 使用情况（按进程统计）：**

`rate(process_cpu_seconds_total[10m])`

- 

**内存（按进程统计）：**

`process_virtual_memory_bytes`

#### 构建信息

- 

**Prometheus：**

`prometheus_build_info`

- 

**outline-ss-server：**

`shadowsocks_build_info`

- 

**Node.js：**

`nodejs_version_info`

如需查看可用指标的完整列表，请参阅 `outline-ss-server` [源代码](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/metrics.go)。
