---
title: "Access Performance Metrics"
sidebar_label: "Performance Metrics"
---

Outline bietet detaillierte Leistungsmesswerte mit [Prometheus](https://prometheus.io/). So sind Sie immer auf dem Laufenden über die Leistung und Nutzung Ihres Servers. In dieser Anleitung erfahren Sie, wie Sie diese Messwerte erhalten und aufrufen können.

**Wichtiger Hinweis:** Diese Anleitung geht davon aus, dass Sie bereits Grundkenntnisse zu Prometheus und PromQL haben. Wenn Sie Prometheus noch nicht so gut kennen, empfehlen wir Ihnen, sich damit in seiner Dokumentation und in Tutorials zu beschäftigen, bevor Sie sich den Messwerten von Outline widmen.

## Voraussetzungen

- **Outline-Server mit aktiviertem Prometheus**: Prüfen Sie, ob die Prometheus-Metriken auf Ihrem Outline-Server aktiviert sind. (Das ist für gewöhnlich die Standardeinstellung.)

- **SSH-Zugriff auf Ihren Server**: Sie benötigen den SSH-Zugriff, um den Prometheus-Port weiterzuleiten.

## Anleitung

1. **Prometheus-Port weiterleiten**

Verbinden Sie sich über SSH mit Ihrem Server und leiten Sie den Port 9090 weiter:

2. **Auf Prometheus-Weboberfläche zugreifen**

Öffnen Sie Ihren Browser und gehen Sie zu: <http://localhost:9090/graph> Prometheus-Messwerte abfragen

3. **Nutzen Sie PromQL-Abfragen, um genau die Messwerte zu erhalten, die Sie interessieren.**

### Beispiel für PromQL-Abfragen

#### Nutzung

- **Datenbytes (über Zugriffsschlüssel, protokoll und Route):**

`increase(shadowsocks_data_bytes[1d])`

- **Datenbytes (über Zugriffsschlüssel aggregiert):**

`sum(increase(shadowsocks_data_bytes[1d])) by (access_key)`

- **Datenbytes (für die Berechnung von Datenlimits):**

`sum(increase(shadowsocks_data_bytes{dir=~"c<p|p>t"}[30d])) by (access_key)`

- **Datenbytes (by Standort, Protokoll und Route):**

`increase(shadowsocks_data_bytes_per_location[1d])`

#### Aktive Zugriffsschlüssel

`sum(max(max_over_time(shadowsocks_data_bytes{access_key!=""} [1h])) by (access_key) > bool 0)`

#### TCP-Verbindungen

- **TC-Verbindungen (über Zugriffsschlüssel, Standort und Status):**

`increase(shadowsocks_tcp_connections_closed[1d])`

- **TCP-Verbindungen (über Standort):**

`increase(shadowsocks_tcp_connections_opened[1d])`

#### UDP

- **UDP-Pakete (über Standort und Status):**

`increase(shadowsocks_udp_packets_from_client_per_location[1d])`

- **UDP-Verknüpfungen (keine Aufschlüsselung):**

`increase(shadowsocks_udp_nat_entries_added[1d])`

#### Performance

- **CPU-Nutzung (nach Verarbeitung):**

`rate(process_cpu_seconds_total[10m])`

- **Arbeitsspeicher (nach Verarbeitung):**

`process_virtual_memory_bytes`

#### Build-Informationen

- **Prometheus:**

`prometheus_build_info`

- **Outline-ss-Server:**

`shadowsocks_build_info`

- **Node.js:**

`nodejs_version_info`

Eine vollständige Liste der verfügbaren Messwerte finden Sie im `outline-ss-server`
[Quellcode](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/metrics.go).
