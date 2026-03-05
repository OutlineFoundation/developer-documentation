---
title: "Access Performance Metrics"
sidebar_label: "Performance Metrics"
---

Outline ofrece métricas de rendimiento detalladas a través de [Prometheus](https://prometheus.io/), lo que te permite acceder a estadísticas más exhaustivas sobre el uso y el estado de tu servidor. Esta guía explica el proceso de obtener y consultar esas métricas.

**Nota importante:** En esta guía se asume que tienes nociones básicas de Prometheus y PromQL. Si nunca has usado Prometheus, te recomendamos consultar su documentación y tutoriales antes de analizar las métricas de Outline.

## Requisitos previos

- 

**Servidor de Outline con Prometheus habilitado:** asegúrate de que tu servidor de Outline tiene habilitadas las métricas de Prometheus (suele ser la configuración predeterminada).

- 

**Acceso SSH a tu servidor:** necesitarás acceso SSH para redirigir el puerto de Prometheus.

## Instrucciones

1. 

**Redirigir el puerto de Prometheus**

Conéctate a tu servidor mediante SSH y redirige el puerto 9090:

2. 

**Acceder a la interfaz web de Prometheus**

Abre tu navegador web y ve a: <http://localhost:9090/graph>
Consultar las métricas de Prometheus

3. 

**Usa las consultas de PromQL para obtener las métricas que te interesen.**

### Ejemplos de consultas de PromQL

#### Uso

- 

**Bytes de datos (por clave de acceso, protocolo y dirección):**

`increase(shadowsocks_data_bytes[1d])`

- 

**Bytes de datos (agregados por clave de acceso):**

`sum(increase(shadowsocks_data_bytes[1d])) by (access_key)`

- 

**Bytes de datos (para el cálculo de límites de datos):**

`sum(increase(shadowsocks_data_bytes{dir=~"c<p|p>t"}[30d])) by (access_key)`

- 

**Bytes de datos (por ubicación, protocolo y dirección):**

`increase(shadowsocks_data_bytes_per_location[1d])`

#### Claves de acceso activas

`sum(max(max_over_time(shadowsocks_data_bytes{access_key!=""} [1h])) by (access_key) > bool 0)`

#### Conexiones TCP

- 

**Conexiones TCP (por clave de acceso, ubicación y estado):**

`increase(shadowsocks_tcp_connections_closed[1d])`

- 

**Conexiones TCP (por ubicación):**

`increase(shadowsocks_tcp_connections_opened[1d])`

#### UDP

- 

**Paquetes UDP (por ubicación y estado):**

`increase(shadowsocks_udp_packets_from_client_per_location[1d])`

- 

**Asociaciones UDP (sin desglose):**

`increase(shadowsocks_udp_nat_entries_added[1d])`

#### Rendimiento

- 

**Uso de CPU (por proceso):**

`rate(process_cpu_seconds_total[10m])`

- 

**Memoria (por proceso):**

`process_virtual_memory_bytes`

#### Información de compilación

- 

**Prometheus:**

`prometheus_build_info`

- 

**outline-ss-server:**

`shadowsocks_build_info`

- 

**Node.js:**

`nodejs_version_info`

Puedes consultar la lista completa de las métricas disponibles en el [código fuente](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/metrics.go) de `outline-ss-server`.
