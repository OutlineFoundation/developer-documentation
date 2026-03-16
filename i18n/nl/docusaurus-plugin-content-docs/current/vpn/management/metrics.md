---
title: "Prestatiestatistieken van Outline-server openen"
sidebar_label: "Prestatiestatistieken van Outline-server openen"
---

Outline biedt uitgebreide prestatiestatistieken via [Prometheus](https://prometheus.io/), waarmee je meer inzicht krijgt in het gebruik en de status van je server. Deze handleiding leidt je door het proces om deze statistieken op te halen en te checken.

**Belangrijke opmerking:** In deze handleiding gaan we ervan uit dat je de basis van Prometheus en PromQL onder de knie hebt. Als je Prometheus nog niet eerder hebt gebruikt, raden we je aan de documentatie en tutorials van Prometheus door te nemen voordat je aan de slag gaat met de statistieken van Outline.

## Vereisten {#prerequisites}

- **Outline-server met Prometheus aangezet**: Zorg dat Prometheus aanstaat voor je Outline-server. (Dit is meestal de standaardconfiguratie.)

- **SSH-toegang tot je server**: Je moet SSH-toegang hebben om de Prometheus-poort door te sturen.

## Instructies {#instructions}

1. **Prometheus-poort doorsturen**

Maak verbinding met je server via SSH en stuur poort 9090 door:

```sh
ssh root@your_server_ip -L 9090:localhost:9090
```

2. **De Prometheus-webinterface openen**

Open je webbrowser en ga naar: <http://localhost:9090/graph>
Query maken voor Prometheus-statistieken

3. **Gebruik PromQL-query's om de specifieke statistieken op te halen die je wilt doornemen.**

### Voorbeeld van PromQL-query's {#example_promql_queries}

#### Gebruik {#usage}

- **Gegevensbytes (per toegangssleutel, protocol en richting):**

`increase(shadowsocks_data_bytes[1d])`

- **Gegevensbytes (verzameld door toegangssleutel):**

`sum(increase(shadowsocks_data_bytes[1d])) by (access_key)`

- **Gegevensbytes (om gegevenslimieten te berekenen):**

`sum(increase(shadowsocks_data_bytes{dir=~"c<p|p>t"}[30d])) by (access_key)`

- **Gegevensbytes (per locatie, protocol en richting):**

`increase(shadowsocks_data_bytes_per_location[1d])`

#### Actieve toegangssleutels {#active_access_keys}

`sum(max(max_over_time(shadowsocks_data_bytes{access_key!=""} [1h])) by (access_key) > bool 0)`

#### TCP-verbindingen {#tcp_connections}

- **TCP-verbindingen (per toegangssleutel, locatie en status):**

`increase(shadowsocks_tcp_connections_closed[1d])`

- **TCP-verbindingen (per locatie):**

`increase(shadowsocks_tcp_connections_opened[1d])`

#### UDP {#udp}

- **UDP-pakketten (per locatie en status):**

`increase(shadowsocks_udp_packets_from_client_per_location[1d])`

- **UDP-koppelingen (geen uitsplitsing):**

`increase(shadowsocks_udp_nat_entries_added[1d])`

#### Prestaties {#performance}

- **CPU-gebruik (per process):**

`rate(process_cpu_seconds_total[10m])`

- **Geheugen (per process):**

`process_virtual_memory_bytes`

#### Informatie over build {#build_information}

- **Prometheus:**

`prometheus_build_info`

- **outline-ss-server:**

`shadowsocks_build_info`

- **Node.js:**

`nodejs_version_info`

De complete lijst met beschikbare statistieken staat in de `outline-ss-server`
[broncode](https://github.com/OutlineFoundation/outline-ss-server/blob/master/cmd/outline-ss-server/metrics.go).
