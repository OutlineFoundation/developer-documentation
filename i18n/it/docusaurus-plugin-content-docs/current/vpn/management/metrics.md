---
title: "Access Performance Metrics"
sidebar_label: "Performance Metrics"
---

Outline fornisce metriche dettagliate sulle prestazioni tramite
[Prometheus](https://prometheus.io/), consentendoti di ottenere informazioni più approfondite sull'utilizzo e lo stato di salute del tuo server. Questa guida ti guiderà attraverso il processo di
recupero e visualizzazione di queste metriche.

**Nota importante**: questa guida presuppone che tu abbia una conoscenza di base di
Prometheus e PromQL. Se sei nuovo di Prometheus, prendi in considerazione di esplorare la sua
documentazione e i suoi tutorial prima di immergerti nelle metriche di Outline.

## Prerequisiti

- **Server Outline con Prometheus abilitato**: assicurati che il tuo server Outline
abbia le metriche Prometheus abilitate (di solito questa è la configurazione predefinita).

- **Accesso SSH al tuo server**: avrai bisogno dell'accesso SSH per inoltrare la porta
di Prometheus.

## Istruzioni

1. **Inoltra la porta Prometheus**

Connettiti al tuo server tramite SSH e inoltra la porta 9090:

```sh
ssh root@your_server_ip -L 9090:localhost:9090
```

2. **Accedi all'interfaccia web di Prometheus**

Apri il tuo browser web e vai su: <http://localhost:9090/graph>
Interroga le metriche di Prometheus

3. **Utilizza le query PromQL per recuperare le metriche specifiche che ti interessano.**

### Esempio di query PromQL

#### Utilizzo

- **Byte di dati (tramite chiave di accesso, protocollo e direzione):**

`increase(shadowsocks_data_bytes[1d])`

- **Byte di dati (aggregati in base alla chiave di accesso):**

`sum(increase(shadowsocks_data_bytes[1d])) by (access_key)`

- **Byte di dati (per il calcolo dei limiti dei dati):**

`sum(increase(shadowsocks_data_bytes{dir=~"c<p|p>t"}[30d])) by (access_key)`

- **Byte di dati (in base a località, protocollo e direzione):**

`increase(shadowsocks_data_bytes_per_location[1d])`

#### Chiavi di accesso attive

`sum(max(max_over_time(shadowsocks_data_bytes{access_key!=""} [1h])) by (access_key) > bool 0)`

#### Connessioni TCP

- **Connessioni TCP (in base a chiave di accesso, località e stato):**

`increase(shadowsocks_tcp_connections_closed[1d])`

- **Connessioni TCP (in base alla località):**

`increase(shadowsocks_tcp_connections_opened[1d])`

#### UDP

- **Pacchetti UDP (in base a località e stato):**

`increase(shadowsocks_udp_packets_from_client_per_location[1d])`

- **Associazioni UDP (nessuna suddivisione):**

`increase(shadowsocks_udp_nat_entries_added[1d])`

#### Prestazioni

- **Utilizzo CPU (in base al processo):**

`rate(process_cpu_seconds_total[10m])`

- **Memoria (in base al processo):**

`process_virtual_memory_bytes`

#### Informazioni sulla build

- **Prometheus:**

`prometheus_build_info`

- **outline-ss-server:**

`shadowsocks_build_info`

- **Node.js:**

`nodejs_version_info`

L'elenco completo delle metriche disponibili è disponibile
nel [codice sorgente](https://github.com/Jigsaw-Code/outline-ss-server/blob/master/cmd/outline-ss-server/metrics.go) `outline-ss-server`.
