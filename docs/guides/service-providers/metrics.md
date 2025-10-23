Project: /outline/_project.yaml
Book: /outline/_book.yaml

# Accessing Outline Server Performance Metrics

Outline provides detailed performance metrics through
[Prometheus](https://prometheus.io/), allowing you to gain deeper insights into
your server's usage and health. This guide will walk you through the process of
retrieving and viewing these metrics.

**Important Note:** This guide assumes you have a basic understanding of
Prometheus and PromQL. If you're new to Prometheus, consider exploring its
documentation and tutorials before diving into Outline's metrics.

## Prerequisites

- **Outline server with Prometheus enabled**: Ensure that your Outline server
has Prometheus metrics enabled. (This is usually the default configuration).

- **SSH access to your server**: You'll need SSH access to forward the
Prometheus port.

## Instructions

1. **Forward Prometheus Port**

    Connect to your server using SSH and forward port 9090:

    ```sh
    ssh root@your_server_ip -L 9090:localhost:9090
    ```

1. **Access Prometheus Web Interface**

    Open your web browser and navigate to: <http://localhost:9090/graph>
    Query Prometheus Metrics

1. **Use PromQL queries to retrieve the specific metrics you're interested in.**

### Example PromQL Queries

#### Usage

- **Data Bytes (by access key, protocol, and direction):**

  `increase(shadowsocks_data_bytes[1d])`

- **Data Bytes (aggregated by access key):**

  `sum(increase(shadowsocks_data_bytes[1d])) by (access_key)`

- **Data Bytes (for data limits calculation):**

  `sum(increase(shadowsocks_data_bytes{dir=~"c<p|p>t"}[30d])) by (access_key)`

- **Data Bytes (by location, protocol, and direction):**

  `increase(shadowsocks_data_bytes_per_location[1d])`

#### Active Access Keys

`sum(max(max_over_time(shadowsocks_data_bytes{access_key!=""} [1h])) by (access_key) > bool 0)`

#### TCP Connections

- **TCP Connections (by access key, location, and status):**

  `increase(shadowsocks_tcp_connections_closed[1d])`

- **TCP Connections (by location):**

  `increase(shadowsocks_tcp_connections_opened[1d])`

#### UDP

- **UDP Packets (by location and status):**

  `increase(shadowsocks_udp_packets_from_client_per_location[1d])`

- **UDP Associations (no breakdown):**

  `increase(shadowsocks_udp_nat_entries_added[1d])`

#### Performance

- **CPU Usage (by process):**

  `rate(process_cpu_seconds_total[10m])`

- **Memory (by process):**

  `process_virtual_memory_bytes`

#### Build Information

- **Prometheus:**

  `prometheus_build_info`

- **outline-ss-server:**

  `shadowsocks_build_info`

- **Node.js:**

  `nodejs_version_info`

The complete list of available metrics can be found in the `outline-ss-server`
[source code](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/metrics.go).