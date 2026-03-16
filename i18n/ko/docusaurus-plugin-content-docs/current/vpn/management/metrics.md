---
title: "Access Performance Metrics"
sidebar_label: "Performance Metrics"
---

Outline에서는 [Prometheus](https://prometheus.io/)를 통해 자세한 성능 측정항목을 제공하므로 서버의 사용과 상태에 관한 상세하고 유용한 정보를 확인할 수 있습니다. 이 가이드에서는 이러한 측정항목을 검색해 확인하는 과정을 안내합니다.

**중요 참고사항:** 이 가이드에서는 Prometheus와 PromQL을 기본적으로 알고 있다고 가정합니다. Prometheus를 모른다면 문서와 튜토리얼을 살펴본 후 Outline의 측정항목을 살펴보는 것이 좋습니다.

## 기본 요건 {#prerequisites}

- **Prometheus가 사용 설정된 Outline 서버**: Outline 서버에 Prometheus 측정항목이 사용 설정되어 있어야 합니다. 이는 일반적으로 기본 구성입니다.

- **서버에 대한 SSH 액세스**: Prometheus 포트를 전달하려면 SSH 액세스가 필요합니다.

## 안내 {#instructions}

1. **Prometheus 포트 전달**

SSH를 사용하여 서버에 연결하고 포트 9090을 전달합니다.

```sh
ssh root@your_server_ip -L 9090:localhost:9090
```

2. **Prometheus 웹 인터페이스 액세스**

웹브라우저를 열고 <http://localhost:9090/graph> Query Prometheus Metrics로 이동합니다.

3. **PromQL 쿼리를 사용하여 관심 있는 특정 측정항목 검색**

### PromQL 쿼리 예 {#example_promql_queries}

#### 사용 {#usage}

- **데이터 바이트(액세스 키, 프로토콜, 방향별):**

`increase(shadowsocks_data_bytes[1d])`

- **데이터 바이트(액세스 키별로 집계):**

`sum(increase(shadowsocks_data_bytes[1d])) by (access_key)`

- **데이터 바이트(데이터 한도 계산용):**

`sum(increase(shadowsocks_data_bytes{dir=~"c<p|p>t"}[30d])) by (access_key)`

- **데이터 바이트(위치, 프로토콜, 방향별):**

`increase(shadowsocks_data_bytes_per_location[1d])`

#### 활성 액세스 키 {#active_access_keys}

`sum(max(max_over_time(shadowsocks_data_bytes{access_key!=""} [1h])) by (access_key) > bool 0)`

#### TCP 연결 {#tcp_connections}

- **TCP 연결(액세스 키, 위치, 상태별):**

`increase(shadowsocks_tcp_connections_closed[1d])`

- **TCP 연결(위치별):**

`increase(shadowsocks_tcp_connections_opened[1d])`

#### UDP {#udp}

- **UDP 패킷(위치, 상태별):**

`increase(shadowsocks_udp_packets_from_client_per_location[1d])`

- **UDP 연결(분류 없음):**

`increase(shadowsocks_udp_nat_entries_added[1d])`

#### 성능 {#performance}

- **CPU 사용량(프로세스별):**

`rate(process_cpu_seconds_total[10m])`

- **메모리(프로세스별):**

`process_virtual_memory_bytes`

#### 빌드 정보 {#build_information}

- **Prometheus:**

`prometheus_build_info`

- **outline-ss-server:**

`shadowsocks_build_info`

- **Node.js:**

`nodejs_version_info`

사용 가능한 측정항목 전체 목록은 `outline-ss-server` [소스 코드](https://github.com/OutlineFoundation/outline-ss-server/blob/master/cmd/outline-ss-server/metrics.go)에서 확인할 수 있습니다.
