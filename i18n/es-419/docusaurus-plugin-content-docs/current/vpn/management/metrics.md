---
title: "Access Performance Metrics"
sidebar_label: "Performance Metrics"
---

Outline proporciona métricas de rendimiento detalladas a través de
[Prometheus](https://prometheus.io/), lo que te permite obtener estadísticas detalladas sobre el uso
y el estado de tu servidor. En esta guía, te explicaremos el proceso para
obtener y consultar estas métricas.

**Nota importante:** En esta guía, se supone que tienes conocimientos básicos de
Prometheus y PromQL. Si no conoces Prometheus, sugerimos que leas su
documentación y sus instructivos antes de adentrarte en las métricas de Outline.

## Requisitos previos

- **Servidor de Outline con Prometheus habilitado**: Asegúrate de que tu servidor de Outline
tenga habilitadas las métricas de Prometheus (por lo general, esta es la configuración predeterminada).

- **Acceso SSH a tu servidor**: Deberás contar con acceso SSH para reenviar el
puerto de Prometheus.

## Instrucciones

1. **Reenvía el puerto de Prometheus**

Conecta tu servidor usando SSH y el puerto de reenvío 9090:

2. **Accede a la interfaz web de Prometheus**

Abre tu navegador web y dirígete a <http://localhost:9090/graph>
Consulta las métricas de Prometheus

3. **Usa las consultas de PromQL para recuperar las métricas específicas que te interesan.**

### Consultas PromQL de ejemplo

#### Uso

- **Bytes de datos (por clave de acceso, protocolo y dirección):**

`increase(shadowsocks_data_bytes[1d])`

- **Bytes de datos (agregados por clave de acceso):**

`sum(increase(shadowsocks_data_bytes[1d])) by (access_key)`

- **Bytes de datos (para calcular límites de datos):**

`sum(increase(shadowsocks_data_bytes{dir=~"c<p|p>t"}[30d])) by (access_key)`

- **Bytes de datos (por ubicación, protocolo y dirección):**

`increase(shadowsocks_data_bytes_per_location[1d])`

#### Claves de acceso activas

`sum(max(max_over_time(shadowsocks_data_bytes{access_key!=""} [1h])) by (access_key) > bool 0)`

#### Conexiones de TCP

- **Conexiones de TCP (por clave de acceso, ubicación y estado):**

`increase(shadowsocks_tcp_connections_closed[1d])`

- **Conexiones de TCP (por ubicación):**

`increase(shadowsocks_tcp_connections_opened[1d])`

#### UDP

- **Paquetes de UDP (por ubicación y estado):**

`increase(shadowsocks_udp_packets_from_client_per_location[1d])`

- **Asociaciones de UDP (sin desglose):**

`increase(shadowsocks_udp_nat_entries_added[1d])`

#### Rendimiento

- **Uso de CPU (por proceso):**

`rate(process_cpu_seconds_total[10m])`

- **Memoria (por proceso):**

`process_virtual_memory_bytes`

#### Información de compilación

- **Prometheus:**

`prometheus_build_info`

- **outline-ss-server:**

`shadowsocks_build_info`

- **Node.js:**

`nodejs_version_info`

Puedes encontrar la lista completa de métricas disponibles en el [código fuente](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/metrics.go) de `outline-ss-server`.
